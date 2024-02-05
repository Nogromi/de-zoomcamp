from pandas import DataFrame
import pyarrow as pa
import pyarrow.parquet as pq
import os

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter
# update the variables below
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/src/de-zoomcamp-412419-db5fa3246433.json'
project_id = 'de-zoomcamp-412419'
bucket_name = 'mage-zoomcamp-anatolii-kryvko'
object_key = 'green_taxi.parquet'
table_name = 'green_taxi'
root_path = f'{bucket_name}/{table_name}'


@data_exporter
def export_data_to_google_cloud_storage(df: DataFrame, **kwargs) -> None:

    table = pa.Table.from_pandas(df)

    gcs = pa.fs.GcsFileSystem()

    pq.write_to_dataset(
        table,
        root_path=root_path,
        partition_cols=['lpep_pickup_date'],
        filesystem=gcs
    )