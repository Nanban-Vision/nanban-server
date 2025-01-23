from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import shutil
import uuid
from pathlib import Path
from gtts import gTTS
from voice_assistant import *
from object_detection import * 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],  
    allow_headers=["*"],  
)

TEMP_DIR = Path("temp")
TEMP_DIR.mkdir(exist_ok=True)

def text_to_speech(text, output_file, lang='en'):
    tts = gTTS(text=text, lang=lang)
    tts.save(output_file)

@app.post("/object-detection/")
async def object_detection(file: UploadFile = File(...)):
    picture_file_path = TEMP_DIR / f"{uuid.uuid4()}.jpg"
    with picture_file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
   
    detected_description = detect_objects(picture_file_path)

    if detected_description == "no_object": 
        return JSONResponse(
            content={"detail": "No objects detected in the image."},
            status_code=422
        )
    else:
        speech_file_path = TEMP_DIR / f"{uuid.uuid4()}.mp3"
        text_to_speech(detected_description, speech_file_path)
        
        return FileResponse(speech_file_path, media_type="audio/mpeg", filename=speech_file_path.name)

class VoiceAssistantRequest(BaseModel):
    query: str

@app.post("/voice-assistant/")
async def voice_assistant(request: VoiceAssistantRequest):  
    print(f"Received query: {request.query}")
    response_audio_path = None

    assistant_response = voice_mode(request.query)  
    if not response.query.lower().startswith('play song'):
        response_audio_path = TEMP_DIR / f"{uuid.uuid4()}.mp3"
        text_to_speech(assistant_response, response_audio_path)
    else: 
        response_audio_path = assistant_response
    return FileResponse(response_audio_path, media_type="audio/mpeg", filename=response_audio_path.name)

@app.get("/")
async def root():
    return {"status": "healthy"}
