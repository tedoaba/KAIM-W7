from sqlalchemy import Column, Integer, String, Text, DateTime  # Add DateTime here
from app.database import Base

class TelegramMessage(Base):
    __tablename__ = "telegram_messages"

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, index=True)
    date = Column(DateTime, index=True)  # This line now works
    text = Column(String, index=True)
    sender_id = Column(Integer, index=True)

class ObjectDetection(Base):
    __tablename__ = "object_detection"

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String, index=True)
    bounding_box = Column(String)
    confidence = Column(String)
    label = Column(String)
