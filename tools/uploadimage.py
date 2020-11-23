import os
from werkzeug.utils import secure_filename

def uploadImage(file):
    filename = secure_filename(file.filename)

    assets_dir = os.path.join(os.path.dirname("./"), 'static')
    path = os.path.join(assets_dir, 'profile_images', filename)
    path = path.replace("\\","/")
    file.save(path)
    path = "." + path
    return path