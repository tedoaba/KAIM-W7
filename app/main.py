from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from app.database import get_db
import app.telegram_scraper  # Assuming this module has the scraping logic
import app.crud  # Assuming this module contains CRUD operations
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

# Scraping endpoint
@app.post("/scrape")
def scrape_data(db: Session = Depends(get_db)):
    try:
        # Perform scraping (you need to implement the actual scraping logic in telegram_scraper)
        scraped_messages = app.telegram_scraper.scrape_telegram_messages()  # Example function
        for message in scraped_messages:
            # Save each message to the database using CRUD
            telegram_message_create = TelegramMessageCreate(
                message_id=message['message_id'],
                date=message['date'],
                text=message['text'],
                sender_id=message['sender_id']
            )
            app.crud.create_telegram_message(db=db, message=telegram_message_create)

        return {"message": "Scraping completed successfully!", "data": scraped_messages}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
