import numpy as np

def saturation(image, value):
    adjusted = image.astype(np.float32).copy()

    if adjusted.ndim == 3 and adjusted.shape[2] >= 3:
        channels = adjusted[..., :3]
        luminance = (
            0.299 * channels[..., 0]
            + 0.587 * channels[..., 1]
            + 0.114 * channels[..., 2]
        )
        factor = 1.0 + (value / 100.0)
        adjusted[..., :3] = np.clip(
            luminance[..., None] + factor * (channels - luminance[..., None]),
            0,
            255,
        )

    return adjusted.astype(np.uint8)