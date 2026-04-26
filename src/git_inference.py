import torch
from PIL import Image
from transformers import AutoProcessor, AutoModelForCausalLM

# =====================
# LOAD MODEL (GIT)
# =====================

MODEL_ID = "microsoft/git-base"

processor = AutoProcessor.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(MODEL_ID)

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
model.to(DEVICE)
model.eval()

# =====================
# PROMPTS
# =====================

PROMPTS = {
    "Hype": "Caption: {caption} Comment: omg",
    "Heartfelt": "Caption: {caption} Comment: i love",
    "Casual": "Caption: {caption} Comment: this is",
    "Funny": "Caption: {caption} Comment: lol",
}

# =====================
# MAIN FUNCTION
# =====================

def generate_comment(image, caption, tone="Casual", temperature=0.9):
    prompt = PROMPTS[tone].format(caption=caption)

    inputs = processor(
        images=image,
        text=prompt,
        return_tensors="pt"
    ).to(DEVICE)

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=40,
            do_sample=True,
            temperature=temperature,
            top_p=0.95
        )

    full_text = processor.tokenizer.decode(output[0], skip_special_tokens=True)
    comment = full_text.split("Comment:")[-1].strip()

    return comment