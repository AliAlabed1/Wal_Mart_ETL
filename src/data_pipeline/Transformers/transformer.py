import os
import pandas as pd
import sys

# Add the directory containing the `src` folder to the Python path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "../"))  # Adjust to reach `src`
sys.path.append(PROJECT_ROOT)

from utils.logging_utils import app_logger


current_path = os.getcwd()
worksapce = current_path.split('src')[0]

class Transformer():
    def transform(self,df:pd.DataFrame):
        """
        Transforms the input DataFrame and returns a new DataFrame.

        Args:
            - df (pd.DataFrame): The input DataFrame to transform.

        Returns:
            - pd.DataFrame: The transformed DataFrame.

        Rises:
            - TypeError: If the df is not a dataframe.
            - ValueError: If the df df is None.
        """
        if df is None:
            app_logger.error("The df is None")
            raise ValueError("The loaded df is None.")
        # if isinstance(df, pd.DataFrame):
        #     app_logger.error("The given df is not  a data frame")
        #     raise TypeError("The given df is not a data frame")
        
        df['id'] = df.index


        df['Date'] = pd.to_datetime(df['Date'],format='%d-%m-%Y')
        datetime_dim = df[['Date']].reset_index(drop=True)
        datetime_dim['datetime'] = datetime_dim['Date']
        datetime_dim['day'] = datetime_dim['datetime'].dt.day
        datetime_dim['month'] = datetime_dim['datetime'].dt.month
        datetime_dim['year'] = datetime_dim['datetime'].dt.year
        datetime_dim['datetime_id'] = datetime_dim.index
        datetime_dim = datetime_dim[['datetime_id', 'datetime', 'day', 'month', 'year']]
        week_holiday_type = {
            1 :"special holiday week",
            0 : "Holiaday Week"
        }
        
        holiday_week_dim = df[['Holiday_Flag']].reset_index(drop=True)
        holiday_week_dim['holiday_flag_id'] = holiday_week_dim.index
        holiday_week_dim['holiday_flag_name'] = holiday_week_dim['Holiday_Flag'].map(week_holiday_type)


        fact_table = df.merge(datetime_dim,left_on='id',right_on='datetime_id')\
             .merge(holiday_week_dim,left_on='id',right_on='holiday_flag_id')\
             [[
                 'id','Store','datetime_id','Weekly_Sales','holiday_flag_id','Temperature','Fuel_Price',
                 'CPI','Unemployment',
             ]]
        
        app_logger.info("DF is transformed successfully.")
        return{
            'datetime_dim':datetime_dim.to_dict(orient="dict"),
            'holiday_week_dim':holiday_week_dim.to_dict(orient="dict"),
            'fact_table':fact_table.to_dict(orient="dict"),
        }


# Test the Class and main Funcation 
if __name__ == "__main__":
    itransform = Transformer()
    df = itransform.transform(pd.DataFrame())

