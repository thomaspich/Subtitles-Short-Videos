from moviepy.video.VideoClip import TextClip as BaseTextClip
from PIL import Image, ImageDraw
import numpy as np


class TextClip(BaseTextClip):
    def __init__(self, corner_radius=0, padding=(0, 0, 0, 0), *args, **kwargs):
        self.corner_radius = corner_radius
        self.padding = self._normalize_padding(padding)
        self.bg_color = kwargs.get("bg_color", None)
        super().__init__(*args, **kwargs)

        if self.corner_radius > 0 or any(self.padding):
            self._apply_rounded_background_with_padding()

    def _normalize_padding(self, padding):
        if isinstance(padding, (int, float)):
            return (padding, padding, padding, padding)
        elif len(padding) == 2:
            h, v = padding
            return (h, v, h, v)
        elif len(padding) == 4:
            return padding
        else:
            raise ValueError("Padding must be an int, a tuple of 2 or 4 elements.")

    def _apply_rounded_background_with_padding(self):
        original_img = Image.fromarray(self.img)
        orig_width, orig_height = original_img.size

        # Calculate new size with padding
        left, top, right, bottom = self.padding
        new_width = orig_width + left + right
        new_height = orig_height + top + bottom

        # Create new image with transparent background
        # Créer fond avec coins arrondis
        bg = Image.new("RGBA", (new_width, new_height), (0, 0, 0, 0))

        draw = ImageDraw.Draw(bg)
        draw.rounded_rectangle(
            [0, 0, new_width, new_height],
            radius=self.corner_radius,
            fill=self.bg_color
        )

        # Isoler le canal alpha comme masque
        if original_img.mode != "RGBA":
            original_img = original_img.convert("RGBA")
        mask = original_img.split()[3]  # canal alpha

        # Coller le texte dans le fond arrondi avec masque alpha
        bg.paste(original_img, (left, top), mask=mask)

        # Remplacer l'image clip
        self.img = np.array(bg)