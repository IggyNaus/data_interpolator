import numpy as np
import xarray as xr
import pandas as pd

#this is Iggys job mostly

#want to define 5 classes: Nearest neighour, bilinear, IDW, unversal krgigging, and Barnes

class NearestNeighbour():
    #ds = the dataset that were using
    #gr = the new grid resolution wanted
    #nds = new interpolated ds
    def __init__(self,ds,lat,lon):
        self.ds = ds
        self.lat = lat
        self.lon = lon
    def Interpolate(self):
        nds = self.ds.sel(self.lat,self.lon,method='nearest')
        return nds

class Bilinear():
    #ds = the dataset that were using
    #lat,lon = the new grid resolution wanted
    #nds = new interpolated ds
    def __init__(self,ds,lat,lon):
        self.ds = ds
        self.lat = lat
        self.lon = lon
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

    LON, LAT = np.meshgrid(lons_fine, lats_fine)
    T = 300 - 0.5 * (LAT - 25) + 3 * np.sin(np.radians(LON + 100))
    T += np.random.default_rng(42).normal(0, 0.5, T.shape)

    ds_fine = xr.Dataset(
        {'t2m': (['lat', 'lon'], T, {'units': 'K'})},
        coords={'lat': lats_fine, 'lon': lons_fine}
    )

    ds_nn = NearestNeighbour(ds_fine, lats_coarse,lons_coarse)
    print(ds_nn)
    ds_bl = Bilinear(ds_fine, lats_coarse,lons_coarse)
    print(ds_bl)
