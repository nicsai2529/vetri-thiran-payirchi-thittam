import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router

app = FastAPI(
    title="ComicCraft - AI Comic Story Creator",
    description="Generate personalized comic book stories and vivid illustrations powered by Google Gemini & Stable Diffusion",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure required static directories exist
for folder in ["static", "static/panels", "static/exports", "static/css", "static/fonts", "static/img"]:
    os.makedirs(os.path.join(os.getcwd(), folder), exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include application routes
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
