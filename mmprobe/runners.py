"""Lightweight model runner wrappers."""
import torch
from PIL import Image


class HFModelRunner:
    """Wraps a Hugging Face VLM (LLaVA / Qwen-VL / etc.) behind a common API."""

    def __init__(self, model_id: str, device: str = "cuda", dtype=torch.float16):
        from transformers import AutoProcessor, AutoModelForCausalLM
        self.processor = AutoProcessor.from_pretrained(model_id)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id, torch_dtype=dtype
        ).to(device)
        self.device = device

    @torch.no_grad()
    def answer(self, image: Image.Image, prompt: str, max_new_tokens=32) -> str:
        inputs = self.processor(images=image, text=prompt, return_tensors="pt").to(self.device)
        out = self.model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False)
        return self.processor.batch_decode(out, skip_special_tokens=True)[0]
