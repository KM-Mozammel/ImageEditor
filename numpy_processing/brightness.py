import numpy as np


def increase(image, value):
    return adjust_brightness(image, value)


def adjust_brightness(image, value):
    adjusted = image.astype(np.float32).copy()

    if adjusted.ndim == 2:
        return np.clip(adjusted + value, 0, 255).astype(np.uint8)

    if adjusted.ndim == 3 and adjusted.shape[2] >= 3:
        adjusted[..., :3] = np.clip(adjusted[..., :3] + value, 0, 255)

    return adjusted.astype(np.uint8)


def adjust_contrast(image, value):
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


def adjust_saturation(image, value):
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