import numpy as np

def contrast(image, value):
    adjusted = image.astype(np.float32).copy()

    if adjusted.ndim == 2:
        return np.clip(adjusted, 0, 255).astype(np.uint8)

    if adjusted.ndim == 3 and adjusted.shape[2] >= 3:
        channels = adjusted[..., :3]
        if value == 0:
            return adjusted.astype(np.uint8)

        factor = 1.0 + (value / 100.0)
        adjusted[..., :3] = np.clip((channels - 128.0) * factor + 128.0, 0, 255)

    return adjusted.astype(np.uint8)