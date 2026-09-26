@echo off
echo Starting ComicCraft AI Comic Story Creator...
echo Web Interface: http://127.0.0.1:8000
echo API Docs: http://127.0.0.1:8000/docs
echo.
pyenv\tools\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
pause
