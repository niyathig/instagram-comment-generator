import gradio as gr
from BLIP2_inference import generate_comment

def predict(image, caption, tone):
    if image is None:
        return "Please upload an image."

    if caption is None or caption.strip() == "":
        caption = "Instagram post"

    try:
        comment = generate_comment(
            image_path=image,
            caption=caption,
            tone=tone
        )
        return comment
    except Exception as e:
        return f"Error: {e}"

demo = gr.Interface(
    fn=predict,
    inputs=[
        gr.Image(type="filepath", label="Upload Instagram Image"),
        gr.Textbox(
            label="Caption",
            placeholder="Enter the Instagram caption here...",
            lines=2
        ),
        gr.Dropdown(
            choices=["classic", "hype", "funny", "heartfelt"],
            value="classic",
            label="Comment Tone"
        )
    ],
    outputs=gr.Textbox(label="Generated Comment"),
    title="Instagram Comment Generator",
    description="Upload an image, add a caption, choose a tone, and generate an Instagram-style comment.",
    examples=[
        ["data/test.jpg", "sunset vibes", "classic"],
        ["data/test.jpg", "beach day", "hype"],
        ["data/test.jpg", "coffee time", "heartfelt"]
    ],
)

if __name__ == "__main__":
    demo.launch()