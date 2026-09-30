# Solution Architecture

| Field | Details |
|---|---|
| Team ID | SWTID-2026-7634 |
| Project Name | ComicCraft: AI Comic Creation Assistant |
| Team Leader | C Nithya Shree |

## Architecture Flow

```
[User] -> [Streamlit Frontend] -> [Python Backend]
                                     |-> [Content Safety Check]
                                     |-> [Gemini API: script and dialogue]
                                     |-> [Text-to-Image API: panel artwork]
                                     |-> [Pillow: layout and speech bubbles]
[Backend] -> [Finished comic: PDF / PNG] -> [User]
```

## Components

| Component | Responsibility |
|---|---|
| Frontend | Collects the story idea and shows script, panels and final comic |
| Backend | Coordinates script, artwork and layout steps |
| Content Safety Check | Rejects unsafe or inappropriate prompts |
| Gemini API | Generates characters, scenes and dialogue |
| Text-to-Image API | Creates artwork for each panel |
| Layout Engine | Places panels and speech bubbles and prepares export |
