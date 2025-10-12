import re

INTERVAL_PATTERN = re.compile(
    r" {8}intervals \[(\d*)\]\:\n {12}xmin = (\d*\.?\d*) \n {12}xmax = (\d*\.?\d*) \n {12}text = \"(.*)\" \n",
    re.MULTILINE,
)

def get_clip_timestamps(fp: str):

    with open(fp, 'r', encoding='utf-8') as f:
        matches = re.findall(INTERVAL_PATTERN, f.read())

    assert int(matches[-1][0]) == len(matches), f'Trouble parsing textgrid. Index of final match: {matches[-1][0]}, but {len(matches)} matches.'

    speech_segments = []
    for match in matches:
        if match[3] != 'silent':
            speech_segments.extend(match[1:3])

    return ','.join(speech_segments)