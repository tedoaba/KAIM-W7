from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import get_db
import app.telegram_scraper
import app.crud
import app.yolo_object_detection
from app.schemas import TelegramMessageCreate, ObjectDetectionCreate

# Initialize FastAPI app
app = FastAPI()

# Home page endpoint
@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Ethiopian Medical Business Data Scraper and Object Detection API!"
    }

from pydantic import BaseModel

class TelegramChannel(BaseModel):
    channel: str

@app.post("/scrape_telegram/")
async def scrape_telegram(channel_data: TelegramChannel, db: Session = Depends(get_db)):
    channel = channel_data.channel
    messages = await telegram_scraper.scrape_telegram_channel(channel)
    for message in messages:
        crud.create_telegram_message(db, TelegramMessageCreate(**message))
    return {"status": "success", "channel": channel, "messages_scraped": len(messages)}

# Endpoint to perform object detection
@app.post("/detect_objects/")
async def detect_objects(image_path: str, db: Session = Depends(get_db)):
    detections = yolo_object_detection.detect_objects(image_path)
    for detection in detections:
        crud.create_object_detection(db, ObjectDetectionCreate(image_url=image_path, **detection))
    return {"status": "success", "detections": detections}

