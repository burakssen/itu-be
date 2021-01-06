from PIL import Image
from tools.utils import randomnamegen


def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))


def modifyImage(img,width):
    o_width, o_height = img.size
    if o_width == o_height:
        img = crop_center(img,o_width,o_height).resize((width, width), Image.LANCZOS)
        return img
    elif o_width > o_height:
        result = Image.new(img.mode, (o_width, o_width), (0, 0, 0, 0))
        result.paste(img, (0, (o_width - o_height) // 2))
        resized = result.resize((width,width), Image.LANCZOS)
        return resized
    else:

        result = Image.new(img.mode, (o_height, o_height), (0, 0, 0, 0))
        result.paste(img, ((o_height - o_width) // 2, 0))
        resized = result.resize((width,width), Image.LANCZOS)
        return resized


def squareImage(src, width, newImageName, savePath):
    img = Image.open(src)
    path = f"{savePath}/{randomnamegen(50)}{newImageName}.{img.format.lower()}"
    newimg = modifyImage(img,width)
    newimg.save(path)
    return path