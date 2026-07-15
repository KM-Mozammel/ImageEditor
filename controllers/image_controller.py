from engine.image_engine import ImageEngine

from image_manager.state import ImageState
from image_manager.loader import open_image
from image_manager.saver import save_image


class ImageController:

    def __init__(self):
        self.state = ImageState()
        self.engine = ImageEngine()

    @property
    def current_image(self):
        return self.state.current

    def load_image(self, path):

        image = open_image(path)

        self.state.original = image
        self.state.current = image.copy()

    def apply_adjustments(
        self,
        brightness,
        contrast,
        saturation,
    ):

        if self.state.original is None:
            return

        self.state.current = self.engine.apply_adjustments(
            image=self.state.original,
            brightness=brightness,
            contrast=contrast,
            saturation=saturation,
        )

    def reset(self):

        if self.state.original is not None:
            self.state.current = self.state.original.copy()

    def save(self, path):

        save_image(
            self.state.current,
            path,
        )