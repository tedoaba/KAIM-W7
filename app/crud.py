from sqlalchemy.orm import Session
from app.models import TelegramMessage, ObjectDetection
from app.schemas import TelegramMessageCreate, ObjectDetectionCreate

def create_telegram_message(db: Session, message: TelegramMessageCreate):
    db_message = TelegramMessage(channel=message.channel, message_content=message.message_content)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def create_object_detection(db: Session, detection: ObjectDetectionCreate):
    db_detection = ObjectDetection(
        image_url=detection.image_url, 
        bounding_box=detection.bounding_box,
        confidence=detection.confidence, 
        label=detection.label
    )
    db.add(db_detection)
    db.commit()
    db.refresh(db_detection)
    return db_detection
