import os
import secrets
from PIL import Image
from flask import current_app


def save_image(form_image, width=250, height=250, path='static/profile_pics'):
    """ Saves The Passed image to directory You can pass it or it will be by default set to "static/profile_pics"
        And you can pass width and height or they will be by default 250 """
    random_hex = secrets.token_hex(8)
    _, extintion = os.path.splitext(form_image.filename)
    image_filename = random_hex + extintion
    image_path = os.path.join(current_app.root_path, path, image_filename)
    output_size = (width, height)
    i = Image.open(form_image)
    i.thumbnail(output_size)
    i.save(image_path)
    return image_filename
