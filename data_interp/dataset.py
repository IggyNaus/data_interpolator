# Implement csv, netcdf, xarray, pandas conversions
 

import numpy as np
import pandas as pd
import xarray as xr


# first q: file path?
input_file_path = "in_file.txt"
output_file_path = "out_file.txt"

def df_get_col_names(df):
    """
    Returns a list of column names from imported DFs
    """
    names = df.columns.tolist()
    return names

def skywatch_df_datetime(df):
    """
    From Lab6 given code, formats data from ATOC Skywatch Laboratory 
    """
    timeName = input("Please enter name of time column: ")
    dateName = input("Please enter name of date column: ")
    time = (
        df[timeName].astype(str)
        .str.strip()
        .str.replace(r"a$", "AM", regex=True)
        .str.replace(r"p$", "PM", regex=True)
    )
    date = pd.to_datetime(df[dateName].astype(str).str.strip() + " " + t,format="%m/%d/%y %I:%M%p",errors="coerce")
    df = df.set_index(dt).drop(columns=[dateName, timeName])
    df.index.name = "datetime"
    df.columns = [
        "_".join([str(a).strip(), str(b).strip()]).replace(" ", "_").strip("_")
        for a, b in df.columns
    ]
    return df

def dataset_read_csv(file_name):
    """
    Imports csvs as Pandas DFs
    Has users dynamically select correct time and date columns 
    Then coerces standard formatting on date and time columns
    """
    read_file_name = file_name # URL or local path
    df = pd.read_csv(read_file_name, header=[0, 1]) # adjust this as necessary for specific CSVs

    names = df_get_col_names(df)
    print(f"Imported DF with Columns: {names}") 
    
    # Instead of assuming naming conventiosn or trying to search for times and dates directly, have user specify
    print(f"ATOC SKYWATCH: Try to coerce date and time format?")
    formatted = False
    while not(formatted):
        format = input("[y / n]: ")
        if (format == "y") | (format == "Y"): 
            format_df_datetime(df)
        elif (format == "n") | (format == "N"):
            break
        else: 
            print(f"Invalid input, please try again.")
            continue

    return df


def dataset_read_nc(file_name):
    xar = xr.open_dataset(file_name)
    return xar



if __name__ == "__main__":
    from pathlib import Path
    INfile_path = Path("..").joinpath("data_interpolator").joinpath("filtered-copy-fixed-crop.csv")
    OUTfile_path = Path("..").joinpath("data_interpolator").joinpath("test_output.nc")
    df = dataset_read_csv(INfile_path)

    INfile_path = Path("..").joinpath("data_interpolator").joinpath("sample_data_camulator.nc")
#ATOC_4815/data_interpolator/filtered-copy-fixed-crop.csv