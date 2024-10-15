import os
import logging

# Set up logging
logging.basicConfig(filename='logs/dbt_run.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def run_dbt():
    try:
        logging.info('Running DBT models...')
        os.system('dbt init dbt_medical_data')
        os.system('dbt run')  
        logging.info('DBT models run successfully.')
        
    except Exception as e:
        logging.error(f"Error running DBT models: {e}")
        raise

if __name__ == '__main__':
    run_dbt()
