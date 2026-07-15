import numpy as np


def increase(image, value):
    return brightness(image, value)

def brightness(image, value):
    adjusted = image.astype(np.float32).copy()

    if adjusted.ndim == 2:
        return np.clip(adjusted + value, 0, 255).astype(np.uint8)

    if adjusted.ndim == 3 and adjusted.shape[2] >= 3:
        adjusted[..., :3] = np.clip(adjusted[..., :3] + value, 0, 255)

    return adjusted.astype(np.uint8)
