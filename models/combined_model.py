def generate_comment_chained(image, caption, tone):
    """
    Stage 1: GIT takes image + caption → generates enriched caption
    Stage 2: GPT-2 takes enriched caption → generates comment
    """
    # Stage 1 — GIT generates caption from image
    inputs = processor(
        images=image,
        text=caption,          # pass caption as context
        return_tensors="pt"
    ).to(DEVICE)

    with torch.no_grad():
        out = model.generate(
            **inputs,
            max_new_tokens=20,
            do_sample=False,
            repetition_penalty=1.5,
            no_repeat_ngram_size=3
        )

    git_caption = processor.tokenizer.decode(out[0], skip_special_tokens=True)

    # Stage 2 — GPT-2 generates comment from GIT caption
    tone_starters = {
        "Compliment": "you are",
        "Reflective": "i",
        "Casual":     "this is",
        "Funny":      "lol"
    }
    prompt = f"Caption: {git_caption} Comment: {tone_starters[tone]}"
    inputs = gpt2_tokenizer(prompt, return_tensors="pt").to(DEVICE)

    with torch.no_grad():
        out = gpt2_model.generate(
            **inputs,
            max_new_tokens=30,
            do_sample=True,
            temperature=0.9,
            top_p=0.95,
            no_repeat_ngram_size=3,
            pad_token_id=gpt2_tokenizer.eos_token_id
        )

    full_text = gpt2_tokenizer.decode(out[0], skip_special_tokens=True)
    comment   = full_text.split("Comment:")[-1].strip()
    return git_caption, comment