from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from app.database import get_db
from app import crud, telegram_scraper, yolo_object_detection
from app.schemas import TelegramMessageCreate, ObjectDetectionCreate
from app.models import TelegramMessage, ObjectDetection

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Ethiopian Medical Business Data Scraper and Object Detection API!"}

@app.post("/scrape_telegram/")
async def scrape_telegram(channel: str, db: Session = Depends(get_db)):
    messages = await telegram_scraper.scrape_telegram_channel(channel)
    for message in messages:
        crud.create_telegram_message(db, TelegramMessageCreate(**message))
    return {"status": "success", "channel": channel, "messages_scraped": len(messages)}

@app.post("/detect_objects/")
async def detect_objects(image_path: str, db: Session = Depends(get_db)):
    detections = yolo_object_detection.detect_objects(image_path)
    for detection in detections:
        crud.create_object_detection(db, ObjectDetectionCreate(image_url=image_path, **detection))
    return {"status": "success", "detections": detections}

@app.get("/scraped_data/")
def get_scraped_data(limit: int = 5, db: Session = Depends(get_db)):
    messages = db.query(TelegramMessage).limit(limit).all()
    return {"scraped_messages": messages}

@app.get("/detection_data/")
def get_detection_data(limit: int = 5, db: Session = Depends(get_db)):
    detections = db.query(ObjectDetection).limit(limit).all()
    return {"detections": detections}

@app.get("/scraped_data_html/", response_class=HTMLResponse)
def get_scraped_data_html(limit: int = 5, db: Session = Depends(get_db)):
    messages = db.query(TelegramMessage).limit(limit).all()
    html_content = "<h1>Scraped Telegram Messages</h1><ul>"
    for message in messages:
        html_content += f"<li>{message.message_content}</li>"
    html_content += "</ul>"
    return html_content

@app.get("/detection_data_html/", response_class=HTMLResponse)
def get_detection_data_html(limit: int = 5, db: Session = Depends(get_db)):
    detections = db.query(ObjectDetection).limit(limit).all()
    html_content = "<h1>Object Detection Results</h1><ul>"
    for detection in detections:
        html_content += f"<li>Object: {detection.label}, Confidence: {detection.confidence}, Image: {detection.image_url}</li>"
    html_content += "</ul>"
    return html_content
