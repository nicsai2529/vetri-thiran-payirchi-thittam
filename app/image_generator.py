import os
import re
import time
import urllib.parse
import requests
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv

load_dotenv()

# Directories
STATIC_DIR = os.path.join(os.getcwd(), "static")
PANELS_DIR = os.path.join(STATIC_DIR, "panels")
os.makedirs(PANELS_DIR, exist_ok=True)

HF_API_KEY = os.getenv("HF_API_KEY", "")
SD_MODEL = os.getenv("SD_MODEL", "runwayml/stable-diffusion-v1-5")

# Optional Diffusers pipeline if installed and CUDA is available
pipe = None
try:
    import torch
    from diffusers import StableDiffusionPipeline
    if torch.cuda.is_available():
        print("⚡ CUDA available. Loading Stable Diffusion pipeline...")
        pipe = StableDiffusionPipeline.from_pretrained(SD_MODEL, torch_dtype=torch.float16)
        pipe = pipe.to("cuda")
except Exception as e:
    pipe = None


def sanitize_filename(prompt: str) -> str:
    """Sanitizes a prompt string into a safe file name."""
    clean = re.sub(r'[^a-zA-Z0-9_\- ]', '', prompt)
    clean = clean.strip().replace(' ', '_')[:40]
    timestamp = int(time.time() * 1000)
    return f"panel_{clean}_{timestamp}.png" if clean else f"panel_{timestamp}.png"


def create_fallback_comic_panel(prompt: str, output_path: str):
    """Creates a stylized comic placeholder image using PIL when offline."""
    width, height = 768, 512
    # Create comic style gradient background
    img = Image.new("RGB", (width, height), color=(26, 26, 46))
    draw = ImageDraw.Draw(img)

    # Draw comic border and dot pattern
    border_margin = 12
    draw.rectangle([border_margin, border_margin, width - border_margin, height - border_margin],
                   outline=(245, 197, 24), width=4)

    # Draw halftone/accent shapes
    draw.polygon([(0, 0), (width, 0), (0, height // 2)], fill=(22, 33, 62))
    draw.polygon([(width, height), (0, height), (width, height // 2)], fill=(15, 52, 96))

    # Inner comic frame
    inner_margin = 24
    draw.rectangle([inner_margin, inner_margin, width - inner_margin, height - inner_margin],
                   outline=(233, 69, 96), width=2)

    # Text rendering
    title_text = "COMICCRAFT AI PANEL"
    prompt_snippet = (prompt[:140] + '...') if len(prompt) > 140 else prompt

    # Standard PIL default font
    draw.text((width // 2 - 120, height // 2 - 40), title_text, fill=(255, 222, 89))
    draw.text((60, height // 2 + 10), f"Prompt: {prompt_snippet}", fill=(230, 230, 230))
    draw.text((width // 2 - 80, height - 50), "★ Comic Art Scene ★", fill=(100, 200, 255))

    img.save(output_path, "PNG")


def generate_image(prompt: str, filename: str = None) -> str:
    """
    Generates a comic-style image based on the prompt.
    Saves the image into static/panels/ and returns the relative file path.
    """
    if not filename:
        filename = sanitize_filename(prompt)
    
    if not filename.endswith((".png", ".jpg", ".jpeg")):
        filename += ".png"

    output_path = os.path.join(PANELS_DIR, filename)

    # 1. Try local Diffusers pipeline if available
    if pipe is not None:
        try:
            print(f"🎨 Generating image via local Stable Diffusion for: {prompt[:40]}...")
            image = pipe(prompt).images[0]
            image.save(output_path)
            return f"static/panels/{filename}"
        except Exception as e:
            print(f"⚠️ Local Diffusers failed: {e}. Falling back to online generation...")

    # 2. Try Pollinations / AI Image Generation API (Free, high-speed, direct image return)
    try:
        encoded_prompt = urllib.parse.quote(f"comic book style illustration, vibrant comic art, graphic novel panel: {prompt}")
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=768&height=512&nologo=true&enhance=true"
        print(f"🎨 Fetching AI illustration from: {url[:70]}...")
        
        response = requests.get(url, timeout=20)
        if response.status_code == 200 and len(response.content) > 1000:
            with open(output_path, "wb") as f:
                f.write(response.content)
            print(f"✅ Comic panel saved to {output_path}")
            return f"static/panels/{filename}"
    except Exception as e:
        print(f"⚠️ Online image API request failed: {e}")

    # 3. Fallback to stylized PIL graphic
    create_fallback_comic_panel(prompt, output_path)
    print(f"✅ Fallback panel generated at {output_path}")
    return f"static/panels/{filename}"
