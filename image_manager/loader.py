import numpy as np
from PIL import Image

def open_image(path):
    """Return the image Vectors/Matrix"""
    image = Image.open(path)
    
    return np.array(image)