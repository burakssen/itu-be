import os
from werkzeug.utils import secure_filename
from tools.imagemodify import squareImage

def uploadImage(file,newname):
    filename = secure_filename(file.filename)

    assets_dir = os.path.join(os.path.dirname("./"), 'static')
    path = os.path.join(assets_dir, 'temp', filename)
    path = path.replace("\\","/")
    file.save(path)
    prev_path = path
    #print(path)
    img, path = squareImage(path,512,newname,"/static/profile_images")
    img.save("." + path, quality=512)
    os.remove(prev_path)
    print(path)
    return path
    