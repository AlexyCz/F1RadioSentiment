""" UTILS MODULE: Provides non-business logic resuable functions """
import pandas as pd


def concatenate_dataframes(x_df: pd.DataFrame, y_df: pd.DataFrame):
    return pd.concat([x_df, y_df], ignore_index=True)


def standardize_with_microseconds(row: pd.Series, column: str):
    if "." not in row[column]:
        row[column] = row[column].replace("+00:00", ".000000+00:00")
        return row
    return row


def convert_to_dt(x_df: pd.DataFrame, column: str):
    x_df[column] = pd.to_datetime(x_df[column], format="%Y-%m-%dT%H:%M:%S.%f%z")
    return x_df
