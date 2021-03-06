import os 
from PIL import Image
from numpy import array, uint8, median, percentile
from math import ceil
from bitarray import bitarray

OVER_SATURATION_LIMIT = 245
UNDER_SATURATION_LIMIT = 10
MAX_SIZE = 1024
N = 4
SAMPLE_COUNT = 500

path_set_1 = "/home/alprkskn/ceng/771/HDR_Toolbox/demos/stack"
path_set_2 = "/home/alprkskn/ceng/771/HDR_Toolbox/demos/stack_alignment"

def get_images(directory):
    images = []
    for d in os.listdir(directory):
        img = Image.open(directory+'/'+d)
        images.append(img)
    return images

def get_images_as_numpy_arrays(directory, resize):
    images = []
    for d in os.listdir(directory):
        img = Image.open(directory+'/'+d)
        size = img.size

        ref = max(size[0], size[1])
        factor = ceil(ref / MAX_SIZE)

        if resize:
            img = img.resize((int(size[0] / factor), int(size[1] / factor)), Image.ANTIALIAS)
        arr = array(img)
        images.append(arr)
    return images

def get_luminances(img):
    result = []
    for row in img:
        r = []
        for pixel in row:
            r.append((pixel[0]*54 + pixel[1]*183 + pixel[2]*19)/256)
        result.append(r)
    return result

def image_array_from_luminances(lum):
    result = []
    for row in lum:
        r = []
        for pixel in row:
            r.append([pixel, pixel, pixel])
        result.append(r)
    return array(result, "uint8")

def flatten_luminance_array(arr):
    luminances = []
    for row in arr:
        for pixel in row:
            luminances.append(pixel)
    return luminances

def image_from_bitarray(b_array, width, height):
    arr = []
    for x in range(height):
        row = []
        for y in range(width):
            pixel = b_array[x*width+y]
            row.append([pixel, pixel, pixel])
        arr.append(row)
    img = Image.fromarray(array(arr, "uint8") * 255)
    return img


class IMG:
    def __init__(self, image):
        self.height = image.size[1]
        self.width = image.size[0]
        self.image = image
        self.image_array = array(image)
        self.formatted_lum = get_luminances(self.image_array)
        self.luminances = flatten_luminance_array(self.formatted_lum)
        self.bits = bitarray()
        self.exclusion_bits = bitarray()
        self.compute_mtb()
        print "Init image", median(self.luminances)

    def determine_percentile(self):
        return 50

    def save_exclusion(self, path):
        bytes = self.exclusion_bits.to01()
        arr = []
        for x in range(self.height):
            row = []
            for y in range(self.width):
                pixel = bytes[x*self.width+y]
                row.append([pixel, pixel, pixel])
            arr.append(row)
        img = Image.fromarray(array(arr, "uint8") * 255)
        img.save(path, path.split('.')[-1])            

    def save_mtb(self, path):
        bytes = self.bits.to01()
        arr = []
        for x in range(self.height):
            row = []
            for y in range(self.width):
                pixel = bytes[x*self.width+y]
                row.append([pixel, pixel, pixel])
            arr.append(row)
        img = Image.fromarray(array(arr, "uint8") * 255)
        img.save(path, path.split('.')[-1])

    def save_grayscale(self, path):
        img = Image.fromarray(image_array_from_luminances(self.formatted_lum))
        img.save(path, path.split('.')[-1])

    def compute_mtb(self):
        threshold_percentile = self.determine_percentile()
        m = percentile(self.luminances, threshold_percentile)
        for p in self.luminances:
            self.bits.append(p > m)
            self.exclusion_bits.append((p < (m - 4)) or (p > (m + 4)))
