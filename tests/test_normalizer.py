import pandas as pd
from src.normalizer import Normalizer
from src.excel_reader import ExcelReader

def test_convert_to_datetime():
    """
    Test convert_to_datetime function on synthetic data
    :return:
    """
    data = {
        'Agent_Name': ['John Doe', 'Alice Smith', 'Bob Johnson'],
        'Commission_Period': ['2024-06', '2024-05', 'invalid_date'],
        'Policy_Effective_Date': ['2024-05-01', '2023-06-15', '2022-07-20'],
        'Commission_Amount': [500.00, 750.00, 800.00],
        'Other_Info': ['N/A', 'N/A', 'N/A']
    }

    df = pd.DataFrame(data)
    normalizer = Normalizer(df)
    df_converted = normalizer.convert_to_datetime()

    assert pd.api.types.is_datetime64_any_dtype(df_converted['Commission_Period'])
    assert pd.isna(df_converted.loc[2, 'Commission_Period'])
    assert df_converted['Agent_Name'].dtype == 'object'
    assert df_converted['Commission_Amount'].dtype == 'float64'


def test_convert_to_datetime_on_real_data():
    """
    Test convert_to_datetime function on real data
    :return:
    """

    file_paths = [
        'data/Centene%2006.2024%20Commission.xlsx',
        'data/Emblem%2006.2024%20Commission.xlsx',
        'data/Healthfirst%2006.2024%20Commission.xlsx'
    ]

    excel_reader = ExcelReader(file_paths)
    dataframes = excel_reader.dataframes


    normalizer_centene = Normalizer(dataframes['centene'])
    df_converted_centene = normalizer_centene.convert_to_datetime()
    assert pd.api.types.is_datetime64_any_dtype(df_converted_centene['Pay Period'])
    assert pd.api.types.is_datetime64_any_dtype(df_converted_centene['Signed Date'])
    assert pd.api.types.is_datetime64_any_dtype(df_converted_centene['Effective Date'])
    assert pd.api.types.is_datetime64_any_dtype(df_converted_centene['Original Effective Date'])
    assert pd.api.types.is_datetime64_any_dtype(df_converted_centene['Member Term Date'])


    normalizer_healthfirst = Normalizer(dataframes['healthfirst'])
    df_converted_healthfirst = normalizer_healthfirst.convert_to_datetime()
    assert pd.api.types.is_datetime64_any_dtype(df_converted_healthfirst['Member Effective Date'])
    assert pd.api.types.is_datetime64_any_dtype(df_converted_healthfirst['Period'])
    assert df_converted_healthfirst['Member ID'].dtype == 'int64'


    normalizer_emblem = Normalizer(dataframes['emblem'])
    df_converted_emblem = normalizer_emblem.convert_to_datetime()
    assert pd.api.types.is_datetime64_any_dtype(df_converted_emblem['Effective Date'])
    assert pd.api.types.is_datetime64_any_dtype(df_converted_emblem['Term Date'])
    assert df_converted_emblem['Member ID'].dtype == 'int64'
    assert df_converted_emblem['Payee Name'].dtype == 'object'









