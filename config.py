"""
Set defaults here
"""

DEFAULT_DIRECTORY = 'stills'
DEFAULT_CLIPS_DIRECTORY = 'clips'
DEFAULT_FPS = 5
DEFAULT_WINDOW = 20
DEFAULT_OFFSET = -10
TIMEFORMATS = ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M:%S.%f']
OUT_TEMPLATE = '{stills_directory}/{filename}-{timestamp}-{label}-%03d.jpeg'
VIDEO_OUT_TEMPLATE = '{clips_directory}/{filename}-{timestamp}-{label}.mp4'
CROP_TOP = 50
CLIPS = False
CLIP_DIRECTORY = 'clips'


mapping = {
    'vidstart_ts': 'start',
    'catch_ts': 'event',
    'vidend_ts': None,
    'label_l1': 'label',
    'label_l2': None,
    'cam_num': 'camera'}
