import darkdetect
from pathlib import Path



UTF8_ENCODING = 'utf-8'
WINDOWS_ENCODING = 'windows-1250'

BAD_ANS_TEXT = 'Jesteś dupa! Prawidłowa odpowiedź to: '
BAD_ANS_COLOR = 'red'
GOOD_ANS_TEXT = 'Brawo!'
GOOD_ANS_COLOR = 'green'

if darkdetect.isDark():
    DEFAULT_COLOR = 'white'
else:
    DEFAULT_COLOR = 'black'

WINDOW_GEOMETRY = [
    10,
    10,
    640,
    480,
]

ROOT_PATH = Path(__file__).parent
CONFIG_PATH = ROOT_PATH.joinpath('.config.json')
STATS_PATH = ROOT_PATH.joinpath('.stats.json')

EXCLUDED_EXTENSIONS = ['.swp']
IGNORED_LINES = [
    '\n',
]
COMMENT_CHARS = [
    '#',
]

WINDOW_RESIZABLE = False

try:
    import local_settings  # noqa: F401
except ImportError:
    pass
