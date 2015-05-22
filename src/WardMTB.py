import hdrutils as hd


images = hd.get_images(hd.path_set_1, False)

i0 = hd.IMG(images[0])
#i1 = hd.IMG(images[1])
#i2 = hd.IMG(images[2])


#i0.save_grayscale("img/lol_0.png")
#i1.save_grayscale("img/lol_1.png")
#i2.save_grayscale("img/lol_2.png")

i0.save_mtb("img/mtb_0.png")
#i1.save_mtb("img/mtb_1.png")
#i2.save_mtb("img/mtb_2.png")