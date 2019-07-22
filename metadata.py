# from http://stackoverflow.com/
# questions/11302908/python-using-hachoir-how-extract-metadata-for-file-like-objects
# from hachoir.core.error import HachoirError
from hachoir.stream.input import InputIOStream
from hachoir.parser.guess import guessParser
from hachoir.metadata import extractMetadata


def metadata_for_filelike(filelike):
    try:
        filelike.seek(0)
    except (AttributeError, IOError):
        return None

    stream = InputIOStream(filelike, None, tags=[])
    parser = guessParser(stream)

    if not parser:
        return None

    try:
        metadata = extractMetadata(parser)
    # used to be HachoirError, but not longer defined by package
    except:
        return None

    return metadata
