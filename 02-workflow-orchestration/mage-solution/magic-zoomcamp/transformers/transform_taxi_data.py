if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    zero_passengers = data['passenger_count'].isin([0]).sum()
    print(f"Preprocessing: records with zero passengers: {zero_passengers}")

    non_zero_passengers = data[data['passenger_count']>0]
    print(f"Preprocessing: records with non zero passengers: {non_zero_passengers.shape[0]}")

    return non_zero_passengers


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'


@test
def test_size_zero_passenger(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output['passenger_count'].isin([0]).sum()==0 , 'There are rides with 0 passenger'
