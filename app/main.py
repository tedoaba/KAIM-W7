from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db
import telegram_scraper
import crud
import yolo_object_detection
from schemas import TelegramMessageCreate, ObjectDetectionCreate

# Initialize FastAPI app
app = FastAPI()

# Home page endpoint
@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Ethiopian Medical Business Data Scraper and Object Detection API!"
    }

# Endpoint to scrape Telegram channel
@app.post("/scrape_telegram/")
async def scrape_telegram(channel: str, db: Session = Depends(get_db)):
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

