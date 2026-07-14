import unittest

import numpy as np

from numpy_processing.brightness import adjust_brightness, adjust_contrast, adjust_saturation


class ImageAdjustmentTests(unittest.TestCase):
    def test_adjust_brightness_increases_values(self):
        image = np.array([[[10, 20, 30], [40, 50, 60]]], dtype=np.uint8)
        adjusted = adjust_brightness(image, 20)

        self.assertTrue(np.all(adjusted[..., :3] >= image[..., :3]))

    def test_adjust_contrast_changes_values(self):
        image = np.array([[[64, 64, 64], [192, 192, 192]]], dtype=np.uint8)
        adjusted = adjust_contrast(image, 50)

        self.assertTrue(np.any(adjusted != image))

    def test_adjust_saturation_changes_colors(self):
        image = np.array([[[100, 50, 50], [200, 100, 100]]], dtype=np.uint8)
        adjusted = adjust_saturation(image, 50)

        self.assertTrue(np.any(adjusted != image))


if __name__ == "__main__":
    unittest.main()
