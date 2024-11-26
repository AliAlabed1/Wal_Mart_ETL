import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "../"))  # Adjust to reach `src`
sys.path.append(PROJECT_ROOT)

from utils.logging_utils import app_logger
import psycopg2
import yaml
import pandas as pd

class ExportToPostgress:
    def __init__(self, config_file):
        # Load the configuration
        with open(config_file, 'r') as file:
            self.config = yaml.safe_load(file)['database']
            app_logger.info('Load config.yml successfuly')

    def connect(self):
        # Establish a connection to the database
        return psycopg2.connect(
            host=self.config['host'],
            port=self.config['port'],
            user=self.config['user'],
            password=self.config['password'],
            database=self.config['database']
        )

    def export(self, json_data):
        try:
            conn = self.connect()
            cursor = conn.cursor()

            # Load and ensure tables exist
            self.ensure_table_exists(cursor, json_data['datetime_dim'], "datetime_dim")
            self.ensure_table_exists(cursor, json_data['holiday_week_dim'], "holiday_week_dim")
            self.ensure_table_exists(cursor, json_data['fact_table'], "fact_table")

            # Insert data
            self.insert_table(cursor, conn, pd.DataFrame.from_dict(json_data['datetime_dim']), "datetime_dim")
            self.insert_table(cursor, conn, pd.DataFrame.from_dict(json_data['holiday_week_dim']), "holiday_week_dim")
            self.insert_table(cursor, conn, pd.DataFrame.from_dict(json_data['fact_table']), "fact_table")

            app_logger.info("Data loaded successfully!")

        except Exception as e:
            app_logger.error(f"Error: {e}")
        finally:
            conn.close()

    def ensure_table_exists(self, cursor, data_dict, table_name):
        """Create the table dynamically if it does not exist."""
        df = pd.DataFrame.from_dict(data_dict)
        columns = ", ".join([f"{col} {self.get_postgres_type(dtype)}" for col, dtype in zip(df.columns, df.dtypes)])
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {columns}
        );
        """
        cursor.execute(create_table_query)

    @staticmethod
    def get_postgres_type(dtype):
        """Map Pandas data types to PostgreSQL data types."""
        if pd.api.types.is_integer_dtype(dtype):
            return "INTEGER"
        elif pd.api.types.is_float_dtype(dtype):
            return "FLOAT"
        elif pd.api.types.is_bool_dtype(dtype):
            return "BOOLEAN"
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            return "TIMESTAMP"
        else:
            return "TEXT"

    def insert_table(self, cursor, conn, dataframe, table_name):
        # Convert DataFrame to list of tuples
        columns = ",".join(dataframe.columns)
        values = [tuple(x) for x in dataframe.to_numpy()]
        placeholders = ",".join(["%s"] * len(dataframe.columns))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        # Insert data into the table
        cursor.executemany(query, values)
        conn.commit()


# Test the Class and main Funcation 
if __name__ == "__main__":
    iload = ExportToPostgress()