# Implement csv, netcdf, xarray, pandas conversions
 

import numpy as np
import pandas as pd
import xarray as xr


# first q: file path?
input_file_path = "in_file.txt"
output_file_path = "out_file.txt"

def text_input_filepath(in_file_name, out_file_name):
    input_file_path = file_name
    output_file_path = out_file_name




if __name__ == "__main__":
    from pathlib import Path
    INfile_path = Path("..").joinpath("data_interpolator").joinpath("sample_data_camulator.nc")
    OUTfile_path = Path("..").joinpath("data_interpolator").joinpath("test_output.nc")
