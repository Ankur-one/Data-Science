import pandas as pd
import os
from sqlalchemy import create_engine
import logging
import time

# Ensure log directory exists
os.makedirs("logs", exist_ok=True)

# Configure logging
logging.basicConfig(
    filename="logs/ingestion_db.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

# SQLite engine
engine = create_engine('sqlite:///inventory.db')

def ingest_db(df, table_name, engine):
    """Insert dataframe into database."""
    try:
        df.to_sql(table_name, con=engine, if_exists='replace', index=False)
        logging.info(f"Table '{table_name}' created successfully.")
    except Exception as e:
        logging.error(f"Failed to ingest {table_name}: {e}")

def load_raw_data():
    start = time.time()
    folder_path = r"D:\Data analyst\Project\Vendor\DA"  # safer path
    
    for file in os.listdir(folder_path):
        if file.endswith('.csv'):
            try:
                file_path = os.path.join(folder_path, file)
                df = pd.read_csv(file_path)
                table_name = file[:-4].replace(" ", "_")
                
                logging.info(f'Ingesting {file} into database as table {table_name}')
                ingest_db(df, table_name, engine)
            
            except Exception as e:
                logging.error(f"Error processing file {file}: {e}")
    
    end = time.time()
    total_time = (end - start) / 60
    logging.info('-------- Ingestion Complete -------')
    logging.info(f'Total Time Taken: {total_time:.2f} minutes')

if __name__ == "__main__":   # ✅ Correct
    load_raw_data()
