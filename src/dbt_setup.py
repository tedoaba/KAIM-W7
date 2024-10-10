import os
import logging

# Set up logging
logging.basicConfig(filename='logs/dbt.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def run_dbt():
    try:
        logging.info('Running DBT models...')
        os.system('dbt run')  # Run DBT models
        logging.info('DBT models run successfully.')
        
    except Exception as e:
        logging.error(f"Error running DBT models: {e}")
        raise

if __name__ == '__main__':
    run_dbt()
