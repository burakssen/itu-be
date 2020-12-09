import os
from werkzeug.utils import secure_filename
from tools.imagemodify import squareImage

def uploadImage(file,newname):
    return squareImage(file,512,newname,"/static/profile_images")
    