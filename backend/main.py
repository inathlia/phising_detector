from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from backend.model import analyze_content
from pathlib import Path

app = FastAPI(title="Phishing & Scam Detection API")

class TextRequest(BaseModel):
    content: str

@app.post("/api/analyze")
def analyze_text(req: TextRequest):
    return analyze_content(req.content)

@app.post("/api/analyze-file")
async def analyze_file(file: UploadFile = File(...)):
    content = (await file.read()).decode(errors="ignore")
    return analyze_content(content)

@app.get("/", response_class=HTMLResponse)
def frontend():
    return Path("frontend/index.html").read_text()

