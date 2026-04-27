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
        ax.plot(x, y)
        # ax.set_title((y + " vs. " + x))
        ax.set_xticks(ax.get_xticks(), ax.get_xticklabels(), rotation=25, ha='right')
        ax.grid()
        #ax.set_ylabel(y)
        #ax.set_xlabel(x)

    def simple_map(self, pass_ax, var_name, lat_start, lat_end, lon_start, lon_end, colour_map = 'YlGnBu', transformation=ccrs.PlateCarree()):
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
        # lat_start = lat_range[0]
        # lat_end = lat_range[1]
        # lon_start = lon_range[0]
        # lon_end = lon_range[1]

        etsAp = self.ds[var_name].plot(
            ax=pass_ax,
            transform=transformation,                # data is on regular lat/lon
            cmap=colour_map,
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
    
    

    def simple_layout_maps(self, layout):
        """
        Aims to automate certain types of MAP PLOT layout. Plotting functions can also be called independently for layouts not covered.
        Built on matplotlib subplot mosaic. 

        Available layouts: 
            simple map, code: 1m
            (1)/(1), (1x map over 1x map), code: 1m1m
                AA
                BB
            (1)/(1)/(1)/(1)/(1), (5x map), code: 5m
                AA
                BB
                CC
                DD
                EE
                - ideal for showcasing all methods 
        
        Arguments:
            layout - layout code. key provided above under available layouts

        """
        # I know user input like this isn't necessarily the best way to do it so revisit later?
        match layout:
            case "1m":
                (var_name, lat_start, lat_end, lon_start, lon_end, colourmap) = get_inputs_helper(layout)
                fig, ax = plt.subplots(figsize=(2, 2), layout='constrained')
                self.simple_map(ax, var_name, lat_start, lat_end, lon_start, lon_end, colour_map=colourmap)
            case "1m1m":
                (var_name1, lat_start1, lat_end1, lon_start1, lon_end1, colourmap1,
                var_name2, lat_start2, lat_end2, lon_start2, lon_end2, colourmap2) = get_inputs_helper(layout)
                # Debug:
                # print(f"First map, variable: {var_name1}")
                # print(f"First map, latitude start: {lat_start1}")
                # print(f"First map, latitude end: {lat_end1}") 
                # print(f"First map, longitude start: {lon_start1}") 
                # print(f"First map, longitude end: {lon_end1}") 
                # print(f"First map, colourmap: {colourmap1}")
                # print(f"Second map, variable: {var_name2}")
                # print(f"Second map, latitude start: {lat_start2}")
                # print(f"Second map, latitude end: {lat_end2}") 
                # print(f"Second map, longitude start: {lon_start2}") 
                # print(f"Second map, longitude end: {lon_end2}") 
                # print(f"Second map, colourmap: {colourmap2}")
                

                axes = plt.figure(layout="constrained").subplot_mosaic(
                    """
                    AA
                    BB
                    """,
                    height_ratios=[1, 1],
                    subplot_kw=dict(projection=ccrs.PlateCarree())
                )
                self.simple_map(pass_ax=axes["A"], var_name=var_name1, lat_start=lat_start1, 
                lat_end=lat_end1, lon_start=lon_start1, lon_end=lon_end1, colour_map=colourmap1)
                self.simple_map(pass_ax=axes["B"], var_name=var_name2, lat_start=lat_start2, 
                lat_end=lat_end2, lon_start=lon_start2, lon_end=lon_end2, colour_map=colourmap2)
                plt.savefig((var_name1 + "_and_" + var_name2+"_1m1m.png"),dpi=250,bbox_inches='tight')
            
    def simple_layout_plots(self, layout, x1=None, y1=None, x2=None, y2=None):
        """
        Aims to automate certain types of plot layout. Plotting functions can also be called independently for layouts not covered.
        Built on matplotlib subplot mosaic. 

        Available layouts: 
            simple map, code: 1m
            simple plot, code: 1p
            (1)/(1), (1x map over 1x map), code: 1m1m
                AA
                BB
            (1)/(2 - 2), (1x map over 2x simple plot), code: 1m2p 
                AA
                BC
            (2 - 2)/(1), (2x simple plot over 1x map), code: 2p1m
                BC
                AA
            (2 - 2)/(2 - 2) (2x2 simple plot), code: 2p2p
                AB
                CD
            (1)/(1)/(2 - 2) (1x map over 1x map over 2x simple plot), code: 1m1m2p
                AA
                BB
                CD
                - ideal for comparing two different methods and errors etc
            (1)/(1)/(1)/(1)/(1), (5x map), code: 5m
                AA
                BB
                CC
                DD
                EE
                - ideal for showcasing all methods 
        
        Arguments:
            layout - layout code. key provided above under available layouts
            x1, y1, x2, y2: numpy nd.arrays to be plotted 
        """
        match layout:
            case "1m":
                self.simple_layout_maps("1m")
            case "1m1m":
                self.simple_layout_maps("1m1m")
            case "1p":
                if (x1 is None) or (y1 is None):
                    raise ValueError("Please enter valid x1, y1")
                fig,ax = plt.subplots(figsize=(2, 2), layout='constrained')
                self.simple_plot(ax,x1,y1)
                plt.savefig((y1 + "_vs_" + x1+"_1p.png"),dpi=250,bbox_inches='tight')
            case "1p1p":
                if (x1 is None) or (y1 is None) or (x2 is None) or (y2 is None):
                    raise ValueError("Please enter valid x1, y1, x2, y2")
                axes = plt.figure(layout="constrained").subplot_mosaic(
                    """
                    AA
                    BB
                    """,
                    height_ratios=[1, 1],
                )
                self.simple_plot(axes["A"], x1, y1)
                self.simple_plot(axes["B"], x2, y2)
                plt.savefig((y1 + "_vs_" + x1 + "_and_" + y2 + "_vs_" + x2+"_1p1p.png"),dpi=250,bbox_inches='tight')
            case "2p1m":
                if (x1 is None) or (y1 is None) or (x2 is None) or (y2 is None):
                    raise ValueError("Please enter valid x1, y1, x2, y2")
                axes = plt.figure(layout="constrained").subplot_mosaic(
                    """
                    AC
                    BB
                    """,
                    height_ratios=[1, 2],
                    per_subplot_kw={"B": dict(projection=ccrs.PlateCarree())}
                )
                self.simple_plot(axes["A"], x1, y1)
                # axes["A"].set
                self.simple_plot(axes["C"], x2, y2)
                (var_name, lat_start, lat_end, lon_start, lon_end, colourmap) = get_inputs_helper("1m")
                self.simple_map(axes["B"], var_name, lat_start, lat_end, lon_start, lon_end, colour_map=colourmap)
                return axes
            case "1m1m2p":
                if (x1 is None) or (y1 is None) or (x2 is None) or (y2 is None):
                    raise ValueError("Please enter valid x1, y1, x2, y2")
                # plot_mosaic = [
                #     ["plot A"], ["plot B"],
                # ]
                # map_mosaic = [
                #     [plot_mosaic],
                #     ["B"],
                #     ["C"]
                # ]
                axes_1m1m2p = plt.figure(layout='constrained').subplot_mosaic(
                    # map_mosaic,
                    # layout="constrained"
                    """
                    ACC
                    BDD
                    """,
                    height_ratios=[2,2],
                    width_ratios=[1,1,2],
                    per_subplot_kw={("C", "D"): dict(projection=ccrs.PlateCarree())}
                )
                
                self.simple_plot(axes_1m1m2p["A"], x1, y1)
                # axes["A"].set
                self.simple_plot(axes_1m1m2p["B"], x2, y2)
                (var_name1, lat_start1, lat_end1, lon_start1, lon_end1, colourmap1,
                var_name2, lat_start2, lat_end2, lon_start2, lon_end2, colourmap2) = get_inputs_helper("1m1m")
                self.simple_map(pass_ax=axes_1m1m2p["C"], var_name=var_name1, lat_start=lat_start1, 
                lat_end=lat_end1, lon_start=lon_start1, lon_end=lon_end1, colour_map=colourmap1)
                self.simple_map(pass_ax=axes_1m1m2p["D"], var_name=var_name2, lat_start=lat_start2, 
                lat_end=lat_end2, lon_start=lon_start2, lon_end=lon_end2, colour_map=colourmap2)
                return axes_1m1m2p

                






            
                
            




if __name__ == "__main__":
    import datetime
    from data_interp.dataset import dataset_read_nc, dataset_read_csv
    
    cam_data = dataset_read_nc("../data_interpolator/sample_data_camulator.nc")
    
    # extent: [-20, 40, 35, 65]
    # var: PRECT
    
    cam_data.coords['longitude'] = (cam_data.coords['longitude'] + 180) % 360 - 180
    cam_data = cam_data.sortby(cam_data.longitude)

    cam_data_timenonsAvg = cam_data.mean(dim='time')
    # plot_test = Plotters(cam_data_timenonsAvg)
    # plot_test.simple_layout_maps("1m1m")

    cam_data_spatialAvg = cam_data['PRECT'].mean(dim=['latitude','longitude'])
    cam_data_timeAvg = cam_data_spatialAvg.mean(dim='time')
    x1_str=cam_data['time'].dt.strftime("%m/%d/%Y")
    x1_ticks = x1_str[::10]
    y1 = cam_data_spatialAvg

    y2 = cam_data_spatialAvg = cam_data['TREFHT'].mean(dim=['latitude','longitude'])

    
    plot_2p1m = Plotters(cam_data_timenonsAvg)
    # axes = plot_2p1m.simple_layout_plots("2p1m", x1_str, y1, x1_str, y2)
    # axes["A"].set_title("Spatial Average Time Series")
    # axes["A"].set_ylabel("PRECT")
    # axes["C"].set_title("Spatial Average Anomaly")
    # axes["C"].set_ylabel("PRECT Anomaly")
    # plt.savefig("PRECT_2p1m.png", dpi=250, bbox_inches='tight')
    
    axes = plot_2p1m.simple_layout_plots("1m1m2p", x1_str, y1, x1_str, y2)
    axes["A"].set_title("PRECT Spatial Average")
    axes["A"].set_ylabel("PRECT")
    axes["A"].set_xticks(x1_ticks)
    axes["B"].set_title("TREFHT Spatial Average")
    axes["B"].set_ylabel("PRECT Anomaly")
    plt.savefig(("PRECT_and_TREFHT" + "_1m1m2p.png"),dpi=250,bbox_inches='tight')

