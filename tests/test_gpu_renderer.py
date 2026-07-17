import unittest
import numpy as np

from engine.image_engine import ImageEngine
from rendering.opengl_renderer import OpenGLRenderer


class OpenGLRendererTests(unittest.TestCase):
    def test_engine_falls_back_when_native_extension_is_unavailable(self):
        engine = ImageEngine()
        img = np.zeros((4, 4, 3), dtype=np.uint8)
        result = engine.apply_adjustments(img, brightness=10, contrast=10, saturation=10)
        self.assertEqual(result.shape, img.shape)
        self.assertEqual(result.dtype, np.uint8)

    def test_renderer_reports_support_status(self):
        renderer = OpenGLRenderer()
        self.assertIsInstance(renderer.is_supported(), bool)


if __name__ == "__main__":
    unittest.main()
