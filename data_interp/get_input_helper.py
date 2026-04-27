import cartopy.crs as ccrs


def basic_plot_inputs():
    x = input("Please input independent variable: ")
    y = input("Please input dependent variable: ")
    return (x, y)


def map_lat_long(): 
    """
    Basic lat & long start and end input and validation block

    """
    lat_start = float(input("Please enter start latitude: "))
    lat_end = float(input("Please enter end latitude: "))
    lon_start = float(input("Please enter start longitude: "))
    lon_end = float(input("Please enter end longitude: "))
                
    # Type Check
    if not(
        (str(type(lat_start)) == "<class 'float'>")
        and (str(type(lat_end)) == "<class 'float'>")
        and (str(type(lon_start)) == "<class 'float'>")
        and (str(type(lon_end)) == "<class 'float'>")
        ):
        raise TypeError("Latitude & Longitude start AND end must be floats.")

    # Start and End value guard for plotting methods
    assert lat_start < lat_end, "Latitude start must be smaller than latitude end"
    assert lon_start < lon_end, "Longitude start must be smaller than longitude end"

    return (lat_start, lat_end, lon_start, lon_end)

def map_var():
    """
    Grabs variable to be plotted

    """
    var_name = input("Please enter target variable: ")      
    # Type Check
    if not(
        (str(type(var_name)) == "<class 'str'>")
        ):
        
        raise TypeError("Variable name should be a valid string.")
    return var_name



def basic_map_inputs():
    """
    Collects verified variable name and map range and returns them as a tuple 

    """
    var_name = map_var()
    lat_start, lat_end, lon_start, lon_end = map_lat_long()
    return (var_name, lat_start, lat_end, lon_start, lon_end)

# def addt_map_inputs(identicalVar, identicalRange):
#     """
#     Determines what information to collect from user based on what is shared with first plot

#     """
#     if identicalVar: 
#         pass
#     else:
#         var_2 = map_var()
    
#     if identicalRange: 
#         pass
#     else: 
#         lat_start_2, lat_end_2, lon_start_2, lon_end_2 = map_lat_long()



def colourmap_helper():
    """
    Colourmap code helper. Provides user a list of acceptable maps. 

    """
    colourmap = "YlGnBu"
    cmap = str(input("Custom Colourmap? (Enter [Y/N]): "))
    if ((cmap == "Y") or (cmap == "y") or (cmap == "Yes") or (cmap == "yes")):
        print(f"Available colourmaps can be found here: https://matplotlib.org/stable/gallery/color/colormap_reference.html")
        colourmap = input("Please input desired colourmap name: ")
    elif ((cmap == "N") or (cmap == "n") or (cmap == "No") or (cmap == "no")):
        pass
    else:
        raise ValueError("Incorrect colourmap input (Correct inputs: Y, y, N, n, Yes, yes, No, no)")
    return colourmap


def get_inputs_helper(layout_code):
    """
    Internal helper function to streamline getting inputs in plotting.py
    
    """
    match layout_code:
        case "1m":
            # pass_ax, var_name, lat_range, lon_range, color_map = 'YlGnBu', transformation=ccrs.PlateCarree()
            var_name, lat_start, lat_end, lon_start, lon_end = basic_map_inputs()
            colourmap = colourmap_helper()

            return var_name, lat_start, lat_end, lon_start, lon_end, colourmap
        case "1m1m":
            #first map: 
            var_name1, lat_start1, lat_end1, lon_start1, lon_end1 = basic_map_inputs()
            colourmap1 = colourmap_helper()

            #second map:
            identicalVar = input("Second map - Plot identical variable? [Y/N]: ")
            if ((identicalVar == "Y") or (identicalVar == "y") or (identicalVar == "Yes") or (identicalVar == "yes")):
                var_name2 = var_name1
            elif ((identicalVar == "N") or (identicalVar == "n") or (identicalVar == "No") or (identicalVar == "no")):
                var_name2 = map_var()
            else:
                raise ValueError("Incorrect input (Correct inputs: Y, y, N, n, Yes, yes, No, no)")
            
            identicalRange = input("Second map - Use identical range? [Y/N]: ")
            if ((identicalRange == "Y") or (identicalRange == "y") or (identicalRange == "Yes") or (identicalRange == "yes")):
                lat_start2 = lat_start1 
                lat_end2 = lat_end1 
                lon_start2 = lon_start1 
                lon_end2 = lon_end1
            elif ((identicalRange == "N") or (identicalRange == "n") or (identicalRange == "No") or (identicalRange == "no")):
                lat_start2, lat_end2, lon_start2, lon_end2 = map_lat_long()
            else:
                raise ValueError("Incorrect input (Correct inputs: Y, y, N, n, Yes, yes, No, no)")

            identicalColourMap = input("Second map - Use identical colourmap? [Y/N]: ")
            if ((identicalColourMap == "Y") or (identicalColourMap == "y") or (identicalColourMap == "Yes") or (identicalColourMap == "yes")):
                colourmap2 = colourmap1
            elif ((identicalColourMap == "N") or (identicalColourMap == "n") or (identicalColourMap == "No") or (identicalColourMap == "no")):
                colourmap2 = colourmap_helper()
            else:
                raise ValueError("Incorrect input (Correct inputs: Y, y, N, n, Yes, yes, No, no)")
            
            return (var_name1, lat_start1, lat_end1, lon_start1, lon_end1, colourmap1, var_name2, lat_start2, lat_end2, lon_start2, lon_end2, colourmap2)
        case "1p":
            x, y = basic_plot_inputs()
            return x, y

