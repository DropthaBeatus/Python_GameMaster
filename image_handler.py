import discord
import os
from PIL import Image


def image_combine(png_collect, file_name):
    images = [Image.open(x) for x in png_collect]
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_im = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset,0))
        x_offset += im.size[0]

#TODO: find a way to delete image in short memory
    new_im.save(file_name)
    #path = os.path.dirname(new_im)
    #print(path)


def delete_image(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)