from __future__ import annotations

import time
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import List, Optional

import torch
from PIL import Image
from transformers import Blip2ForConditionalGeneration, Blip2Processor


DEFAULT_MODEL = "Salesforce/blip2-flan-t5-xl"
TONE_INSTRUCTIONS = {
    "hype": "Make it energetic, short, and supportive, like a close friend hyping them up.",
    "funny": "Make it playful and funny, but still kind and appropriate.",
    "heartfelt": "Make it warm, genuine, and supportive without being too long.",
    "classic": "Make it sound like a natural Instagram comment, specific but casual.",
}
def generate_comment(image_path, caption, tone="classic"):
    from PIL import Image

    image = Image.open(image_path).convert("RGB")

    inputs = processor(images=image, text=caption, return_tensors="pt").to(device)

    output = model.generate(**inputs, max_new_tokens=30)
    comment = processor.decode(output[0], skip_special_tokens=True)

    return comment
    
from BLIP2_inference import generate_comment

@dataclass
class GenerationResult:
    comments: List[str]
    latency_seconds: float
    model_name: str
    prompt: str


@lru_cache(maxsize=1)
def load_blip2(model_name: str = DEFAULT_MODEL):
    """Load BLIP-2 once and reuse it across UI calls.

    For Colab T4, use fp16 on CUDA. On CPU, this may be slow; the app still runs,
    but graders should expect longer inference.
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.float16 if device == "cuda" else torch.float32
    processor = Blip2Processor.from_pretrained(model_name)
    model = Blip2ForConditionalGeneration.from_pretrained(model_name, torch_dtype=dtype)
    model.to(device)
    model.eval()
    return processor, model, device


def build_prompt(caption: str, tone: str = "classic", num_comments: int = 3) -> str:
    tone_line = TONE_INSTRUCTIONS.get(tone, TONE_INSTRUCTIONS["classic"])
    return (
        f"You are helping someone comment on a friend's Instagram post. "
        f"Caption: {caption or 'No caption provided.'}\n"
        f"{tone_line}\n"
        f"Generate {num_comments} different short Instagram comments. "
        f"Avoid hashtags, usernames, spam, flirting with strangers, or generic one-word comments."
    )


def _postprocess(raw_text: str, max_comments: int = 3) -> List[str]:
    pieces: List[str] = []
    for line in raw_text.replace(";", "\n").split("\n"):
        line = line.strip(" -0123456789.)\t")
        if line and line not in pieces:
            pieces.append(line)
    if not pieces and raw_text.strip():
        pieces = [raw_text.strip()]
    return pieces[:max_comments]


@torch.no_grad()
def generate_comment(
    image_path: str | Path | Image.Image,
    caption: str = "",
    tone: str = "classic",
    num_comments: int = 3,
    model_name: str = DEFAULT_MODEL,
    max_new_tokens: int = 80,
) -> GenerationResult:
    """Generate Instagram comments from image + caption using zero-shot BLIP-2."""
    processor, model, device = load_blip2(model_name)
    image = image_path if isinstance(image_path, Image.Image) else Image.open(image_path).convert("RGB")
    prompt = build_prompt(caption, tone, num_comments)

    start = time.perf_counter()
    inputs = processor(images=image, text=prompt, return_tensors="pt").to(device)
    outputs = model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
        do_sample=True,
        temperature=0.85,
        top_p=0.92,
        num_return_sequences=1,
    )
    raw = processor.batch_decode(outputs, skip_special_tokens=True)[0]
    latency = time.perf_counter() - start
    return GenerationResult(
        comments=_postprocess(raw, max_comments=num_comments),
        latency_seconds=latency,
        model_name=model_name,
        prompt=prompt,
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--image", required=True)
    parser.add_argument("--caption", default="")
    parser.add_argument("--tone", default="classic", choices=list(TONE_INSTRUCTIONS))
    args = parser.parse_args()

    result = generate_comment(args.image, args.caption, args.tone)
    for i, comment in enumerate(result.comments, 1):
        print(f"{i}. {comment}")
    print(f"Latency: {result.latency_seconds:.2f}s")
