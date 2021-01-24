import os
from PIL import Image
import tempfile
import io
import json
from datetime import datetime


# TODO write image array data stream to temp images and then close it without saving the image
def image_combine(png_collect, player_name):
    images = [Image.open(x) for x in png_collect]
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_im = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset,0))
        x_offset += im.size[0]

    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")
    tmp_filename = 'Image_Tmp/' + player_name + dt_string + ".png"
    new_im.save(tmp_filename)
    img_json_delete_todo(tmp_filename)
    return tmp_filename

# TODO: find a way to delete image in short memory
    #new_im.save(file_name)
    #return new_im
    #path = os.path.dirname(new_im)
    #print(path)


def delete_image(file_path):
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            return True
        except Exception:
            print(Exception)
            return False

def image_to_byte_array(image:Image):
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format='PNG')
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr

def img_json_delete_todo(tmp_img):
    file_to_delete = {'name': tmp_img, 'deleted': 0}

    def write_json(data, filename='JSON/delete_temp_imgs_todo.json'):
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    with open('../JSON/delete_temp_imgs_todo.json') as json_file:
        data = json.load(json_file)
        temp = data['files_to_delete']
        temp.append(file_to_delete)

    write_json(data)


def img_json_delete():
    with open('../JSON/delete_temp_imgs_todo.json') as file:
        data = json.load(file)
        temp = data['files_to_delete']

    x = len(temp)
    while x > 0:
        row = temp[x-1]
        if delete_image(row['name']):
            del temp[x-1]
        x -= 1

    with open('../JSON/delete_temp_imgs_todo.json', 'w') as file:
        json.dump(data, file, indent=4)








