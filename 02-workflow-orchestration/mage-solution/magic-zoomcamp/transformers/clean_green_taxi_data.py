from pandas import DataFrame

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    print(f"Preprocessing: original dataframe size: {data.shape[0]}")
    non_zero_passengers = data[data['passenger_count']>0]  
    print(f"Preprocessing: records non zero passengers: {non_zero_passengers.shape[0]}")
    non_zero_distance = non_zero_passengers[non_zero_passengers['trip_distance']>0]
    print(f"Preprocessing: records with non zero passengers and distance: {non_zero_distance.shape[0]}")
    print(non_zero_distance.columns)
    non_zero_distance['lpep_pickup_date'] = non_zero_distance['lpep_pickup_datetime'].dt.date
    non_zero_distance.columns = (non_zero_distance.columns
                .str.replace('(?<=[a-z])(?=[A-Z])', '_', regex=True)
                .str.lower()
             )
    return non_zero_distance    




@test
def test_vendor_id(output, *args) -> None:
    """
    id must be in [1,2] according to the documentation
    https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_green.pdf

   1= Creative Mobile Technologies, LLC; 2= VeriFone Inc

    """
    assert output['vendor_id'].isin([1, 2]).all()

@test
def test_passenger_count(output, *args) -> None:
    """
    check if all samples have passenger_count>0 .
    """
    assert (output['passenger_count']>0).all()


@test
def test_trip_distance(output, *args) -> None:
    """
    check if all samples have passenger_count>0 .
    """
    assert (output['passenger_count']>0).all()
    
