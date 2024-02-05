from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from os import path
import pyarrow as pa
import pyarrow.parquet as pq
from pandas import DataFrame

import os
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_from_google_cloud_storage(*args, **kwargs):
    """
    Template for loading data from a Google Cloud Storage bucket.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#googlecloudstorage
    """
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    bucket_name = 'mage-zoomcamp-anatolii-kryvko'

    object_key = 'your_object_key'

    return GoogleCloudStorage.with_config(ConfigFileLoader(config_path, config_profile)).load(
        bucket_name,
        object_key,
    )


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/src/de-zoomcamp-412419-db5fa3246433.json'
project_id = 'de-zoomcamp-412419'
bucket_name = 'mage-zoomcamp-anatolii-kryvko'
object_key = 'green_taxi.parquet'
table_name = 'green_taxi'
root_path = f'{bucket_name}/{table_name}'

@data_loader
def read_data_from_google_cloud_storage(root_path: str) -> pa.Table:
    gcs = pa.fs.GcsFileSystem()

    # List the files in the root path
    file_info = gcs.get_file_info(root_path)
    print("file_info",file_info)
    # Get the file paths
    file_paths = [f.path for f in file_info]
    print("file_paths",file_paths)
    # Read the Parquet files into a PyArrow Table
    table = pq.read_table(file_paths, filesystem=gcs)

    return table

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
