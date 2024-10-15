from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from app.database import get_db
import app.telegram_scraper
import app.crud
import app.yolo_object_detection
from app.schemas import TelegramMessageCreate, ObjectDetectionCreate
from app.models import TelegramMessage, ObjectDetection

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
    messages = await app.telegram_scraper.scrape_telegram_channel(channel)
    for message in messages:
        app.crud.create_telegram_message(db, TelegramMessageCreate(**message))
    return {"status": "success", "channel": channel, "messages_scraped": len(messages)}

# Endpoint to perform object detection
@app.post("/detect_objects/")
async def detect_objects(image_path: str, db: Session = Depends(get_db)):
    detections = app.yolo_object_detection.detect_objects(image_path)
    for detection in detections:
        app.crud.create_object_detection(db, ObjectDetectionCreate(image_url=image_path, **detection))
    return {"status": "success", "detections": detections}

# Endpoint to fetch a few samples of scraped Telegram data
@app.get("/scraped_data/")
def get_scraped_data(limit: int = 5, db: Session = Depends(get_db)):
    messages = db.query(TelegramMessage).limit(limit).all()
    return {"scraped_messages": messages}

# Endpoint to fetch a few samples of object detection data
@app.get("/detection_data/")
def get_detection_data(limit: int = 5, db: Session = Depends(get_db)):
    detections = db.query(ObjectDetection).limit(limit).all()
    return {"detections": detections}

# HTML Endpoint to display scraped Telegram data
@app.get("/scraped_data_html/", response_class=HTMLResponse)
def get_scraped_data_html(limit: int = 5, db: Session = Depends(get_db)):
    messages = db.query(TelegramMessage).limit(limit).all()
    
    html_content = "<h1>Scraped Telegram Messages</h1><ul>"
    for message in messages:
        html_content += f"<li>{message.content} - {message.timestamp}</li>"
    html_content += "</ul>"
    
    return html_content

# HTML Endpoint to display object detection data
@app.get("/detection_data_html/", response_class=HTMLResponse)
def get_detection_data_html(limit: int = 5, db: Session = Depends(get_db)):
    detections = db.query(ObjectDetection).limit(limit).all()
    
    html_content = "<h1>Object Detection Results</h1><ul>"
    for detection in detections:
        html_content += f"<li>Object: {detection.object_name}, Confidence: {detection.confidence}, Image: {detection.image_url}</li>"
    html_content += "</ul>"
    
    return html_content
