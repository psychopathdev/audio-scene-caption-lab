"""Presence probe — is object X in the image? yes/no."""
import random
from PIL import Image, ImageDraw
from .base import Probe, Sample, register


@register
class PresenceProbe(Probe):
    name = "presence"

    SHAPES = ["circle", "square", "triangle", "star"]

    def generate(self, n=200, seed=0):
        rng = random.Random(seed)
        for _ in range(n):
            target = rng.choice(self.SHAPES)
            present = rng.random() < 0.5
            shapes_in_img = []
            if present:
                shapes_in_img.append(target)
            # fill with non-targets
            others = [s for s in self.SHAPES if s != target]
            shapes_in_img.extend(rng.sample(others, k=rng.randint(1, 2)))
            img = self._render(shapes_in_img, rng)
            yield Sample(
                image=img,
                prompt=f"Is there a {target} in the image? Answer yes or no.",
                answer="yes" if present else "no",
                meta={"target": target, "present": present},
            )

    def _render(self, shapes, rng):
        img = Image.new("RGB", (256, 256), "white")
        d = ImageDraw.Draw(img)
        for shape in shapes:
            x, y = rng.randint(20, 200), rng.randint(20, 200)
            self._draw(d, shape, x, y)
        return img

    @staticmethod
    def _draw(d, shape, x, y, c="black"):
        if shape == "circle":
            d.ellipse([x, y, x + 40, y + 40], outline=c, width=2)
        elif shape == "square":
            d.rectangle([x, y, x + 40, y + 40], outline=c, width=2)
        elif shape == "triangle":
            d.polygon([(x + 20, y), (x, y + 40), (x + 40, y + 40)], outline=c)
        else:  # star — lazy approximation
            d.polygon([(x + 20, y), (x + 25, y + 15), (x + 40, y + 15),
                       (x + 28, y + 25), (x + 33, y + 40), (x + 20, y + 30),
                       (x + 7, y + 40), (x + 12, y + 25), (x, y + 15),
                       (x + 15, y + 15)], outline=c)
