import re

def build_comic_layout(image_paths: list, full_story: str, outline: list) -> list:
    """
    Organizes generated images, story text, and outlines into a structured layout list.
    
    Args:
        image_paths (list): List of paths to generated panel images.
        full_story (str): Full story text with panel narrations and dialogues.
        outline (list): List of outline dictionaries from gemini_flash.
        
    Returns:
        list: Structured list of comic panel objects.
    """
    # Split the full story into individual panel segments
    # Common separators: **Panel 1: or Panel 1: or ## Panel 1
    raw_segments = re.split(r'(?i)(?=\*?\*?panel\s+\d+)', full_story)
    story_panels = [seg.strip() for seg in raw_segments if seg.strip()]

    # If splitting didn't yield enough segments, fallback to splitting by double newlines or outline count
    if len(story_panels) < len(outline):
        chunks = [c.strip() for c in full_story.split("\n\n") if c.strip()]
        if len(chunks) >= len(outline):
            story_panels = chunks[:len(outline)]
        else:
            # Duplicate or slice
            story_panels = (story_panels + [full_story] * len(outline))[:len(outline)]

    layout = []
    for idx, (image, text, panel_info) in enumerate(zip(image_paths, story_panels, outline), start=1):
        # Extract title from outline or text
        title = panel_info.get("title")
        if not title:
            first_line = text.split("\n")[0]
            clean_title = re.sub(r'^\*?\*?panel\s*\d*[:\- ]*', '', first_line, flags=re.IGNORECASE).replace('**', '').strip()
            title = clean_title if clean_title else f"Panel {idx}"
            
        # Clean text lines (remove repetitive panel header if desired)
        lines = text.splitlines()
        if lines and re.search(r'(?i)^(\*?\*?panel|\#\#\s*panel)', lines[0]):
            cleaned_text = "\n".join(lines[1:]).strip()
        else:
            cleaned_text = text.strip()

        # If empty text, use fallback
        if not cleaned_text:
            cleaned_text = panel_info.get("scene_description", "An unforgettable moment in the hero's journey.")

        layout.append({
            "panel": idx,
            "title": title,
            "image_path": image,
            "text": cleaned_text,
            "scene_description": panel_info.get("scene_description", ""),
            "image_prompt": panel_info.get("image_prompt", "")
        })

    return layout
