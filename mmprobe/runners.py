"""Model runner wrappers — local HF and remote OpenAI-compatible."""
from typing import Optional
import torch
from PIL import Image


class HFModelRunner:
    """Wraps a Hugging Face VLM behind a common API."""

    def __init__(self, model_id: str, device: str = "cuda", dtype=torch.float16):
        from transformers import AutoProcessor, AutoModelForCausalLM
        self.model_id = model_id
        self.processor = AutoProcessor.from_pretrained(model_id)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id, torch_dtype=dtype, device_map=device
        )
        self.device = device

    @torch.no_grad()
    def answer(self, image: Image.Image, prompt: str, max_new_tokens=32) -> str:
        # NB: this assumes a chat-template-compatible processor; older
        # LLaVA checkpoints need a different prompt format
        messages = [{"role": "user", "content": [{"type": "image"},
                                                  {"type": "text", "text": prompt}]}]
        text = self.processor.apply_chat_template(messages, add_generation_prompt=True)
        inputs = self.processor(images=image, text=text, return_tensors="pt").to(self.device)
        out = self.model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False)
        # strip the prompt from the decoded output
        decoded = self.processor.batch_decode(out, skip_special_tokens=True)[0]
        return decoded[len(text):].strip() if decoded.startswith(text) else decoded


class OpenAIRunner:
    """For gpt-4o-style endpoints. Lazy import."""

    def __init__(self, model: str = "gpt-4o-mini", api_key: Optional[str] = None):
        import openai
        self.model = model
        self.client = openai.OpenAI(api_key=api_key)

    def answer(self, image, prompt, max_new_tokens=32):
        import base64, io
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        data_url = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": data_url}},
            ]}],
            max_tokens=max_new_tokens,
        )
        return resp.choices[0].message.content
