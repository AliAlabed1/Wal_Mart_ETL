import os
import sys

# Add the directory containing the `src` folder to the Python path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "../"))  # Adjust to reach `src`
sys.path.append(PROJECT_ROOT)


from data_pipeline.extractor.loader import LoadCSVFile
from utils.logging_utils import app_logger
from data_pipeline.Transformers.transformer import Transformer
from data_pipeline.loader.exporter import ExportToPostgress
from data_pipeline.query_runner.query_runner import QueryRunner
def execute():
    """
    GET method to render the HTML form.
    """
    loader = LoadCSVFile()
    df = loader.load_data('../../Data/Walmart.csv')
    

    transformer = Transformer()
    json_data = transformer.transform(df)
    exporter = ExportToPostgress(config_file=f'{PROJECT_ROOT}/config.yaml')
    exporter.export(json_data)

    query_runner = QueryRunner(config_file=f'{PROJECT_ROOT}/config.yaml')


    query = """
        DROP TABLE IF EXISTS tbl_analytics;
        CREATE TABLE tbl_analytics AS
        SELECT
            f.id,
            f.store,
            d.datetime,  -- Correctly refer to the datetime column from datetime_dim
            f.weekly_sales,
            h.holiday_flag_name,
            f.temperature,
            f.fuel_price,
            f.cpi,
            f.unemployment
        FROM
            fact_table f
        JOIN
            datetime_dim d ON f.datetime_id = d.datetime_id
        JOIN
            holiday_week_dim h ON f.holiday_flag_id = h.holiday_flag_id;
        """

    query_runner.run_query(query, fetch_results=False)



    return "string"
execute()