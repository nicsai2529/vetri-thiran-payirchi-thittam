# Data Flow Diagram & User Stories

| Field | Details |
|---|---|
| Team ID | SWTID-2026-7634 |
| Project Name | ComicCraft: AI Comic Creation Assistant |
| Team Leader | C Nithya Shree |

## Data Flow (Level 0)

```
User -> Story idea, genre, art style, number of panels
     -> Content safety check
     -> LLM: characters, scenes and dialogue per panel (script)
     -> User reviews and edits script
     -> Text-to-image model: artwork for each panel
     -> Layout engine: panels + speech bubbles
     -> Finished comic (PDF / PNG) -> User
```

## User Stories

| User Type | Story No. | User Story | Acceptance Criteria | Priority |
|---|---|---|---|---|
| Customer | USN-1 | As a user, I can enter a story idea and choose an art style | Input is accepted and saved | High |
| Customer | USN-2 | As a user, I want a panel-wise script generated | Script shows scene and dialogue for each panel | High |
| Customer | USN-3 | As a user, I want to edit the script | Edited text is used for artwork | Medium |
| Customer | USN-4 | As a user, I want artwork for every panel | One image is shown per panel | High |
| Customer | USN-5 | As a user, I want characters to look the same in all panels | Character appearance stays consistent | High |
| Customer | USN-6 | As a user, I want speech bubbles added automatically | Dialogue appears in bubbles on each panel | High |
| Customer | USN-7 | As a user, I want to download my comic | PDF and PNG files are downloaded | Medium |
