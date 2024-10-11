import pandas as pd
import logging

# Set up logging
logging.basicConfig(filename='../logs/data_cleaning.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def clean_data(file_path):
    try:
        logging.info('Starting data cleaning process...')
        
        # Load raw data
        df = pd.read_csv(file_path)

        # Remove duplicates
        df_cleaned = df.drop_duplicates()

        # Handle missing values
        df_cleaned.dropna(subset=['text'], inplace=True)
        df_cleaned.fillna({'sender_id':'Unknown'}, inplace=True)

        # Standardize date format
        df_cleaned['date'] = pd.to_datetime(df_cleaned['date'], errors='coerce')

        # Data validation (Remove empty messages)
        df_cleaned = df_cleaned[df_cleaned['text'].str.strip() != '']

        # Save cleaned data
        cleaned_file_path = file_path.replace('.csv', '_cleaned.csv')
        df_cleaned.to_csv(cleaned_file_path, index=False)

        logging.info(f'Data cleaned successfully. Cleaned data saved at: {cleaned_file_path}')

        return cleaned_file_path

    except Exception as e:
        logging.error(f'Error during data cleaning: {e}')
        raise

if __name__ == '__main__':
    file_path = '../data/telegram_medical_businesses_data.csv'  # Update this path as needed
    clean_data(file_path)
