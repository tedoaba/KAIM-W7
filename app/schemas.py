from pydantic import BaseModel
from datetime import datetime  # Import datetime for DateTime type

class TelegramMessageCreate(BaseModel):
    message_id: int
    date: datetime  # Change DateTime to datetime
    text: str
    sender_id: int  # Changed this to int for consistency

class ObjectDetectionCreate(BaseModel):
    image_url: str
    bounding_box: str
    confidence: str
    label: str
