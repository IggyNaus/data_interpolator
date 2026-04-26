import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature

from data_interp.get_input_helper import get_inputs_helper

class Plotters():
    """
    Goal: Command-line Plotting for various layout styles without user writing code directly.
    Functions: 
        simple_plot - simple x vs y plot
        simple_map - simple map plot 
        simple layout - aims to automate certain layouts for the user, requiring only command line inputs to plot
            !!!Not all layouts will be covered by this!!! The simple plot, map, etc. can be combined individually by the user. 
    """
    def __init__(self,ds):
        self.ds = ds
        

    def simple_plot(self, ax, x, y):
        """
        Simple x-vs-y plot block.
        Plots, assumes title, sets standard xtick values, grid, and x/y label 
        
        Arguments:
            ax - axes to be plotted on
            x - x-axis variable
            y - y-axis variable 
        """
        ax.plot(self.ds[x], self.ds[y])
        ax.set_title((y + " vs. " + x))
        ax.set_xticks(ax.get_xticks(), ax.get_xticklabels(), rotation=25, ha='right')
        ax.grid()
        ax.set_ylabel(y)
        ax.set_xlabel(x)

    def simple_map(self, pass_ax, var_name, lat_range, lon_range, color_map = 'YlGnBu', transformation=ccrs.PlateCarree()):
        """
        Simple geographic plot. 
        ASSUMES LAT, LON ON -180 TO 180 RANGE! And, that Start < End.
        Plots on Plate Carree transformation, though this can be adjusted. 
        Position of colourbar may also need to be adjusted. Included is code to place it as needed. 
        
        Arguments:
            pass_ax - axes to be plotted on
            var_name - variable of interest
            lat_range - [start, end] pair  
            lon_range - [start, end] pair
            color_map - colormap code of choice 
            transformation - ccrs transformation type. Default is Plate Carree
        """
        lat_start = lat_range[0]
        lat_end = lat_range[1]
        lon_start = lon_range[0]
        lon_end = lon_range[1]

        etsAp = self.ds[var_name].plot(
            ax=pass_ax,
            transform=transformation,                # data is on regular lat/lon
            cmap=color_map,
            add_colorbar=True                        # To adjust to custom colourbar location, switch this to False   
        )
        pass_ax.set_extent([lat_start, lat_end, lon_start, lon_end], crs=transformation)
        # to enable custom colourbar placement, enable these lines:
        # cax = pass_ax.inset_axes([-0.28, 0.15, 0.02, 0.7]) 
        # fig.colorbar(etsAp, cax=cax, orientation='vertical')
        # cax.set_title(var_name,fontsize='small')
        pass_ax.coastlines(linewidth=0.8)
        pass_ax.set_title((var_name + " Plot"))
        pass_ax.set_ylabel("Latitude")
        pass_ax.set_xlabel("Longitude")
        pass_ax.add_feature(cfeature.BORDERS, linewidth=0.5, linestyle='--')
        pass_ax.add_feature(cfeature.LAND, facecolor='lightgray', alpha=0.3)
        pass_ax.gridlines(draw_labels=True, linewidth=0.5, alpha=0.5)
    
    

    def simple_layout(self, layout):
        """
        Aims to automate certain types of plot layout. Plotting functions can also be called independently for layouts not covered.
        Built on matplotlib subplot mosaic. 

        Available layouts: 
            simple map, code: 1m
            simple plot, code: 1p
            (1)/(1), (1x map over 1x map), code: 1m1m
            (1)/(2 - 2), (1x map over 2x simple plot), code: 1m2p 
            (2 - 2)/(1), (2x simple plot over 1x map), code: 2p1m
            (2 - 2)/(2 - 2) (2x2 simple plot), code 2p2p
        
        Arguments:
            layout - layout code. key provided above under available layouts

        """
        # I know user input like this isn't necessarily the best way to do it so revisit later?
        match layout:
            case "1m":
                get_input_helper(layout)
            case "1m1m":
