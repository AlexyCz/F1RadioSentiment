""" UTILS MODULE: Provides non-business logic resuable functions """
import pandas as pd


def concatenate_dataframes(x_df: pd.DataFrame, y_df: pd.DataFrame):
    """
    Returns a pandas concatenated dataframe given inputs with `ignore_index`
        set to true.

    return: DataFrame
    """
    return pd.concat([x_df, y_df], ignore_index=True)


def standardize_with_microseconds(row: pd.Series, column: str):
    """
    Returns an updated pandas series representing the input row of data
        and timestamp extended column date data.

    return: Series
    """
    if "." not in row[column]:
        row[column] = row[column].replace("+00:00", ".000000+00:00")
        return row
    return row


def convert_to_dt(x_df: pd.DataFrame, column: str):
    """
    Returns a dataframe with input column converted to microsecond timestamped
        datatime format.

    return: DataFrame
    """
    x_df[column] = pd.to_datetime(x_df[column], format="%Y-%m-%dT%H:%M:%S.%f%z")
    return x_df
