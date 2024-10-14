from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class TelegramMessage(Base):
    __tablename__ = "telegram_messages"

    id = Column(Integer, primary_key=True, index=True)
    channel = Column(String, index=True)
    message_content = Column(Text)

class ObjectDetection(Base):
    __tablename__ = "object_detection"

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String, index=True)
    bounding_box = Column(String)
    confidence = Column(String)
    label = Column(String)
