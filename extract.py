import os
import sys
from datetime import datetime
from getopt import getopt, GetoptError
from moviepy.editor import VideoFileClip
from metadata import metadata_for_filelike

INFILE = '../media/cam_3_day.mp4'
DEFAULT_FOLDER = '.'
TIMEFORMAT = '%d/%m/%Y %H:%M:%S'
OUT_TEMPLATE = '{0}/{1}_{2}_{3}_{4}_image%03d.jpeg'

HELP = (
    '\nextract.py '
    '--videofile <inputfile> --annotations <annotationfile>.txt\n\n'
    'options:\n\n'
    '   -o --offset  Start time of the video (you might be able to get it\n'
    '                from the first frame). If not provided, EXIF\n'
    '                \'Create Date\' will be used. Time format is \n'
    '                \"YYYY-MM-DD HH:MM:SS\". Use quotes around the \n'
    '                date or escape otherwise.\n'
    '   -f --folder  Output folder.\n'
    '                If not provided the current folder will be used.\n'
    '   -w --window  Number of seconds that will be extracted from the event\n'
    '                start. Defaults to 3.\n'
    '   -h --help    This help.\n')


def get_absolute_path(filename):
    return os.path.abspath(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)), filename))


def get_part_from_filename(fil):
    return os.path.split(fil)[1].split('.')[0]


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
                    out_name = OUT_TEMPLATE.format(
                        opts['folder'],
                        get_part_from_filename(opts['annotations']),
                        get_part_from_filename(opts['videofile']),
                        snippet,
                        parts[13].strip('"'))  # species code
                    subclip.write_images_sequence(out_name, fps=10)
                except ValueError:
                    pass


def main():
    opts = get_options()
    iterate_over_annotations(opts)


if __name__ == '__main__':
    main()
