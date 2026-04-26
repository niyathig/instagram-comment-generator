import pandas as pd
import time
import os

# Import your model function
from BLIP2_inference import generate_comment

# ====== CONFIG ======
DATA_PATH = "data/dataset.csv"   # CHANGE THIS if needed
OUTPUT_PATH = "docs/eval_50_results.csv"

# ====== LOAD DATA ======
df = pd.read_csv(DATA_PATH)

# Make sure these columns exist
# REQUIRED: image_path, caption
# OPTIONAL: comment (ground truth)

df_50 = df.head(50)

results = []

# ====== METRICS ======
def word_overlap(pred, ref):
    if pd.isna(ref):
        return 0

    p = set(str(pred).lower().split())
    r = set(str(ref).lower().split())

    if len(r) == 0:
        return 0

    return len(p & r) / len(r)


def quality_score(text):
    text = str(text).lower().strip()
    words = text.split()

    score = 0

    if 2 <= len(words) <= 15:
        score += 1

    if text not in ["cute", "nice", "love this", "so pretty"]:
        score += 1

    if any(x in text for x in ["!", "🔥", "😍", "❤️", "✨"]):
        score += 1

    return score / 3


# ====== GENERATION LOOP ======
for i, row in df_50.iterrows():
    print(f"Processing {i+1}/50")

    image_path = row["image_path"]
    caption = row["caption"]
    reference = row.get("comment", "")

    start = time.time()

    try:
        generated = generate_comment(image_path, caption)
        error = ""
    except Exception as e:
        generated = ""
        error = str(e)

    latency = time.time() - start

    results.append({
        "index": i,
        "image_path": image_path,
        "caption": caption,
        "reference_comment": reference,
        "generated_comment": generated,
        "latency_sec": latency,
        "overlap_score": word_overlap(generated, reference),
        "quality_score": quality_score(generated),
        "error": error
    })

# ====== SAVE RESULTS ======
os.makedirs("docs", exist_ok=True)

results_df = pd.DataFrame(results)
results_df.to_csv(OUTPUT_PATH, index=False)

print("\n✅ DONE")
print(f"Saved to {OUTPUT_PATH}")

print("\nAverages:")
print("Latency:", results_df["latency_sec"].mean())
print("Overlap:", results_df["overlap_score"].mean())
print("Quality:", results_df["quality_score"].mean())