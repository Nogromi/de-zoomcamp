import io
import pandas as pd
import requests

import pandas as pd
import requests
from io import BytesIO
import warnings
import os 


if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    parquet_dfs = {}

    # Suppress warnings temporarily
    # with warnings.catch_warnings():
    #     warnings.simplefilter("ignore")
        
    months = [f'{i:02}' for i in range(1, 13)]
    full_df = pd.DataFrame()


    # parse_dates_green_taxi = ['lpep_pickup_datetime', 'lpep_dropoff_datetime']

    for mon in months: 
        url = f'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2022-{mon}.parquet'
        df = pd.read_parquet(url)
        full_df = pd.concat([full_df, df], ignore_index=True)
        print(mon, df.shape, "full:", full_df.shape)

    
    print(full_df.info())

    return full_df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
