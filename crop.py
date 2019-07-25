import os
from PIL import Image


def crop_pics(folder, top):
    """
    This crops all images in a folder. This is obsolete to the project
    since the function is now covered by MoviePy.
    """
    # TODO: remove
    image_names = os.listdir(folder)
    number = len(image_names)
    counter = 0
    if top < 1:
        print('Nothing to crop.')
        return True
    for image_name in image_names:
        image_path = os.path.join(folder, image_name)
        try:
            image = Image.open(image_path)
        except IOError:
            print('{} does not seem to be an image file.'.format(image_path))
        else:
            image = image.crop((0, top, image.size[0], image.size[1]))
            image.save(image_path)
            counter += 1
            print(
                'Image {} out of {} cropped by {} pixels from top.'.format(
                counter, number, top))
    return True
