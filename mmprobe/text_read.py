"""Synthetic OCR probe — single-word read."""
import random
from PIL import Image, ImageDraw, ImageFont
from .base import Probe, Sample, register

WORDS = ["cat", "dog", "house", "tree", "bird", "lake", "moon", "fire", "sun", "snow"]


@register
class TextReadProbe(Probe):
    name = "text_read"

    def generate(self, n=200, seed=0):
        rng = random.Random(seed)
        for _ in range(n):
            word = rng.choice(WORDS)
            img = Image.new("RGB", (256, 96), "white")
            d = ImageDraw.Draw(img)
            # default font is small — that's actually a good stressor
            d.text((20, 30), word, fill="black")
            yield Sample(
                image=img,
                prompt="What single word is written in the image?",
                answer=word,
                meta={"word": word},
            )
