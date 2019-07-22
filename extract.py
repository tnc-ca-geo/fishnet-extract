# standard library
import csv
import os
import sys
import re
from datetime import datetime, timedelta
from getopt import getopt, GetoptError
# third party
from moviepy.editor import VideoFileClip
# project
from metadata import metadata_for_filelike
from crop import crop_pics
# configuration
import config


HELP = (
    '\nextract.py '
    '--video_directory <video_directory> --annotations '
    '<annotation_file>\n\n'
    'options:\n\n'
    '   -a --annotations       Annotation file (csv, required)\n'
#   '   -c --crop              Numbers of pixels to crop from top '
#   '(default 50)\n'
    '   -f --fps               Extracted frame rate per second (default 5)\n'
    '   -o --offset            Windows offset from event start in seconds'
    '(default -10)\n'
    '   -s --stills_directory  Output directory (default ./stills/)\n'
    '   -v --video_directory   Video directory (required)\n'
    '   -w --window            Extracted window in seconds (default 20)\n\n'
    'The annotation csv must implement following columns:\n\n'
    'filename ... name of the videofile in which event can be found\n'
    'start ... start timestamp of the videofile\n'
    'event ... event timestamp\n'
    'label ... event label\n\n'
    'Edit config.mapping to map an annotation file with different '
    'columns names\n\n')


def ensure_directories(filename):
    dirname = os.path.dirname(filename)
    try:
        os.makedirs(dirname)
    except FileExistsError:
        pass


def get_absolute_path(filename):
    return os.path.abspath(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)), filename))


def get_part_from_filename(fil):
    return os.path.split(fil)[1].split('.')[0]


def get_options():
    # TODO: implement argparse
    ret = {
        'stills_directory': get_absolute_path(config.DEFAULT_DIRECTORY),
        'window': config.DEFAULT_WINDOW,
        'crop': config.CROP_TOP,
        'fps': config.DEFAULT_FPS,
        'offset': config.DEFAULT_OFFSET}
    try:
        opts, args = getopt(
            sys.argv[1:],
            'a:c:f:o:s:v:w:h',
            ['annotations=', 'crop=', 'fps=', 'offset=',
             'stills_directory=', 'video_directory=', 'window=', 'help'])
    except GetoptError:
        print(HELP)
        sys.exit(2)
    else:
        for opt, arg in opts:
            if opt in ('-a', '--annotations'):
                path = get_absolute_path(arg)
                if os.path.isfile(path):
                    ret['annotations'] = path
                else:
                    print('\nAnnotations file does not exist.\n')
                    sys.exit(2)
            if opt in ('-c', '--crop'):
                ret['crop'] = int(arg)
            if opt in ('-f', '--fps'):
                ret['fps'] = float(arg)
            if opt in ['-o', '--offset']:
                ret['offset'] = int(arg)
            if opt in ['-s', '--stills_directory']:
                ret['stills_directory'] = get_absolute_path(arg)
            if opt in ['-v', '--video_directory']:
                path = get_absolute_path(arg)
                if os.path.isdir(path):
                    ret['video_directory'] = path
                else:
                    print('\nVideo directory does not exist.\n')
                    sys.exit(2)
            if opt in ('-w', '--window'):
                ret['window'] = int(args)
            if opt in ('-h', '--help'):
                print(HELP)
                sys.exit(2)
        if 'annotations' not in ret:
            print('\nAnnotation file (--annotations or -a) is required\n')
            sys.exit(2)
        if 'video_directory' not in ret:
            print('\nVideo directory (--video_directory or -v) is required\n')
    return ret


def convert_time_delta(timedelta):
    if timedelta.days:
        return None
    hours = int(timedelta.seconds/3600)
    mins = int((timedelta.seconds % 3600)/60)
    secs = int(timedelta.seconds % 60)
    return (hours, mins, secs)


def get_window(delta, diff, offset=0):
    start = (delta[0], delta[1], delta[2] + offset)
    end = (delta[0], delta[1], delta[2] + diff + offset)
    return start, end


def get_epoch(dt):
    return str(int((dt - datetime(1970,1,1)).total_seconds()))


def offset_from_exif(videofile):
    with open(videofile, 'rb') as vf:
        metadata = metadata_for_filelike(vf)
        return metadata.getValues('creation_date')[0]


def transform_dict(dic):
    for item in dic:
        try:
            dic[item] = int(dic[item])
        except ValueError:
            pass
        for timeformat in config.TIMEFORMATS:
            try:
                dic[item] = datetime.strptime(dic[item], timeformat)
            except (TypeError, ValueError):
                pass
    for item in dic.copy():
        if item in config.mapping:
            if config.mapping[item]:
                dic[config.mapping[item]] = dic.pop(item)
            else:
                dic.pop(item)
    dic['label'] = dic['label'].lower().replace(' ', '_')
    return dic


def iterate_over_annotations(opts):
    with open(opts['annotations']) as csvfile:
        reader = csv.DictReader(csvfile)
        for annotation in reader:
            dic = transform_dict(annotation)
            rt = dic['event'] - dic['start']
            ct = convert_time_delta(rt)
            path = os.path.join(opts['video_directory'], dic['filename'])
            try:
                clip = VideoFileClip(path)
            except OSError:
                print('Video {} does not exist'.format(path))
            else:
                if ct:
                    try:
                        start, end = get_window(
                            ct, opts['window'], offset=opts['offset'])
                        snippet = get_epoch(dic['event'])
                        subclip = clip.subclip(t_start=start, t_end=end)
                        out_name = config.OUT_TEMPLATE.format(**{
                            'stills_directory': opts['stills_directory'],
                            'annotations': get_part_from_filename(
                                opts['annotations']),
                            'filename': get_part_from_filename(dic['filename']),
                            'timestamp': snippet,
                            'camera': dic['camera'],
                            'label': dic['label']})
                        ensure_directories(out_name)
                        subclip.write_images_sequence(out_name, fps=opts['fps'])
                    except ValueError:
                        pass


def main():
    opts = get_options()
    iterate_over_annotations(opts)
    # crop_pics(opts['stills_directory'], opts['crop'])
    print('\nDONE\n')


if __name__ == '__main__':
    main()
