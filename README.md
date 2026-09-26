# ComicCraft - AI Comic Story Creator using Gemini Models

ComicCraft is a full-stack AI-driven web application that turns story ideas into personalized, multi-panel comic book stories and vivid illustrations. Built with **FastAPI**, **Google Gemini AI (1.5 Flash & 1.5 Pro)**, and **Stable Diffusion / Image Generator**, ComicCraft automates the entire creative pipeline: storyline outlining, character dialogues, panel art generation, layout building, and downloadable PDF compilation.

---

## 🌟 Key Features

- **Gemini 1.5 Flash Outline Generator**: Generates a structured 5-panel comic outline including scene titles, descriptions, and tailored image generation prompts.
- **Gemini 1.5 Pro Story & Dialogue Generator**: Expands outlines into engaging narrative text, environmental captions, and formatted character dialogues.
- **Comic Illustration Engine**: Generates panel-by-panel comic artwork customized by art style (Classic Comic Book, Anime/Manga, Pixel Art, Realistic, Dark Noir, Vibrant Watercolor).
- **Automated Layout Builder**: Harmonizes scene descriptions, generated imagery, dialogues, and badges into a responsive comic layout.
- **FPDF Multi-Page Comic PDF Exporter**: Compiles complete comic strips into a timestamped, printable, shareable PDF comic book.
- **FastAPI REST API & Interactive UI**: Provides both an interactive Jinja2 web frontend and documented OpenAPI JSON endpoints (`/docs`).

---

## 🏗️ Architecture & Project Structure

```
comiccraft/
│
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entrypoint & static mounting
│   ├── routes.py            # API & web route handlers
│   ├── gemini_flash.py      # 5-panel outline generation using Gemini Flash
│   ├── gemini_pro.py        # Narration & dialogue generation using Gemini Pro
│   ├── image_generator.py   # Comic-style image generation & fallback pipeline
│   ├── layout_builder.py    # Assembles images, story text & outlines
│   └── exporters.py         # Multi-page PDF generation via FPDF
│
├── templates/
│   ├── index.html           # Comic creation input form & live prompt presets
│   ├── comic_preview.html   # Panel-by-panel interactive comic viewer
│   ├── export_success.html  # Download confirmation & CTA page
│   ├── result.html          # Plan review template
│   └── all_users.html       # Generations history template
│
├── static/
│   ├── css/style.css        # Rich comic design system, animations & dark mode
│   ├── panels/              # Storage for generated panel images
│   ├── exports/             # Storage for exported comic PDFs
│   └── fonts/               # Custom fonts directory
│
├── pyenv/                   # Standalone Python 3.11 environment
├── .env                     # Environment variables (API keys & models)
├── requirements.txt         # Python dependencies
├── run.bat                  # One-click Windows startup script
└── README.md                # Documentation
```

---

## 🚀 Quick Start Guide

### 1. Configure Environment Variables
Copy or edit `.env` in the root directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
HF_API_KEY=your_huggingface_api_key_here
MODEL_FLASH=gemini-1.5-flash
MODEL_PRO=gemini-1.5-pro
SD_MODEL=runwayml/stable-diffusion-v1-5
```
*(Note: If no Gemini API key is provided, ComicCraft automatically runs in smart fallback demo mode with high-quality generated content).*

### 2. Run the Server
Double click `run.bat` or run:
```bash
pyenv\tools\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### 3. Open in Browser
- **Web App**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive Swagger API Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📡 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Loads the ComicCraft homepage creation form |
| `POST` | `/generate` | Form submission endpoint; generates comic and renders preview |
| `POST` | `/generate-comic/json` | REST API endpoint accepting JSON payloads (`prompt`, `character_name`, `setting`, `tone`, `style`) |
| `GET` | `/export-success` | Renders the export confirmation page with PDF download links |
| `GET/POST` | `/test-image` | Utility route to test image generation directly |

---

## 🎓 Milestone Deliverables Covered
- **Milestone 1**: Generative AI model selection (Gemini Flash, Gemini Pro, Stable Diffusion) & isolated environment setup.
- **Milestone 2**: Core backend logic (`gemini_flash.py`, `gemini_pro.py`, `image_generator.py`, `layout_builder.py`, `exporters.py`).
- **Milestone 3**: FastAPI routing & controller integration in `routes.py`.
- **Milestone 4**: Responsive Jinja2 frontend templates & comic design system.
- **Milestone 5**: Local deployment, PDF export pipeline verification, and OpenAPI documentation.
