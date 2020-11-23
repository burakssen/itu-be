import os
from werkzeug.utils import secure_filename
from tools.imagemodify import squareImage

def uploadImage(file,newname):
    filename = secure_filename(file.filename)

    assets_dir = os.path.join(os.path.dirname("./"), 'static')
    path = os.path.join(assets_dir, filename)
    path = path.replace("\\","/")
    print(path)
    path = squareImage(path,512,newname,"./static/profile_images")
    return path