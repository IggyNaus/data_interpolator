import numpy as np
import xarray as xr
import pandas as pd

#this is Iggys job mostly

#want to define 5 classes: Nearest neighour, bilinear, IDW, unversal krgigging, and Barnes

class NearestNeighbour():
    #ds = the dataset that were using
    #gr = new grid resolution, tuple of a lat & lon
    #nds = new interpolated dataset
    def __init__(self,ds,gr):
        self.ds = ds
        self.gr = gr
        try:
            self.lat = gr[0]
            self.lon = gr[1]
        except IndexError:
            text = 'wrong grid resolution input, please input a tuple with lat & lon'
            return print(text)

    def Interpolate(self):
        try:
            if self.ds == pd.DataFrame():
                nds = self.ds.interpolate(method='nearest')
            else:    
                nds = self.ds.sel(self.lat,self.lon,method='nearest')
            return nds
        except TypeError:
            text = 'wrong dataset input, please input a pd.DataFrame or xr.DataArray'
            return print(text)

class Bilinear():
    #ds = the dataset that were using
    #gr = new grid resolution, tuple of a lat & lon
    #nds = new interpolated dataset
    def __init__(self,ds,gr):
        self.ds = ds
        try:
            self.lat = gr[0]
            self.lon = gr[1]
        except IndexError:
            text = 'wrong grid resolution input, please input a tuple with lat & lon'
            return print(text)
        
    def Interpolate(self):
        nds = self.ds.interp(self.lat,self.lon)
        return nds

#IDW:
#   need: data, new grid resolution, power parameter (has default), nearest neighbour vs. full sample (defaultss to nn)

#krigging:
#   need: data, new grid resolution, semivariogram

#Barnes:
#   need: data, new grid resolution

#if name == __main__: tests above methods for test case
if __name__ == "__main__":
    lats_fine = np.arange(25, 50, 0.5)
    lons_fine = np.arange(-120, -70, 0.5)

    lats_coarse = np.arange(26, 50, 2.0)
    lons_coarse = np.arange(-119, -70, 2.0)
    new_grid = [lats_coarse, lons_coarse]

    LON, LAT = np.meshgrid(lons_fine, lats_fine)
    T = 300 - 0.5 * (LAT - 25) + 3 * np.sin(np.radians(LON + 100))
    T += np.random.default_rng(42).normal(0, 0.5, T.shape)

    ds_fine = xr.Dataset(
        {'t2m': (['lat', 'lon'], T, {'units': 'K'})},
        coords={'lat': lats_fine, 'lon': lons_fine}
    )

    ds_nn = NearestNeighbour(ds_fine, new_grid)
    print(ds_nn)
    ds_bl = Bilinear(ds_fine, new_grid)
    print(ds_bl)
