"""Size compare — which of two circles is larger?"""
import random
from PIL import Image, ImageDraw
from .base import Probe, Sample, register


@register
class SizeCompareProbe(Probe):
    name = "size_compare"

    def generate(self, n=200, seed=0):
        rng = random.Random(seed)
        for _ in range(n):
            r1 = rng.randint(15, 50)
            r2 = rng.randint(15, 50)
            while abs(r1 - r2) < 10:
                r2 = rng.randint(15, 50)
            img = Image.new("RGB", (256, 128), "white")
            d = ImageDraw.Draw(img)
            d.ellipse([30, 64 - r1, 30 + 2*r1, 64 + r1], fill="red")
            d.ellipse([180, 64 - r2, 180 + 2*r2, 64 + r2], fill="blue")
            answer = "red" if r1 > r2 else "blue"
            yield Sample(
                image=img,
                prompt="Which circle is larger, red or blue? Answer with just the color.",
                answer=answer,
                meta={"r1": r1, "r2": r2},
            )
