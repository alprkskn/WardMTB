import hdrutils as hd

def get_luminances(img):
    result = []
    for row in img:
        r = []
        for pixel in row:
            r.append((pixel[0]*54 + pixel[1]*183 + pixel[2]*19)/256)
        result.append(r)
    return result

images = hd.get_images(hd.path_set_1, False)

