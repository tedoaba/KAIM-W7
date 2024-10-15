import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import logging

# Set up logging
logging.basicConfig(filename='../logs/load_data_to_database.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')


load_dotenv('.env')
db_url = os.getenv('DATABASE_URL')
db_table = os.getenv('DB_TABLE')
# Load the CSV file into a DataFrame
df = pd.read_csv('../data/telegram_medical_businesses_data_cleaned.csv')

# Create a PostgreSQL connection engine
engine = create_engine(db_url)

# Write the DataFrame to PostgreSQL (replace 'my_table' with your table name)
df.to_sql(db_table, engine, index=False, if_exists='append')

print("Data loaded successfully!")