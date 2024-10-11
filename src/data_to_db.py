import pandas as pd
from sqlalchemy import create_engine

# Load the CSV file into a DataFrame
df = pd.read_csv('../data/telegram_medical_businesses_data_cleaned.csv')

# Create a PostgreSQL connection engine
engine = create_engine('postgresql://postgres:tedoaba12@localhost:5435/scraped')

# Write the DataFrame to PostgreSQL (replace 'my_table' with your table name)
df.to_sql('medata', engine, index=False, if_exists='append')

print("Data loaded successfully!")