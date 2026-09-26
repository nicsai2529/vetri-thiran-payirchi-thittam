import os
import traceback
from fastapi import APIRouter, Request, Form, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from app.gemini_flash import generate_outline
from app.gemini_pro import generate_story
from app.image_generator import generate_image
from app.layout_builder import build_comic_layout
from app.exporters import save_pdf

router = APIRouter()
templates = Jinja2Templates(directory="templates")


class PromptRequest(BaseModel):
    prompt: str = Field(..., description="Main story idea")
    character_name: str = Field(default="Hero", description="Main character name")
    setting: str = Field(default="Enchanted Forest", description="Story location/setting")
    tone: str = Field(default="Dramatic", description="Mood and tone of the story")
    style: str = Field(default="Comic Book", description="Visual art style")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Loads the homepage form for comic creation."""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@router.post("/generate", response_class=HTMLResponse)
async def generate_comic(
    request: Request,
    prompt: str = Form(...),
    character_name: str = Form("Hero"),
    setting: str = Form("Enchanted Forest"),
    tone: str = Form("Dramatic"),
    style: str = Form("Comic Book")
):
    """
    Handles form submission, runs AI pipeline, and renders comic preview.
    """
    try:
        # Combine user inputs into single prompt for rich context
        full_prompt = (
            f"{prompt}\n"
            f"The main character is {character_name}.\n"
            f"The setting is a {setting}.\n"
            f"The tone is {tone}. The art style is {style}."
        )

        print(f"🚀 Starting Comic Generation for: {character_name} in {setting}")

        # Step 1: Generate 5-panel outline via Gemini Flash
        outline = generate_outline(full_prompt)
        if not isinstance(outline, list) or not all("image_prompt" in panel for panel in outline):
            raise ValueError("Invalid outline structure from Gemini response.")

        # Step 2: Generate detailed narration and dialogues via Gemini Pro
        full_story = generate_story(outline)

        # Step 3: Generate comic panel illustrations via Stable Diffusion / image generator
        images = []
        for panel in outline:
            panel_prompt = f"{panel.get('image_prompt', '')}, character: {character_name}, style: {style}, {setting}"
            img_path = generate_image(panel_prompt)
            images.append(img_path)

        # Step 4: Build organized comic layout
        layout = build_comic_layout(images, full_story, outline)

        # Step 5: Export to PDF
        pdf_path = save_pdf(layout)
        web_pdf_path = "/" + pdf_path.replace("\\", "/")

        return templates.TemplateResponse(
            request=request,
            name="comic_preview.html",
            context={
                "layout": layout,
                "pdf_path": web_pdf_path,
                "prompt": prompt,
                "character_name": character_name,
                "setting": setting,
                "tone": tone,
                "style": style
            }
        )

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-comic/json")
async def generate_comic_json(payload: PromptRequest):
    """
    API endpoint that accepts JSON payloads and returns structured layout and PDF path.
    """
    try:
        full_prompt = (
            f"{payload.prompt}\n"
            f"The main character is {payload.character_name}.\n"
            f"The setting is a {payload.setting}.\n"
            f"The tone is {payload.tone}. The art style is {payload.style}."
        )

        outline = generate_outline(full_prompt)
        full_story = generate_story(outline)
        images = [
            generate_image(f"{panel.get('image_prompt', '')}, {payload.character_name}, style: {payload.style}")
            for panel in outline
        ]
        layout = build_comic_layout(images, full_story, outline)
        pdf_path = save_pdf(layout)
        web_pdf_path = "/" + pdf_path.replace("\\", "/")

        return JSONResponse({
            "status": "success",
            "character_name": payload.character_name,
            "setting": payload.setting,
            "tone": payload.tone,
            "style": payload.style,
            "layout": layout,
            "pdf_path": web_pdf_path
        })
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})


@router.get("/export-success", response_class=HTMLResponse)
async def export_success(request: Request, pdf_path: str = Query("", description="Path to exported PDF")):
    """
    Confirmation page displayed after comic download.
    """
    return templates.TemplateResponse(
        request=request,
        name="export_success.html",
        context={"pdf_path": pdf_path}
    )


@router.get("/test-image")
@router.post("/test-image")
async def test_image(prompt: str = "A futuristic city at sunset, sci-fi, cinematic, artstation"):
    """
    Developer utility route to test image generation directly.
    """
    try:
        image_path = generate_image(prompt)
        return {"message": "Image generated successfully", "path": "/" + image_path.replace("\\", "/")}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
