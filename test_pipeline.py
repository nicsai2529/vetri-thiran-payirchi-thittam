import sys
import os

# Ensure UTF-8 output encoding for console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

from app.gemini_flash import generate_outline
from app.gemini_pro import generate_story
from app.image_generator import generate_image
from app.layout_builder import build_comic_layout
from app.exporters import save_pdf

print("[*] Starting ComicCraft Verification Test...")

# 1. Test Outline Generation
prompt = "A brave fox named Free exploring an enchanted forest."
print("\n--- 1. Testing generate_outline() ---")
outline = generate_outline(prompt)
print(f"[OK] Generated {len(outline)} panels in outline.")
assert len(outline) == 5, "Expected 5 panels"

# 2. Test Story Generation
print("\n--- 2. Testing generate_story() ---")
story = generate_story(outline)
print("[OK] Generated story output snippet:")
print(story[:200] + "...\n")

# 3. Test Image Generation for first panel
print("\n--- 3. Testing generate_image() ---")
img_path = generate_image("Comic book panel of a brave fox in an enchanted forest", "test_panel_1.png")
print(f"[OK] Image generated at: {img_path}")
assert os.path.exists(img_path), "Generated image file does not exist!"

# 4. Test Layout Builder
print("\n--- 4. Testing build_comic_layout() ---")
images = [img_path] * 5
layout = build_comic_layout(images, story, outline)
print(f"[OK] Layout built with {len(layout)} panels.")
assert len(layout) == 5, "Expected 5 layout panels"

# 5. Test PDF Export
print("\n--- 5. Testing save_pdf() ---")
pdf_path = save_pdf(layout)
print(f"[OK] PDF generated at: {pdf_path}")
assert os.path.exists(pdf_path), "Generated PDF file does not exist!"

print("\n[SUCCESS] ALL 5 PIPELINE COMPONENTS TESTED & VERIFIED SUCCESSFULLY!")
