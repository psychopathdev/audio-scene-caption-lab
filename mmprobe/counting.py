"""Counting probe with controlled clutter."""
import random
from PIL import Image, ImageDraw
from .base import Probe, Sample, register


@register
class CountingProbe(Probe):
    """Counts of 1-10 black dots on white background, optional distractors."""

    name = "counting"

    SHAPES = ("dot", "square")

    def generate(self, n=200, seed=0):
        rng = random.Random(seed)
        for i in range(n):
            k = rng.randint(1, 10)
            clutter = rng.choice([0, 0, 2, 5])  # heavy bias toward no clutter
            img = Image.new("RGB", (256, 256), "white")
            d = ImageDraw.Draw(img)
            self._draw_shapes(d, k, "dot", "black", rng)
            if clutter:
                self._draw_shapes(d, clutter, "square", "gray", rng)
            yield Sample(
                image=img,
                prompt="How many black dots are in this image? "
                       "Answer with a single digit.",
                answer=str(k),
                meta={"k": k, "clutter": clutter},
            )

    @staticmethod
    def _draw_shapes(d, n, shape, color, rng):
        for _ in range(n):
            x, y = rng.randint(10, 230), rng.randint(10, 230)
            if shape == "dot":
                d.ellipse([x, y, x + 14, y + 14], fill=color)
            else:
                d.rectangle([x, y, x + 14, y + 14], fill=color)

    def score(self, sample, model_answer):
        ans = (model_answer or "").strip()
        # try to extract a leading digit/number from the model's reply
        import re
        m = re.search(r"\d+", ans)
        if not m:
            return False
        return int(m.group()) == sample.meta["k"]
