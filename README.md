# Data Interpolator Final Project
A versatile package that features robust and flexible dataset creation, a variety of interpolation methods for users to pick from, and high-quality plotting support. Below has ideas and first draft concepts for the functions we would like to implement.


## dataset.py → Handling of various data types. Configuring csvs, netcdfs, and import/export of data. 
Goal: to be able to select across a wide variety of data input methods and return netcdf files from apis, ftp file systems, https sources, local uploads, etc. (Will be the meat of the project)
User-specified input data type, turn CSV to pd dataframe, turn NetCDF to xr data array, etc. 
Export data to local files. This has an optional double use as a standalone file converter, for users to grab files and download them even if they do not end up using the rest of the project. 

## interpolators.py→ Defines classes that take a data array and return a data array interpolated to a specified grid
https://iri.columbia.edu/~rijaf/CDTUserGuide/html/interpolation_methods.html
Nearest neighbour → Class
Set output grid size() → lets user put in grid size
NN interpolation() → have xarray do it :D
Quality control () → checks against value
Bilinear → class
Set output grid size() → lets user put in grid size
Bilinear interpolation() →have xarray do it :D
Quality control () → checks against value
IDW → Class 
https://pro.arcgis.com/en/pro-app/latest/tool-reference/geostatistical-analyst/idw.htm,https://en.wikipedia.org/wiki/Inverse_distance_weighting
Set power parameter() → lets user put in power parameter(can't be <1), defaults to 1.
Set output grid size() → lets user put in grid size 
Full sample() → lets user choose between nearest neighbour and full sample, defaults to nearest neighbour
IDW interpolation()→ uses above get new grid
Quality control () → checks against value
kriging → Class
https://pro.arcgis.com/en/pro-app/3.4/tool-reference/3d-analyst/how-kriging-works.htm,https://en.wikipedia.org/wiki/Kriging
Semiveriogram() →
Set output grid size() → lets user put in grid size 
kriging interpolation()→
Quality control () → checks against value
Barnes → Class
https://en.wikipedia.org/wiki/Barnes_interpolation
Set output grid size() → lets user put in grid size 
Barnes interpolation()→
Quality control () → checks against value
If name == __main__ → test above 

## plotting.py → Uses one of the interpolators to give a plot of the new grid
Which interpolator() → lets user choose which interpolator, defaults to NN
plotting() → plots interpolated grid

## driver.py → Main function
Dataset input examples
Plotting and Interpolation exams
In-code user guide, intended to be edited by users to their needs


