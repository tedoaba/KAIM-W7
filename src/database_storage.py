import psycopg2
import pandas as pd
from config.db_config import db_params
import logging

# Set up logging
logging.basicConfig(filename='logs/data_cleaning.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def store_data_in_db(cleaned_file_path):
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Create table if not exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS telegram_medical_businesses (
                message_id BIGINT PRIMARY KEY,
                date TIMESTAMP,
                text TEXT,
                sender_id VARCHAR(255)
            );
        ''')

        # Load cleaned data
        df = pd.read_csv(cleaned_file_path)

        # Insert cleaned data into the database
        for _, row in df.iterrows():
            cursor.execute('''
                INSERT INTO telegram_medical_businesses (message_id, date, text, sender_id)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (message_id) DO NOTHING;
            ''', (row['message_id'], row['date'], row['text'], row['sender_id']))

        conn.commit()
        cursor.close()
        conn.close()

        logging.info(f'Cleaned data stored in PostgreSQL database.')
        
    except Exception as e:
        logging.error(f"Error storing data in database: {e}")
        raise

if __name__ == '__main__':
    cleaned_file_path = 'telegram_medical_businesses_data_cleaned.csv'  # Update path if necessary
    store_data_in_db(cleaned_file_path)
