"""Temporal ordering — 2-frame side-by-side."""
import random
from PIL import Image, ImageDraw
from .base import Probe, Sample, register


@register
class TemporalOrderProbe(Probe):
    name = "temporal_order"

    def generate(self, n=200, seed=0):
        rng = random.Random(seed)
        for _ in range(n):
            # left frame: small circle; right frame: big circle
            # "which happened first" — depends on the labeling we choose
            left_first = rng.random() < 0.5
            img = Image.new("RGB", (320, 160), "white")
            d = ImageDraw.Draw(img)
            r_small, r_big = 15, 50
            r_left = r_small if left_first else r_big
            r_right = r_big if left_first else r_small
            d.ellipse([80 - r_left, 80 - r_left, 80 + r_left, 80 + r_left], fill="black")
            d.ellipse([240 - r_right, 80 - r_right, 240 + r_right, 80 + r_right], fill="black")
            # label below frames
            d.text((70, 140), "frame 1", fill="black")
            d.text((230, 140), "frame 2", fill="black")
            yield Sample(
                image=img,
                prompt="Looking at the two frames left-to-right, did the circle grow or shrink?",
                answer="grow" if left_first else "shrink",
                meta={"order": "grow" if left_first else "shrink"},
            )
