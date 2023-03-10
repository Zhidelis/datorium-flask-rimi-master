import os
from werkzeug.utils import secure_filename


def upload_image(upload_folder, image):
    image_name = secure_filename(image.filename)
    image_path = os.path.join(upload_folder, image_name)
    image.save(image_path)
    return image_path, image_name
