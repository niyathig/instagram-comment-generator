# Load GPT-2
gpt2_tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
gpt2_tokenizer.pad_token = gpt2_tokenizer.eos_token
gpt2_model = GPT2LMHeadModel.from_pretrained("gpt2").to(DEVICE)

# Dataset
class CommentDataset(Dataset):
    def __init__(self, comments, tokenizer, max_length=64):
        self.examples = []
        for comment in comments:
            enc = tokenizer(
                f"Comment: {comment}{tokenizer.eos_token}",
                truncation=True,
                max_length=max_length,
                padding="max_length",
                return_tensors="pt"
            )
            self.examples.append({
                "input_ids": enc["input_ids"].squeeze(),
                "attention_mask": enc["attention_mask"].squeeze(),
                "labels": enc["input_ids"].squeeze()
            })

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, idx):
        return self.examples[idx]

comment_dataset = CommentDataset(comments, gpt2_tokenizer)
comment_loader  = DataLoader(comment_dataset, batch_size=8, shuffle=True)
print(f"Dataset size: {len(comment_dataset)}")


#Fine-Tune GPT2
import matplotlib.pyplot as plt
from torch.optim import AdamW

gpt2_optimizer = AdamW(gpt2_model.parameters(), lr=5e-5)
gpt2_epoch_numbers = []
gpt2_epoch_losses  = []

EPOCHS = 5
for epoch in range(EPOCHS):
    total_loss = 0
    for batch in comment_loader:
        batch  = {k: v.to(DEVICE) for k, v in batch.items()}
        output = gpt2_model(**batch)
        loss   = output.loss
        gpt2_optimizer.zero_grad()
        loss.backward()
        gpt2_optimizer.step()
        total_loss += loss.item()

    avg = total_loss / len(comment_loader)
    gpt2_epoch_numbers.append(epoch + 1)
    gpt2_epoch_losses.append(avg)
    print(f"Epoch {epoch+1}/{EPOCHS} — loss: {avg:.4f}")