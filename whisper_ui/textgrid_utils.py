import re
import os

INTERVAL_PATTERN = re.compile(
    r"( {8}intervals \[(\d*)\]\:\n {12}xmin = (\d*\.?\d*) \n {12}xmax = (\d*\.?\d*) \n {12}text = \"(.*)\" \n)",
    re.MULTILINE,
)

def get_intervals(fp: str):
    with open(fp, 'r', encoding='utf-8') as f:
        matches = re.findall(INTERVAL_PATTERN, f.read())

    assert int(matches[-1][1]) == len(matches), f'Trouble parsing textgrid. Index of final match: {matches[-1][1]}, but {len(matches)} matches.'

    return matches

def get_clip_timestamps(fp: str):
    
    matches = get_intervals(fp)

    speech_segments = []
    for match in matches:
        if match[4] != 'silent':
            speech_segments.extend(match[2:4])
    
    return ','.join(speech_segments)

def write_textgrid(fp: str, segments=['abc'] * 11):
    orig_text = open(fp, 'r', encoding='utf-8').read()
    intervals = get_intervals(fp)
    j = 0
    for i, interval in enumerate(intervals):
        if interval[4] == 'silent':
            orig_text = re.sub(
                pattern=intervals[i][0],
                repl=re.sub('silent', segments[j], intervals[i][0]),
                string=orig_text
            )
            j += 1
    orig = os.path.splitext(fp)
    os.rename(fp, orig[0] + '_blank' + orig[1])
    with open(fp, 'w+', encoding='utf-8') as f:
        f.write(orig_text)

def write_textgrid(fp: str, segments: list[str]):
    orig_text = open(fp, 'r', encoding='utf-8').read()
    intervals = get_intervals(fp)
    j = 0
    for i, interval in enumerate(intervals):
        if interval[4] == 'silent':
            if j >= len(segments):
                raise ValueError(f"Not enough segments provided. Need at least {j+1}, but only have {len(segments)}")
            
            # Escape the pattern and do a simple string replacement
            old_interval = interval[0]
            new_interval = old_interval.replace('text = "silent"', f'text = "{segments[j]}"')
            
            orig_text = orig_text.replace(old_interval, new_interval, 1)  # Replace only first occurrence
            j += 1
    
    orig = os.path.splitext(fp)
    os.rename(fp, orig[0] + '_blank' + orig[1])
    with open(fp, 'w+', encoding='utf-8') as f:
        f.write(orig_text)