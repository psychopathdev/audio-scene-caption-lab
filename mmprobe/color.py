"""Color binding probe — which shape is RED?"""
import random
from PIL import Image, ImageDraw
from .base import Probe, Sample, register

COLORS = ["red", "blue", "green", "yellow", "purple"]
SHAPES = ["circle", "square", "triangle"]


@register
class ColorBindingProbe(Probe):
    name = "color_binding"

    def generate(self, n=200, seed=0):
        rng = random.Random(seed)
        for i in range(n):
            target_color = rng.choice(COLORS)
            target_shape = rng.choice(SHAPES)
            # other distractors with different (shape, color) combos
            distractors = []
            for _ in range(3):
                s = rng.choice([x for x in SHAPES if x != target_shape])
                c = rng.choice([x for x in COLORS if x != target_color])
                distractors.append((s, c))
            img = self._render(target_shape, target_color, distractors, rng)
            yield Sample(
                image=img,
                prompt=f"What shape is {target_color} in this image?",
                answer=target_shape,
                meta={"shape": target_shape, "color": target_color},
            )

    def _render(self, ts, tc, distractors, rng):
        img = Image.new("RGB", (256, 256), "white")
        d = ImageDraw.Draw(img)
        positions = [(40, 40), (140, 40), (40, 140), (140, 140)]
        rng.shuffle(positions)
        items = [(ts, tc)] + distractors
        for (shape, color), (x, y) in zip(items, positions):
            self._draw_shape(d, shape, color, x, y)
        return img

    @staticmethod
    def _draw_shape(d, shape, color, x, y):
        if shape == "circle":
            d.ellipse([x, y, x + 60, y + 60], fill=color)
        elif shape == "square":
            d.rectangle([x, y, x + 60, y + 60], fill=color)
        else:
            d.polygon([(x + 30, y), (x, y + 60), (x + 60, y + 60)], fill=color)
