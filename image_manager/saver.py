from PIL import Image

def save_image(image, path):
    Image.fromarray(
        image.astype("uint8")
    ).save(path)