import image_engine_cpp


class ImageEngine:
    def __init__(self):
        self.pipeline = image_engine_cpp.Pipeline()

    def apply_adjustments(self, image, brightness=0, contrast=0, saturation=0):
        self.pipeline.clear()

        if brightness != 0:
            self.pipeline.add_brightness(brightness)
        if contrast != 0:
            self.pipeline.add_contrast(contrast)
        if saturation != 0:
            self.pipeline.add_saturation(saturation)

        result = image.copy()
        self.pipeline.render(result)
        return result
