import hdrutils as hd
import numpy as np

images = hd.get_images(hd.path_set_1)

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

p = get_image_pyramid(images[0], 4)
print len(p)

index=0
for a in p:
    a.save_grayscale("img/greyscale_"+str(index)+".png")
    a.save_mtb("img/mtb_"+str(index)+".png")
    index+=1