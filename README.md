# Building a Data Warehouse to Store Data on Ethiopian Medical Business Data Scraped from Telegram Channels

## KAIM Week 7 Challenges

## Project Overview

This project aims to create a **data warehouse** for Ethiopian medical businesses by scraping relevant data from public **Telegram channels** and analyzing images through **object detection** using the **YOLO (You Only Look Once)** algorithm. The system includes processes for **data scraping**, **data cleaning**, **data transformation**, and **data storage**, as well as providing **API access** to the processed data.

### Key Objectives:
1. **Scraping Images from Telegram Channels**: Scrape images and metadata from specified channels using the Telegram API.
2. **Data Warehousing**: Store scraped images and their metadata in a relational database.
3. **Object Detection Preparation**: Set up data for object detection, ensuring proper storage and accessibility.
4. **Data Transformation**: Use DBT (Data Build Tool) to transform the stored data for object detection and further processing.
5. **API Development**: Develop an API to expose processed data for real-time insights and analysis.


## Table of Contents

- [Project Overview](#project-overview)
- [Requirements](#requirements)
- [Setup Instructions](#setup-instructions)
- [Task Breakdown](#task-breakdown)
  - [Task 1: Telegram Scraping](#task-1-telegram-scraping)
  - [Task 2: Data Warehousing](#task-2-data-warehousing)
  - [Task 3: Object Detection](#task-3-object-detection)
  - [Task 4: Data Transformation with DBT](#task-4-data-transformation-with-dbt)
  - [Task 5: API Development](#task-5-api-development)
- [Project Structure](#project-structure)
- [Challenges and Solutions](#challenges-and-solutions)

## Requirements

- **Python 3.x**
- **Telethon** for Telegram API access
- **SQLAlchemy** for database management
- **PostgreSQL** or **SQLite** for data warehousing
- **Pillow (PIL)** for image processing
- **DBT (Data Build Tool)** for data transformation
- **YOLOv5** (for object detection in future tasks)


## Task Breakdown

### Task 1: Telegram Scraping

#### Overview:
This task focuses on scraping images from Telegram channels using the **Telethon** library. Images are downloaded into a local folder, and metadata is collected for each image, including:
- File path
- Source channel
- Timestamp

#### Key Files:
- `scrape_telegram.py`: Handles the Telegram scraping and metadata extraction.

### Task 2: Data Warehousing

#### Overview:
This task stores the image metadata (from Task 1) into a relational database. The database helps manage image metadata, ensuring future scalability and accessibility for object detection.

#### Database Schema:
- **Table: images**
    - `id`: Primary key (auto-increment).
    - `file_path`: Path to the saved image.
    - `source_channel`: The channel from where the image was scraped.
    - `timestamp`: Time when the image was downloaded.

#### Key Files:
- `database.py`: Manages database operations, including storing image metadata.

### Task 3: Object Detection

In the next phase, object detection will be performed on the scraped images using models like **YOLOv5**. This will involve:
- Loading images from the database.
- Running detection models on the images.
- Storing results in the database.

### Task 4: Data Transformation with DBT

**DBT** will be used for transforming the data in the warehouse, ensuring it’s structured properly for object detection models. The transformations will include:
- Cleaning and organizing metadata.
- Generating datasets optimized for model input.

### Task 5: API Development

An API will be developed to expose the processed data and object detection results for real-time insights. The API will be built using **Flask** or **FastAPI** and will provide endpoints for querying detection results and metadata.

### Python Libraries

The main Python libraries required are listed below. Install them using `pip`:

```bash
pip install telethon dbt opencv-python torch torchvision fastapi uvicorn pydantic sqlalchemy
```

## Project Structure

Here’s a high-level overview of the project’s structure:

```bash
├── app/
│   ├── templates/   
│   ├── crud.py               
│   └── database.py
│   ├── main.py
│   ├── models.py                
│   └── schemas.py
│   ├── telegram_scraper.py     
│   ├── yolo_object_detection.py                                  
├── data/
├── images/
├── logs/
├── dbt_medical_data/
│   ├── analaysis/     
│   ├── macros              
│   └── models/    
│   ├── seeds/    
│   ├── snapshots                
│   └── tests/                          
├── notebooks/
│   ├── telegram_scraper.py     
│   ├── utils.py                
│   └── raw_data/               
├── scripts/
│   ├── __init__.py     
│   ├── main.py                
│   └── dbt_setup.py        
├── src/
│   ├── telegram_scraper.py     
│   ├── utils.py                
│   └── raw_data/               
├── tests/
│   ├── __init__.py     
│   ├── test_data_loader.py                              
├── yolov5/
│   ├── models/
│   ├── runs/               
│   └── utils/
│   ├── detect.py     
│   ├── export.py                
│   └── yolov5.pt                             
├── .gitignore               
├── requirements.txt
└── README.md                   #
```

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
   python src/message_scraper.py
   ```

3. **Output**:
   - Text data and metadata will be saved in a local database.
   - Image files will be stored in the `images/` directory.

### 2. Data Cleaning and Transformation

#### Description
After scraping, the raw data is cleaned and transformed using **DBT** (Data Build Tool). This process involves removing duplicates, handling missing values, and standardizing formats for easy querying and analysis.

#### Setup and Execution

1. **Install DBT**:
   Install DBT and initialize a new DBT project:
   ```bash
   pip install dbt
   dbt init dtb_medical_data
   ```

2. **Define DBT Models**:
   - Define SQL models in the `dbt_medical_data/models/` directory for cleaning and transforming data.
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
   Place the scraped images from the `images/` folder directory for object detection.

3. **Run YOLO**:
   Run the YOLOv5 object detection script:
   ```bash
   cd yolov5
   python detect.py
   ```

4. **Store Detection Results**:
   The detection results (bounding boxes, class labels, and confidence scores) will be saved in a structured format, which will later be loaded into the data warehouse.

### 4. Data Warehouse Design and Implementation

#### Description
The data warehouse stores all the cleaned, transformed, and enriched data, enabling efficient querying and analysis. The data includes textual Telegram posts, image metadata, and YOLO object detection results.

#### Setup and Execution

1. **Install PostgreSQL**:
   Install and configure PostgreSQL, or alternatively, use SQLite for local testing.

2. **Database Models**:
   Define your database schema in `app/models.py` using SQLAlchemy:
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
   python app/database.py
   ```

## FastAPI for Data Access

#### Description
To expose the processed data via an API, **FastAPI** is used to create RESTful endpoints. These endpoints allow users to query the data warehouse for images, detections, and associated metadata.

#### Setup and Execution

1. **Install FastAPI**:
   ```bash
   pip install fastapi uvicorn
   ```

2. **Create FastAPI Application**:
   - Define routes in `app/main.py`:
     
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
   uvicorn app.main:app --reload
   ```

4. **Access the API**:
   Visit `http://127.0.0.1:8000/` to explore the automatically generated API documentation.

## Future Improvements

1. **Data Enrichment**: Add more sources of data, such as public medical directories or customer reviews, to provide a richer dataset.
2. **Machine Learning Models**: Build predictive models to analyze trends in medical products or promotional effectiveness.
3. **Fine-tune YOLO**: Train the YOLO model on specific Ethiopian medical products and packaging to improve detection accuracy.


By following these steps, you can set up a fully operational data pipeline for scraping, cleaning, transforming, analyzing, and querying data on Ethiopian medical businesses.
