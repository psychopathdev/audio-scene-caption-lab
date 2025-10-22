"""Negation probe — model has to pay attention to 'no'."""
import random
from .presence import PresenceProbe
from .base import Sample, register


@register
class NegationProbe(PresenceProbe):
    name = "negation"

    def generate(self, n=200, seed=0):
        for s in super().generate(n=n, seed=seed):
            target = s.meta["target"]
            # flip prompt and answer
            new_prompt = f"Is there NO {target} in the image? Answer yes or no."
            new_answer = "yes" if not s.meta["present"] else "no"
            yield Sample(image=s.image, prompt=new_prompt,
                         answer=new_answer, meta=s.meta)
