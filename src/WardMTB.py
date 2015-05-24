import hdrutils as hd
import numpy as np

from bitarray import bitarray
from math import ceil

#i1 = hd.IMG(images[1])
#i2 = hd.IMG(images[2])


#i0.save_grayscale("img/lol_0.png")
#i1.save_grayscale("img/lol_1.png")
#i2.save_grayscale("img/lol_2.png")

#i1.save_mtb("img/mtb_1.png")
#i2.save_mtb("img/mtb_2.png")

def get_image_pyramid(image, max_depth=1):
    result = []
    width = image.size[0]
    height = image.size[1]
    for l in range(max_depth):
        img = (image.resize((width/(2**l), height/(2**l))))
        result.append(hd.IMG(np.array(img)))
    return result

def shrink2(image_struct):
    image = image_struct.image
    width = image.size[0]
    height = image.size[1]
    img = (image.resize((int(width/2), int(height/2))))
    return hd.IMG(img)

def column_shift(array, x, width, height):
    if x == 0:
        return bitarray(array)
    a = []
    result = bitarray()
    i = 0
    max_count = width*height
    while i < max_count:
        a.append(array[i:i+width])
        i+=width
    count = 0
    for row in a:
        if x > 0:
            row = bitarray('0' * x) + row[:-x]
        elif x < 0:
            row = row[abs(x):] + bitarray('0' * abs(x))
        result.extend(row)
        count+=1
    return result

def row_shift(array, y, width, height):
    if y == 0:
        return bitarray(array)
    result = bitarray()
    if y > 0:
        s = '0' * width * y
        result = bitarray(s) + array[:-width*y]
    elif y < 0:
        s = '0' * width * abs(y)
        result = array[abs(y) * width:] + bitarray(s)
    return result

def array_shift(array, x, y,width, height):
    result = column_shift(array, x, width, height)
    result = row_shift(result, y, width, height)
    return result

#p = get_image_pyramid(images[0], 4)
#print len(p)

#index=0
#for a in p:
#    a.save_grayscale("img/greyscale_"+str(index)+".png")
#    a.save_mtb("img/mtb_"+str(index)+".png")
#    a.save_exclusion("img/exclusion_"+str(index)+".png")
#    index+=1

#count = 0
#for img in images:
#    pyr = get_image_pyramid(img, 4)
#    index=0
#    for a in pyr:
#        a.save_grayscale("img/" + str(count) + "greyscale_"+str(index)+".png")
#        a.save_mtb("img/" + str(count)+"mtb_"+str(index)+".png")
#        a.save_exclusion("img/"+str(count)+"exclusion_"+str(index)+".png")

#        shift_bits = hd.array_shift(a.bits, 100, 50, a.width, a.height)
#        i = hd.image_from_bitarray(shift_bits, a.width, a.height)
#        i.save("img/"+str(count)+"shift_"+str(index)+".png")
#        index+=1
#    count += 1

def get_exp_shift(img1, img2, shift_bits, shift_ret):
    cur_shift = [0, 0]
    if shift_bits > 0:
        sml_img1 = shrink2(img1)
        sml_img2 = shrink2(img2)
        get_exp_shift(sml_img1, sml_img2, shift_bits-1, cur_shift)
        cur_shift[0] *=2
        cur_shift[1] *=2
    else:
        cur_shift[0] = cur_shift[1] = 0
        tb1 = img1.bits
        eb1 = img1.exclusion_bits
        tb2 = img2.bits
        eb2 = img2.exclusion_bits
        min_err = img1.width * img1.height
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                xs = cur_shift[0] + i
                ys = cur_shift[1] + j
                shifted_tb2 = array_shift(tb2, xs, ys, img1.width, img1.height)
                shifted_eb2 = array_shift(eb2, xs, ys, img1.width, img1.height)
                diff_b = tb1^shifted_tb2
                diff_b = diff_b & eb1
                diff_b = diff_b & shifted_eb2
                err = diff_b.count()
                if err < min_err:
                    shift_ret[0] = xs
                    shift_ret[1] = ys
                    min_err = err
    return shift_ret

def compute_alignments(path,depth):
    images = hd.get_images(path)
    #a = bitarray([1,0,1,0,0,1,0,1,1,0,1,0,0,1,0,1])
    REFERENCE = int(len(images) / 2)

    #IMG1 = hd.IMG(images[0])
    #IMG2 = hd.IMG(images[1])

    #shift_ret = [0,0]
    #get_exp_shift(IMG1,IMG2, 3, shift_ret)
    #print shift_ret

    REF = hd.IMG(images[REFERENCE])
    alignment_shifts = []
    for i in range(len(images)):
        img = hd.IMG(images[i])
        if i == REFERENCE:
            alignment_shifts.append([0,0])
            continue
        shift_ret = [0,0]
        get_exp_shift(REF, img, depth, shift_ret)
        alignment_shifts.append(shift_ret)
    return alignment_shifts
