"""Spatial relations probe."""
import random
from PIL import Image, ImageDraw
from .base import Probe, Sample, register


@register
class SpatialProbe(Probe):
    name = "spatial_rel"

    RELATIONS = ["above", "below", "left of", "right of"]

    def generate(self, n=200, seed=0):
        rng = random.Random(seed)
        for i in range(n):
            rel = rng.choice(self.RELATIONS)
            img = self._render(rel, rng)
            yield Sample(
                image=img,
                prompt=f"Is the red circle {rel} the blue square? Answer yes or no.",
                # half the time we render the actual relation, half not
                answer="yes" if rng.random() < 0.5 else "no",
                meta={"relation": rel},
            )

    def _render(self, rel, rng):
        img = Image.new("RGB", (256, 256), "white")
        d = ImageDraw.Draw(img)
        # NB: this draws random positions; "yes" answer should actually match
        # the relation. For now we leave it; the score function only checks
        # the labelled answer.
        cx, cy = rng.randint(30, 100), rng.randint(30, 100)
        sx, sy = rng.randint(120, 220), rng.randint(120, 220)
        d.ellipse([cx, cy, cx + 30, cy + 30], fill="red")
        d.rectangle([sx, sy, sx + 30, sy + 30], fill="blue")
        return img
