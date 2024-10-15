from pydantic import BaseModel

class TelegramMessageCreate(BaseModel):
    channel: str
    message_content: str

class ObjectDetectionCreate(BaseModel):
    image_url: str
    bounding_box: str
    confidence: str
    label: str
