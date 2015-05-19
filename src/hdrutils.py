import os 
from PIL import Image
from numpy import array, uint8


OVER_SATURATION_LIMIT = 245
UNDER_SATURATION_LIMIT = 10
MAX_SIZE = 1024
N = 4
SAMPLE_COUNT = 500


def get_images(directory, resize):
    images = []
    for d in os.listdir(directory):
        img = Image.open(directory+'/'+d)
        size = img.size

        ref = max(size[0], size[1])
        factor = ceil(ref / MAX_SIZE)

        if resize:
            img = img.resize((int(size[0] / factor), int(size[1] / factor)), Image.ANTIALIAS)
        arr = array(img).astype(float)
        images.append(arr)
    return images