UTF8_ENCODING = 'utf-8'
WINDOWS_ENCODING = 'windows-1250'

BAD_ANS_TEXT = 'Jesteś dupa! Prawidłowa odpowiedź to: '
BAD_ANS_COLOR = 'red'
GOOD_ANS_TEXT = 'Brawo!'
GOOD_ANS_COLOR = 'green'

ERROR_FILE_LOCATION = 'data/_ERR.txt'

EXCLUDED_EXTENSIONS = ['.swp']
IGNORED_LINES = [
    '\n',
]

WINDOW_RESIZABLE = False

try:
    import local_settings
except ImportError:
    pass
