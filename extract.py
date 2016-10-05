import os
import sys
from datetime import datetime
from getopt import getopt, GetoptError
from moviepy.editor import VideoFileClip
from PIL import Image
from metadata import metadata_for_filelike

from moviepy.video.fx.accel_decel import accel_decel
from moviepy.video.fx.blackwhite import blackwhite


INFILE = '../media/cam_3_day.mp4'
ANNOTATIONS ='../media/1631.txt'
DEFAULT_FOLDER = os.path.dirname(os.path.realpath(__file__))
TIMEFORMAT = '%d/%m/%Y %H:%M:%S'

HELP = ('\nextract.py --videofile <inputfile> --annotations <annotationfile>.txt\n\n'
        'options:\n'
        '          -o --offset  Start time of the video (you might be able to get it from the first frame).\n'
        '                       If not provided, EXIF \'Create Date\' will be used.\n'
        '                       Time format is \"YYYY-MM-DD HH:MM:SS\". \n'
        '                       Use quotes around the date or escape otherwise.\n'
        '          -f --folder  Output folder. If not provided the current folder will be used.\n'
        '          -w --window  Number of seconds that will be extracted from the event start. Defaults to 3.\n'
        '          -h --help    This help\n')


def get_absolute_path(filename):
    return os.path.abspath(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)), filename))


def get_options():
    ret = {
        'folder': DEFAULT_FOLDER,
        'offset': None,
        'window': 3
    }
    try:
        opts, args = getopt(
            sys.argv[1:],
            'v:a:o:f:w:h',
            ['videofile=', 'annotations=', 'offset=',
             'folder=', 'window=', 'help'])
    except GetoptError:
        print HELP
        sys.exit(2)
    else:
        for opt, arg in opts:
            if opt in ('-v', '--videofile'):
                path = get_absolute_path(arg)
                if os.path.isfile(path):
                    ret['videofile'] = path
                else:
                    print '\nVideofile does not exist.\n'
                    sys.exit(2)
            if opt in ('-a', '--annotations'):
                path = get_absolute_path(arg)
                if os.path.isfile(path):
                    ret['annotations'] = path
                else:
                    print '\nAnnotations file does not exist.\n'
                    sys.exit(2)
            if opt in ('-h', '--help'):
                print HELP
                sys.exit(2)
            elif opt in ('-o', '--offset'):
                try:
                    ret['offset'] = datetime.strptime(
                        arg, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    print '\nInvalid date format.\n'
                    sys.exit(2)
            elif opt in ('-f', '--folder'):
                path = get_absolute_path(arg)
                if os.path.isdir(path):
                    ret['folder'] = path
                else:
                    print '\nOutput folder does not exists.\n'
                    sys.exit(2)
            elif opt in ('-w', '--window'):
                try:
                    ret['window'] = int(arg)
                except ValueError:
                    pass
    if not 'videofile' in ret:
        print '\nVideofile is required.\n'
        sys.exit(2)
    if not 'annotations' in ret:
        print '\nAnnotationfile is required.\n'
        sys.exit(2)
    return ret


def convert_time_delta(timedelta):
    if timedelta.days:
        return None
    hours = int(timedelta.seconds/3600)
    mins = int((timedelta.seconds % 3600)/60)
    secs = int(timedelta.seconds % 60)
    return (hours, mins, secs)


def get_window(timedelta, diff):
    start = timedelta
    end = (timedelta[0], timedelta[1], timedelta[2] + diff)
    return start, end


def get_epoch(dt):
    return str(int((dt - datetime(1970,1,1)).total_seconds()))


def offset_from_exif(videofile):
    with open(videofile, 'rb') as vf:
        metadata = metadata_for_filelike(vf)
        return metadata.getValues('creation_date')[0]


def iterate_over_annotations(opts):
    offset = opts['offset'] or offset_from_exif(opts['videofile'])
    print '\nSetting start time to {}.'.format(offset)
    print 'Annotation times will be interpreted relative to this time.\n\n'
    clip = VideoFileClip(opts['videofile'])
    infile_snippet = os.path.split(opts['videofile'])[1].replace('.mp4', '')
    with open(opts['annotations']) as a:
        for line in a:
            parts = line.split(',')
            dt = datetime.strptime(parts[16], TIMEFORMAT)
            rt = dt - offset
            ct = convert_time_delta(rt)
            if ct:
                try:
                    start, end = get_window(ct, opts['window'])
                    snippet = get_epoch(dt)
                    subclip = clip.subclip(t_start=start, t_end=end)
                    subclip.write_images_sequence(opts['folder'] + '/'+ infile_snippet + '_' + snippet + '_' + 'image%03d.jpeg')
                except ValueError:
                    pass


def main():
    opts = get_options()
    iterate_over_annotations(opts)


if __name__ == '__main__':
    main()
