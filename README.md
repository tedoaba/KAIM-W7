# KAIM Week 7 Challenges

## Project Overview

This project aims to scrape images from specified Telegram channels, store them in a structured database (data warehouse), and prepare the dataset for object detection tasks using models like YOLOv5. The goal is to build a scalable system that continuously scrapes images, stores metadata efficiently, and enables future object detection, analytics, and reporting.

### Key Objectives:
1. **Scraping Images from Telegram Channels**: Scrape images and metadata from specified channels using the Telegram API.
2. **Data Warehousing**: Store scraped images and their metadata in a relational database.
3. **Object Detection Preparation**: Set up data for object detection, ensuring proper storage and accessibility.
4. **Data Transformation**: Use DBT (Data Build Tool) to transform the stored data for object detection and further processing.
5. **API Development**: Develop an API to expose processed data for real-time insights and analysis.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Requirements](#requirements)
- [Setup Instructions](#setup-instructions)
- [Task Breakdown](#task-breakdown)
  - [Task 1: Telegram Scraping](#task-1-telegram-scraping)
  - [Task 2: Data Warehousing](#task-2-data-warehousing)
- [Future Tasks](#future-tasks)
  - [Task 3: Object Detection](#task-3-object-detection)
  - [Task 4: Data Transformation with DBT](#task-4-data-transformation-with-dbt)
  - [Task 5: API Development](#task-5-api-development)
- [Project Structure](#project-structure)
- [Challenges and Solutions](#challenges-and-solutions)

---

## Requirements

- **Python 3.x**
- **Telethon** for Telegram API access
- **SQLAlchemy** for database management
- **PostgreSQL** or **SQLite** for data warehousing
- **Pillow (PIL)** for image processing
- **DBT (Data Build Tool)** for data transformation
- **YOLOv5** (for object detection in future tasks)

---

## Setup Instructions

### Step 1: Clone the Repository
```bash
git clone https://github.com/tedoaba/KAIM-W7.git
cd KAIM-W7
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Set Up Telegram API Credentials
- Sign up on [Telegram](https://my.telegram.org/apps) to get your `api_id` and `api_hash`.
- Add the credentials to the script as shown in the scraping section below.

### Step 4: Set Up the Database
For **SQLite**:
```bash
touch test.db
```

For **PostgreSQL**:
- Install PostgreSQL and create a database:
```bash
sudo apt-get install postgresql
sudo -u postgres psql
CREATE DATABASE telegram_images;
```

### Step 5: Running the Scraper
Run the Python script to start scraping images:
```bash
python scrape_telegram.py
```

---

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

---

## Future Tasks

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

---

## Project Structure

```
telegram-scraping-object-detection/
├── images/                     # Directory where scraped images are stored
├── scrape_telegram.py           # Telegram scraping script
├── database.py                  # Script to manage the database and store metadata
├── requirements.txt             # Python dependencies
├── README.md                    # Project documentation (this file)
├── test.db                      # SQLite database (for local testing)
└── data_transformations/        # Placeholder for DBT models and transformations
```

---

## Conclusion

This project lays the foundation for an automated image scraping pipeline from Telegram channels. The images and metadata stored in a structured database will be used for object detection, transforming the raw data into valuable insights through the upcoming tasks. With the current scraping and data warehousing components in place, the project is well-positioned for the next phases of object detection, transformation, and API development.
