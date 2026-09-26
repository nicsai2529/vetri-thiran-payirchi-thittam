import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL_PRO = os.getenv("MODEL_PRO", "gemini-1.5-pro")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


def get_mock_story(outline: list) -> str:
    """Fallback story generator for offline testing or when API key is missing."""
    story_parts = []
    for idx, panel in enumerate(outline, start=1):
        title = panel.get("title", f"Panel {idx}")
        desc = panel.get("scene_description", "")
        part = f"""**Panel {idx}: {title}**
**CAPTION:** {desc}
**NARRATION:** The air crackled with anticipation as the journey unfolded.
**DIALOGUE:** "We've made it this far—there is no turning back now!"
"""
        story_parts.append(part)
    return "\n\n".join(story_parts)


def generate_story(outline: list) -> str:
    """
    Generates a detailed comic story with narration and character dialogue
    from a list of comic panel outlines using Gemini 1.5 Pro.
    
    Args:
        outline (list): A list of dictionaries representing each comic panel's idea.
        
    Returns:
        str: The generated comic story text.
    """
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key or api_key.startswith("your_"):
        print("⚠️ GEMINI_API_KEY not configured. Using high-quality mock comic narration.")
        return get_mock_story(outline)

    # Format the panel outline as a numbered list for clarity
    formatted_outline = "\n".join([
        f"Panel {i+1}: {item.get('title', 'Scene')} - {item.get('scene_description', '')}"
        for i, item in enumerate(outline)
    ])

    prompt = f"""
You're a professional comic book writer.

Given the following panel breakdown, write a comic-style story with engaging narration and character dialogues for each panel.

Panel Outline:
{formatted_outline}

Guidelines:
- Use a fun, vivid, and engaging tone, like an actual comic book.
- Use explicit headers for each panel like: **Panel 1: Title**
- Include **CAPTION:** for ambient scene descriptions or environment sounds.
- Include **NARRATION:** and clearly marked character dialogue lines.
- Keep each panel self-contained but part of a cohesive story.
"""

    try:
        model = genai.GenerativeModel(MODEL_PRO)
        response = model.generate_content(prompt)
        print(f"\n📖 RAW GEMINI PRO RESPONSE:\n{response.text}\n")
        return response.text
    except Exception as e:
        print(f"❌ Error generating story with Gemini Pro: {e}")
        return get_mock_story(outline)
