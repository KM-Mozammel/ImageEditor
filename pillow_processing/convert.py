from PIL import Image

def to_grayscale(image):
    return image.convert("L")
