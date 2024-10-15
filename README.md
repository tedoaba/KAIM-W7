# KAIM Week 7 Challenges

## Kara Solutions: Ethiopian Medical Business Data Warehouse Project

## Overview

This project aims to create a **data warehouse** for Ethiopian medical businesses by scraping relevant data from public **Telegram channels** and analyzing images through **object detection** using the **YOLO (You Only Look Once)** algorithm. The system includes processes for **data scraping**, **data cleaning**, **data transformation**, and **data storage**, as well as providing **API access** to the processed data.

The project consists of four main tasks:

1. **Data Scraping from Telegram Channels**
2. **Data Cleaning and Transformation**
3. **Object Detection using YOLO**
4. **Data Warehouse Design and Implementation**

This `README` provides a step-by-step guide for setting up and running each part of the project, including the tools and technologies used, as well as detailed instructions for replicating the work.

---

## Table of Contents

- [Overview](#overview)
- [System Requirements](#system-requirements)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
  - [1. Data Scraping](#1-data-scraping)
  - [2. Data Cleaning and Transformation](#2-data-cleaning-and-transformation)
  - [3. Object Detection using YOLO](#3-object-detection-using-yolo)
  - [4. Data Warehouse Design and Implementation](#4-data-warehouse-design-and-implementation)
- [FastAPI for Data Access](#fastapi-for-data-access)
- [Future Improvements](#future-improvements)

---

## System Requirements

To run this project, the following software and libraries are required:

- **Python 3.8+**
- **PostgreSQL or SQLite** (for database storage)
- **Telethon** (Telegram scraping)
- **DBT (Data Build Tool)** (data transformations)
- **YOLOv5** (object detection)
- **FastAPI** (API development)
- **Pydantic** (for data validation)
- **SQLAlchemy** (for database ORM)

### Python Libraries

The main Python libraries required are listed below. Install them using `pip`:

```bash
pip install telethon dbt opencv-python torch torchvision fastapi uvicorn pydantic sqlalchemy
```

---

## Project Structure

Here’s a high-level overview of the project’s structure:

```bash
├── data_scraping/
│   ├── telegram_scraper.py     # Script for scraping Telegram data
│   ├── utils.py                # Helper functions for scraping
│   └── raw_data/               # Directory where raw data is temporarily stored
├── data_cleaning/
│   ├── dbt_project/            # DBT models for data transformation
│   └── cleaning_pipeline.py    # Script for running DBT data cleaning models
├── object_detection/
│   ├── detect.py               # Script for YOLO object detection
│   └── images/                 # Scraped images for object detection
├── warehouse/
│   ├── models.py               # SQLAlchemy models for the data warehouse
│   └── database.py             # Database connection and schema definitions
├── fastapi_app/
│   ├── main.py                 # FastAPI app entry point
│   ├── crud.py                 # CRUD operations for API
│   ├── schemas.py              # Pydantic schemas for request/response validation
│   └── database.py             # Database connection for FastAPI
└── README.md                   # Project documentation
```

---

## Setup Instructions

### 1. Data Scraping

#### Description
The first step involves scraping textual and image data from public Telegram channels that focus on Ethiopian medical businesses. The data is collected using Python scripts and the **Telethon** library, which interfaces with Telegram's API.

#### Telegram Channels Scraped
- [DoctorsET](https://t.me/DoctorsET)
- [Chemed Telegram Channel](https://t.me/lobelia4cosmetics)
- [Yetenaweg](https://t.me/yetenaweg)
- [EAHCI](https://t.me/EAHCI)
- Additional channels from [https://et.tgstat.com/medicine](https://et.tgstat.com/medicine)

#### Setup and Execution

1. **Install Dependencies**:
   ```bash
   pip install telethon
   ```

2. **Run the Scraper**:
   Before running, make sure to create a `.env` file with your Telegram API credentials (API ID, API hash, and phone number).
   
   Example `.env` file:
   ```plaintext
   API_ID=your_api_id
   API_HASH=your_api_hash
   PHONE=your_phone_number
   ```

   Execute the script:
   ```bash
   python data_scraping/telegram_scraper.py
   ```

3. **Output**:
   - Text data and metadata will be saved in a local database.
   - Image files will be stored in the `raw_data/images/` directory.

---

### 2. Data Cleaning and Transformation

#### Description
After scraping, the raw data is cleaned and transformed using **DBT** (Data Build Tool). This process involves removing duplicates, handling missing values, and standardizing formats for easy querying and analysis.

#### Setup and Execution

1. **Install DBT**:
   Install DBT and initialize a new DBT project:
   ```bash
   pip install dbt
   dbt init medical_data_project
   ```

2. **Define DBT Models**:
   - Define SQL models in the `dbt_project/models/` directory for cleaning and transforming data.
   - Sample DBT model file:
     ```sql
     -- models/cleaned_telegram_data.sql
     select
         distinct message_id,
         message_text,
         timestamp::timestamp as message_time,
         channel_name
     from raw_data
     where message_text is not null
     ```

3. **Run DBT Models**:
   Apply the transformations by running the DBT models:
   ```bash
   dbt run
   ```

4. **Testing**:
   Test data quality using DBT's built-in test features:
   ```bash
   dbt test
   ```

---

### 3. Object Detection using YOLO

#### Description
In this task, we perform **object detection** on the scraped images using **YOLOv5** to detect medical equipment, promotional materials, and other objects related to Ethiopian medical businesses.

#### Setup and Execution

1. **Install YOLO Dependencies**:
   Install PyTorch and YOLOv5:
   ```bash
   pip install torch torchvision
   git clone https://github.com/ultralytics/yolov5.git
   cd yolov5
   pip install -r requirements.txt
   ```

2. **Prepare Images**:
   Place the scraped images from the `raw_data/images/` folder into the `yolov5/data/images/` directory for object detection.

3. **Run YOLO**:
   Run the YOLOv5 object detection script:
   ```bash
   python detect.py --weights yolov5s.pt --img 640 --conf 0.5 --source data/images
   ```

4. **Store Detection Results**:
   The detection results (bounding boxes, class labels, and confidence scores) will be saved in a structured format, which will later be loaded into the data warehouse.

---

### 4. Data Warehouse Design and Implementation

#### Description
The data warehouse stores all the cleaned, transformed, and enriched data, enabling efficient querying and analysis. The data includes textual Telegram posts, image metadata, and YOLO object detection results.

#### Setup and Execution

1. **Install PostgreSQL**:
   Install and configure PostgreSQL, or alternatively, use SQLite for local testing.

2. **Database Models**:
   Define your database schema in `warehouse/models.py` using SQLAlchemy:
   ```python
   from sqlalchemy import Column, Integer, String, ForeignKey
   from sqlalchemy.orm import relationship

   class ImageMetadata(Base):
       __tablename__ = 'image_metadata'
       id = Column(Integer, primary_key=True)
       image_path = Column(String, nullable=False)
       channel_name = Column(String, nullable=False)
       timestamp = Column(String, nullable=False)

   class ObjectDetection(Base):
       __tablename__ = 'object_detection'
       id = Column(Integer, primary_key=True)
       image_id = Column(Integer, ForeignKey('image_metadata.id'))
       bounding_box = Column(String, nullable=False)
       confidence = Column(Float, nullable=False)
       class_label = Column(String, nullable=False)

       image = relationship("ImageMetadata", back_populates="detections")
   ```

3. **Migrate Database**:
   Initialize and migrate the database to create the tables:
   ```bash
   python warehouse/database.py
   ```

---

## FastAPI for Data Access

#### Description
To expose the processed data via an API, **FastAPI** is used to create RESTful endpoints. These endpoints allow users to query the data warehouse for images, detections, and associated metadata.

#### Setup and Execution

1. **Install FastAPI**:
   ```bash
   pip install fastapi uvicorn
   ```

2. **Create FastAPI Application**:
   - Define routes in `fastapi_app/main.py`:
     ```python
     from fastapi import FastAPI, Depends
     from sqlalchemy.orm import Session
     from .crud import get_detections
     from .database import SessionLocal

     app = FastAPI()

     @app.get("/detections/{image_id}")
     def read_detections(image_id: int, db: Session = Depends(get_db)):
         detections = get_detections(db, image_id=image_id

)
         return detections
     ```

3. **Run FastAPI**:
   Start the FastAPI server:
   ```bash
   uvicorn fastapi_app.main:app --reload
   ```

4. **Access the API**:
   Visit `http://127.0.0.1:8000/docs` to explore the automatically generated API documentation.

---

## Future Improvements

1. **Data Enrichment**: Add more sources of data, such as public medical directories or customer reviews, to provide a richer dataset.
2. **Machine Learning Models**: Build predictive models to analyze trends in medical products or promotional effectiveness.
3. **Fine-tune YOLO**: Train the YOLO model on specific Ethiopian medical products and packaging to improve detection accuracy.

---

By following these steps, you can set up a fully operational data pipeline for scraping, cleaning, transforming, analyzing, and querying data on Ethiopian medical businesses.