import numpy as np


def increase(image, value):
    
    bright = image.copy()
    
    bright[:, :, :3] = np.clip(
        bright[:, :, :3] + value,
        0,
        225
    )
    
    return bright