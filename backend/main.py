from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import shutil, os
 
from ai_modules.final_analyzer import generate_final_report
 
app = FastAPI()
 
app.add_middleware(CORSMiddleware, allow_origins=["*"],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
 
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
 
@app.get("/")
def home():
    return {"message": "TrendPilotAI Backend Running"}
 
@app.post("/analyze")
async def analyze_content(
    file:      UploadFile = File(...),
    caption:   str = Form(""),
    region:    str = Form("IN"),
    state:     str = Form(""),        # e.g. IN-TN, IN-MH
    platforms: str = Form("instagram"), # comma-separated
    goal:      str = Form("viral"),
):
    try:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
 
        platform_list = [p.strip() for p in platforms.split(",") if p.strip()]
 
        result = generate_final_report(
            image_path    = file_path,
            caption       = caption,
            region        = region,
            state         = state,
            platforms     = platform_list,
            goal          = goal,
        )
 
        return {"success": True, "data": result}
 
    except Exception as e:
        print("MAIN API ERROR:", e)
        return {"success": False, "error": str(e)}