# Data Interpolator Final Project
A versatile package that features robust and flexible dataset creation, a variety of interpolation methods for users to pick from, and high-quality plotting support. 

---

## Overview

---
## Package Structure

```
data_interpolator/
├── data_interp/     
│   ├── __init__.py         
│   ├── dataset.py           # getting the dataset
│   ├── get_input_helper.py  
│   ├── interpolators.py     # where the interpolator classes are
│   ├── main.py              
│   └── plotting.py          # plottig functions and utility
├── README.MD
└── pyproject.toml
```

---

## Instalation

---

## dataset.py → Handling of various data types. Configuring csvs, netcdfs, and import/export of data. 
Goal: to be able to select across a wide variety of data input methods and return netcdf files from apis, ftp file systems, https sources, local uploads, etc. (Will be the meat of the project)
User-specified input data type, turn CSV to pd dataframe, turn NetCDF to xr data array, etc. 
Export data to local files. This has an optional double use as a standalone file converter, for users to grab files and download them even if they do not end up using the rest of the project. 

## interpolators.py→ Defines classes that take a data array and return a data array interpolated to a specified grid

Nearest neighbour class
-takes in a xr.Dataset or pd.DataFrame and a tuple of the new grid size and returns a xr.Dataset with the specified grid size.

Bilinear class
-takes in a xr.Dataset or pd.DataFrame and a tuple of the new grid size and returns a xr.Dataset with the specified grid size.

IDW class 
-takes in a xr.Dataset or pd.DataFrame and a tuple of the new grid size and returns a pd.DataFrame with the specified grid size.

kriging class
-takes in a xr.Dataset or pd.DataFrame and a tuple of the new grid size and returns a pd.DataFrame with the specified grid size.

Barnes class
-takes in a xr.Dataset or pd.DataFrame and a tuple of the new grid size and returns a pd.DataFrame with the specified grid size.

if __name__ == main tests to make sure an equivalent dataframe and dataset will give same result.

---

## plotting.py → Uses one of the interpolators to give a plot of the new grid
Which interpolator() → lets user choose which interpolator, defaults to NN
plotting() → plots interpolated grid

## driver.py → Main function
Dataset input examples
Plotting and Interpolation exams
In-code user guide, intended to be edited by users to their needs

## Dependencies

---

## Authors

Made by Skai Glasser & Iggy Naus.

---



