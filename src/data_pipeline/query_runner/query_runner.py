import os
import pandas as pd
import sys


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "../"))  
sys.path.append(PROJECT_ROOT)

from utils.logging_utils import app_logger


import psycopg2
import yaml

class QueryRunner:
    def __init__(self, config_file):
        # Load database configuration
        with open(config_file, 'r') as file:
            self.config = yaml.safe_load(file)['database']
            app_logger.info('config.yaml loaded successfully for query runner')

    def connect(self):
        # Establish a connection to the database
        return psycopg2.connect(
            host=self.config['host'],
            port=self.config['port'],
            user=self.config['user'],
            password=self.config['password'],
            database=self.config['database']
        )

    def run_query(self, query, fetch_results=True):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute(query)

            # Fetch results if required
            if fetch_results:
                results = cursor.fetchall()
                return results
            else:
                conn.commit()  
                app_logger.info("Query executed successfully!")
        except Exception as e:
            app_logger.info(f"Error executing query: {e}")
        finally:
            conn.close()

# Test the Class and main Funcation 
if __name__ == "__main__":
    iquery = QueryRunner()
