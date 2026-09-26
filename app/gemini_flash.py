import os
import sys
import json
import re

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL_FLASH = os.getenv("MODEL_FLASH", "gemini-1.5-flash")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


def get_mock_outline(user_prompt: str) -> list:
    """Fallback generator for offline testing or when API key is missing."""
    prompt_snippet = user_prompt.strip() or "An exciting heroic adventure"
    return [
        {
            "panel": 1,
            "title": "The Beginning of the Journey",
            "scene_description": f"The story begins with our hero stepping into the realm. Prompt inspiration: {prompt_snippet}",
            "image_prompt": f"Comic book art, introducing main hero, wide establishing shot, vibrant comic colors, dramatic lighting, detailed background: {prompt_snippet}"
        },
        {
            "panel": 2,
            "title": "Into the Unknown",
            "scene_description": "Venturing deeper into uncharted territory, strange sights and unexpected obstacles emerge.",
            "image_prompt": "Comic book panel, hero moving carefully through mystical surroundings, suspenseful atmosphere, sharp ink lines, retro comic style"
        },
        {
            "panel": 3,
            "title": "The Rising Conflict",
            "scene_description": "A sudden discovery triggers a confrontation, raising the stakes high.",
            "image_prompt": "Dynamic action comic panel, intense confrontation, high angle shot, colorful energy bursts, dynamic comic book shading"
        },
        {
            "panel": 4,
            "title": "The Turning Point",
            "scene_description": "Through bravery and quick wit, the hero finds the key to overcoming the challenge.",
            "image_prompt": "Heroic close-up panel, glowing magical power, triumphant expression, speedlines, bold comic ink outlines"
        },
        {
            "panel": 5,
            "title": "A New Dawn",
            "scene_description": "The dust settles as peace is restored and a new legend is born.",
            "image_prompt": "Inspiring comic panel, hero looking at the sunrise horizon, cinematic wide angle, epic comic masterpiece"
        }
    ]


def generate_outline(user_prompt: str) -> list:
    """
    Generates a 5-panel comic layout based on the user's story prompt using Gemini Flash.
    
    Args:
        user_prompt (str): The user's comic idea prompt.
        
    Returns:
        list: A list of dictionaries, one for each panel.
    """
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key or api_key.startswith("your_"):
        print("⚠️ GEMINI_API_KEY not configured. Using high-quality mock outline.")
        return get_mock_outline(user_prompt)

    prompt = f"""
You are a professional AI comic planner.

Your task is to generate a *strictly formatted* JSON array containing 5 panel descriptions for a comic based on the story idea below:

STORY: "{user_prompt}"

Each JSON object must include:
- "panel" (integer)
- "title" (string)
- "scene_description" (string)
- "image_prompt" (string, detailed comic illustration prompt for image generation)

Respond ONLY in this valid JSON format, without any explanations or markdown:
[
  {{
    "panel": 1,
    "title": "Title here",
    "scene_description": "Scene description here",
    "image_prompt": "Detailed comic style image prompt"
  }}
]
"""
    try:
        model = genai.GenerativeModel(MODEL_FLASH)
        response = model.generate_content(prompt)
        output_text = response.text.strip()
        print(f"\n✨ RAW GEMINI FLASH RESPONSE:\n{output_text}\n")

        # Remove any markdown formatting if present
        cleaned_text = output_text
        if "```json" in cleaned_text:
            cleaned_text = cleaned_text.split("```json")[1].split("```")[0].strip()
        elif "```" in cleaned_text:
            cleaned_text = cleaned_text.split("```")[1].split("```")[0].strip()

        # Find JSON array
        match = re.search(r'\[.*\]', cleaned_text, re.DOTALL)
        if match:
            panel_data = json.loads(match.group(0))
        else:
            panel_data = json.loads(cleaned_text)

        # Structure validation
        if not isinstance(panel_data, list):
            raise ValueError("Gemini response is not a list.")

        required_keys = {"panel", "title", "scene_description", "image_prompt"}
        for panel in panel_data:
            if not isinstance(panel, dict) or not required_keys.issubset(panel.keys()):
                raise ValueError(f"Invalid panel format or missing keys: {panel}")

        return panel_data

    except json.JSONDecodeError as e:
        print(f"❌ JSON Decode Error: {e}")
        print(f"❌ Full Text Received:\n{output_text if 'output_text' in locals() else 'None'}")
        return get_mock_outline(user_prompt)
    except Exception as e:
        print(f"❌ Unexpected Error in generate_outline: {e}")
        return get_mock_outline(user_prompt)
