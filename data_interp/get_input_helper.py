import cartopy.crs as ccrs

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
    var_name = map_var
    lat_start, lat_end, lon_start, lon_end = map_lat_long()
    return (var_name, lat_start, lat_end, lon_start, lon_end)

def colourmap_helper():
    """
    Colourmap code helper. Provides user a list of acceptable maps. 

    """
    colourmap = "YlGnBu"
    cmap = str(input("Custom Colourmap? (Enter [Y/N]): "))
    if ((cmap == "Y") or (cmap == "y")):
        print(f"Available colourmaps can be found here: https://matplotlib.org/stable/gallery/color/colormap_reference.html")
        colourmap = input("Please input desired colourmap name: ")
    elif ((cmap == "N") or (cmap == "n")):
        pass
    else:
        raise ValueError("Incorrect colourmap input (Correct inputs: Y, y, N, n)")
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
            identicalVar = input("Second map - Plot same variable as before?")
