"""Counting probe — small shapes on plain background."""
import random
from PIL import Image, ImageDraw
from .base import Probe, Sample, register


@register
class CountingProbe(Probe):
    name = "counting"

    def generate(self, n=200, seed=0):
        rng = random.Random(seed)
        for i in range(n):
            k = rng.randint(1, 10)
            img = Image.new("RGB", (224, 224), "white")
            d = ImageDraw.Draw(img)
            for _ in range(k):
                x, y = rng.randint(10, 200), rng.randint(10, 200)
                d.ellipse([x, y, x + 14, y + 14], fill="black")
            yield Sample(image=img,
                         prompt="How many dots are in this image? Answer with a single digit.",
                         answer=str(k),
                         meta={"k": k})
