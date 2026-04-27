model.eval()

PROMPTS = {
    "Hype": "omg",
    "Heartfelt": "i love this",
    "Casual": "this is",
    "Funny": "lol",
}

BAD_PREFIXES = [
    "caption:",
    "comment:",
    "image caption:",
    "generated comment:",
]

def clean_generated_comment(text, caption=""):
    text = str(text).strip()

    # remove prompt/caption if repeated
    if caption and caption.lower() in text.lower():
        text = text.replace(caption, "", 1).strip()

    # keep only after comment marker if present
    for marker in ["Comment:", "comment:"]:
        if marker in text:
            text = text.split(marker)[-1].strip()

    # remove junk words after generation
    junk_words = {"comment", "copy", "caption", "capt"}
    words = text.split()
    words = [w for w in words if w.lower().strip(":,.!?") not in junk_words]

    # stop if junk markers appear
    stop_tokens = ["Comment:", "comment:", "Copy", "copy", "Caption:", "caption:", "\n"]
    cleaned = []
    for word in words:
        if word in stop_tokens:
            break
        cleaned.append(word)

    text = " ".join(cleaned)

    # remove repeated triple words
    final_words = []
    for word in text.split():
        if len(final_words) >= 2 and word == final_words[-1] == final_words[-2]:
            continue
        final_words.append(word)

    text = " ".join(final_words).strip()

    # Instagram length
    text = " ".join(text.split()[:15])

    return text


def generate_comment(image, caption, tone="Hype", temperature=0.7):
    starter = PROMPTS[tone]

    # Here, caption can now be the Instagram comment dataset text.
    prompt = f"{caption} {starter}"

    inputs = processor(
        images=image,
        text=prompt,
        return_tensors="pt"
    ).to(DEVICE)

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=18,
            do_sample=True,
            temperature=temperature,
            top_p=0.9,
            repetition_penalty=1.3,
            no_repeat_ngram_size=3,
        )

    full_text = processor.tokenizer.decode(output[0], skip_special_tokens=True)
    comment = full_text.replace(prompt, "", 1).strip()
    comment = clean_generated_comment(comment, caption)

    if comment == "" or len(comment.split()) < 2:
        comment = f"{starter} this is so good"

    return comment