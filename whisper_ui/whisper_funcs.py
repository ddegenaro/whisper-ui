import os
import re
import json
from gc import collect

import torch
import whisper
from whisper.tokenizer import LANGUAGES, TO_LANGUAGE_CODE
from pyannote.audio import Pipeline

from whisper_ui.handle_prefs import USER_PREFS, check_model

SUPPORTED_FILETYPES = ('flac', 'm4a', 'mp3', 'mp4', 'wav')
AVAILABLE_MODELS = whisper.available_models()
VALID_LANGUAGES = sorted(
    LANGUAGES.keys()
) + sorted(
    [k.title() for k in TO_LANGUAGE_CODE.keys()]
)
LANGUAGES_FLIPPED = {v: k for k, v in LANGUAGES.items()}
TO_LANGUAGE_CODE_FLIPPED = {v: k for k, v in TO_LANGUAGE_CODE.items()}
SAMPLE_RATE = 16_000

if torch.cuda.is_available():
    DEVICE = torch.device('cuda')
elif torch.backends.mps.is_available():
    DEVICE = torch.device('mps')
else:
    DEVICE = torch.device('cpu')

class ModelInterface:

    def __init__(self):
        if USER_PREFS['DEBUG']:
            self.model = 'abc'
        else:
            self.model = None
        self.diarize_model = None
        
    def map_available_language_to_valid_language(self, available_language):
        
        if available_language == 'None':
            return None
        
        al = available_language.lower()
        if al not in VALID_LANGUAGES:
            if al in LANGUAGES_FLIPPED and LANGUAGES_FLIPPED[al] in VALID_LANGUAGES:
                return LANGUAGES_FLIPPED[al]
            elif al in TO_LANGUAGE_CODE_FLIPPED and TO_LANGUAGE_CODE_FLIPPED[al] in VALID_LANGUAGES:
                return TO_LANGUAGE_CODE_FLIPPED[al]
        else:
            return al

    def get_model(self, switch_model: bool = False):
        
        model_name = USER_PREFS["model"]
        
        if not check_model(model_name):
            print(f'\tWarning: model {model_name} not found in cache. Please download it.')
            return
        
        if self.model is None or switch_model:
            print(f'\tLoading model {model_name}. This may take a while if you have never used this model.')
            print(f'\t\tChecking for GPU...')
            
            if DEVICE == 'cuda' or DEVICE == 'mps':
                print('\t\tGPU found.')
            else:
                print('\t\tNo GPU found. Using CPU.')
            try:
                self.model = whisper.load_model(name=USER_PREFS['model'], in_memory=True)
            except:
                self.model = whisper.load_model(name=USER_PREFS['model'])
            try:
                self.model.to(DEVICE)
            except:
                print(f'\t\tWarning: issue loading model onto device {DEVICE}. Using {self.model.device}.')
            print(f'\tLoaded model {model_name} successfully.')
        else:
            print(f'\tUsing currently loaded model ({model_name}).')

    def format_outputs(self, outputs):
        
        text_template = USER_PREFS['text_template']
        segmentation_template = USER_PREFS['segmentation_template']
        
        text_template_filled = None
        segmentation_lines = None
        
        if USER_PREFS['do_text']:
            text_is = USER_PREFS['text_insertion_symbol']
            text_template_filled = text_template.replace(
                text_is, outputs['text']
            )
        
        if USER_PREFS['do_segmentation']:
            text_is = USER_PREFS['segment_insertion_symbol']
            start_is = USER_PREFS['start_time_insertion_symbol']
            end_is = USER_PREFS['end_time_insertion_symbol']
            
            segmentation_lines = []
            for segment in outputs['segments']:
                text = segment['text']
                start = str(segment['start'])
                end = str(segment['end'])
                seg_template_filled = segmentation_template.replace(
                    text_is, text
                ).replace(
                    start_is, start
                ).replace(
                    end_is, end
                )
                segmentation_lines.append(seg_template_filled)
                
        return {
            'text': text_template_filled,
            'segmentation_lines': segmentation_lines
        }

    def make_paths(self, output_dir, fname):
        
        txt_loc = os.path.join(output_dir, fname + '.txt')
        seg_loc = os.path.join(output_dir, fname + '.seg')
        json_loc = os.path.join(output_dir, fname + '.json')
        
        # if any of the files already exist, make new ones with incremented numbers
        while any((os.path.exists(txt_loc), os.path.exists(seg_loc), os.path.exists(json_loc))):
            
            # if already numbered, just increment
            endswith_suffix = re.search(r'_\d+$', fname)
            if endswith_suffix:
                fname = fname[:endswith_suffix.start()] +'_' + str(int(endswith_suffix.group()[1:])+1)
            
            # if not numbered, add _1
            else:
                fname += '_1'
                
            txt_loc = os.path.join(output_dir, fname + '.txt')
            seg_loc = os.path.join(output_dir, fname + '.seg')
            json_loc = os.path.join(output_dir, fname + '.json')
        
        # if none of the files exist, fname is fine
        else:
            return txt_loc, seg_loc, json_loc

    def write_outputs(self, outputs: dict, formatted_outputs: dict, fname: str):
        text = formatted_outputs['text']
        segmentation_lines = formatted_outputs['segmentation_lines']
        
        output_dir = USER_PREFS['output_dir']
        os.makedirs(output_dir, exist_ok=True)
        
        txt_loc, seg_loc, json_loc = self.make_paths(output_dir, fname)
        
        if USER_PREFS['do_text']:
            with open(txt_loc, 'w+', encoding='utf-8') as f:
                f.write(text.strip())
            print(f'\t\tWrote transcription to "{os.path.abspath(txt_loc)}".')
        if USER_PREFS['do_segmentation']:
            with open(seg_loc, 'w+', encoding='utf-8') as g:
                for line in segmentation_lines:
                    g.write(line.strip() + '\n')
            print(f'\t\tWrote segmentation to "{os.path.abspath(seg_loc)}".')
        if USER_PREFS['do_json']:
            with open(json_loc, 'w+', encoding='utf-8') as h:
                json.dump(outputs, h, indent=4)
            print(f'\t\tWrote JSON data to "{os.path.abspath(json_loc)}".')

    def transcribe(self, paths: list, switch_model: bool):

        BATCH_SIZE = USER_PREFS['batch_size']
        
        if not paths:
            print('No matching files found.\n')
            return
        
        print(f'Beginning transcription of {len(paths)} audio file(s).')

        self.get_model(switch_model=switch_model)

        if self.diarize_model is None:
            print('Loading diarization model.')
            self.diarize_model = Pipeline.from_pretrained(
                "pyannote/speaker-diarization-3.1",
                use_auth_token=USER_PREFS['hf_auth_token']
            )
            try:
                self.diarize_model.to(DEVICE)
            except:
                print(f'\t\tWarning: issue loading diarization model onto device {DEVICE}. Using {self.model.device}.')
        else:
            print('Diarization model pre-loaded.')
        
        for i, path in enumerate(paths):
            
            print(f'\tTranscribing "{path}" (file {i+1}/{len(paths)})...')
            
            path = os.path.normpath(path)
            assert os.path.exists(path)
            
            basename = os.path.basename(path)
            fname, ext = os.path.splitext(basename)
            
            if ext[1:] not in SUPPORTED_FILETYPES:
                msg = f'\tWarning: file "{path}" may not be supported. '
                msg += '\tSupported filetypes are: ' + ', '.join(SUPPORTED_FILETYPES)
                print(msg)
            
            if USER_PREFS['DEBUG']:
                outputs = json.load(
                    open(os.path.join('test_outputs', 'example_output.json'), 'r', encoding='utf-8')
                )
            else:
                
                audio = whisper.load_audio(path)

                with torch.no_grad():
                    diarized_out = self.diarize_model(
                        {
                            'waveform': torch.tensor(audio).unsqueeze(0).to(DEVICE),
                            'sample_rate': SAMPLE_RATE
                        }
                    )
                
                torch.cuda.empty_cache()
                collect()

                audio_segs = [
                    audio[round(seg.start * SAMPLE_RATE) : round(seg.end * SAMPLE_RATE + 1)]
                    for seg in diarized_out.itersegments()
                ]

                print(f'\tFound {len(audio_segs)} segments. Transcribing segments...')

                output_texts = []
                output_langs = []

                for batch_start in range(0, len(audio_segs), BATCH_SIZE):
                    batch_end = min(batch_start + BATCH_SIZE, len(audio_segs))
                    batch_segs = audio_segs[batch_start:batch_end]
                    
                    for i, audio_seg in enumerate(batch_segs):
                        with torch.no_grad():
                            model_outputs = self.model.transcribe(
                                audio_seg,
                                language = None,
                                task = 'transcribe'
                            )
                        output_texts.append(model_outputs['text'])
                        output_langs.append(model_outputs['language'])
                    
                    print(f'\tTranscribed batch {batch_start//BATCH_SIZE + 1}/{(len(audio_segs) + BATCH_SIZE - 1)//BATCH_SIZE} ({batch_end}/{len(audio_segs)} segments).')
                    torch.cuda.empty_cache()
                    collect()

                formatted_outputs = [
                    self.format_outputs(output_text, output_lang, seg)
                    for output_text, output_lang, seg in zip(output_texts, )
                ]
                for formatted_output in formatted_outputs:
                    self.write_outputs(outputs, formatted_output, fname)
                print('\tDone.')
        
        print(f'Transcribed {len(paths)} files.\n')

        return self