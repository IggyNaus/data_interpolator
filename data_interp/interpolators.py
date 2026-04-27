import numpy as np
import xarray as xr
import pandas as pd

import pykrige.kriging_tools as kt
from pykrige.ok import OrdinaryKriging

#this is Iggys job mostly

#want to define 5 classes: Nearest neighour, bilinear, IDW, unversal krgigging, and Barnes

class NearestNeighbour():
    #ds = the dataset that were using
    #gr = new grid resolution, tuple of a lat & lon
    #nds = new interpolated dataset
    def __init__(self,ds,gr):
        self.ds = ds
        if isinstance(self.ds, pd.DataFrame):
            self.ds = self.ds.set_index(['lat','lon']).to_xarray()
        self.gr = gr
        try:
            self.lats = gr[0]
            self.lons = gr[1]
        except IndexError:
            text = 'wrong grid resolution input, please input a tuple with lat & lon'
            return print(text)

    def Interpolate(self):
        
        try:  
            nds = self.ds.sel(lat=self.lats,lon=self.lons,method='nearest')
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
        if isinstance(self.ds, pd.DataFrame):
            self.ds = self.ds.set_index(['lat','lon']).to_xarray()
        try:
            self.lats = gr[0]
            self.lons = gr[1]
        except IndexError:
            text = 'wrong grid resolution input, please input a tuple with lat & lon'
            return print(text)
        
    def Interpolate(self):
        try:
            nds = self.ds.interp(lat=self.lats,lon=self.lons)
            return nds
        except TypeError:
            text = 'wrong dataset input, please input a pd.DataFrame or xr.DataArray'
            return print(text)

#IDW:
#   need: data, new grid resolution, power parameter (has default), nearest neighbour vs. full sample (defaultss to nn)
class idw():
    #ds = the dataset that were using
    #gr = new grid resolution, tuple of a lat & lon
    #nds = new interpolated dataset
    def __init__(self,ds,gr,power=1):
        self.ds = ds
        self.power = power
        if isinstance(self.ds, xr.Dataset):
            self.ds = self.ds.to_dataframe().reset_index()
        self.ds = self.ds.set_axis(['lat','lon','data'],axis=1)

        self.lat = self.ds['lat']
        self.lon = self.ds['lat']
        self.data = self.ds['data']

        if self.lat.size < self.lon.size:
            self.lat.size = np.linspace(self.lat[0],self.lat[-1],num=self.lon.size)
        if self.lon.size < self.lat.size:
            self.lon.size = np.linspace(self.lat[0],self.lat[-1],num=self.lat.size)

        try:
            self.lats = gr[0]
            self.lons = gr[1]
        except IndexError:
            text = 'wrong grid resolution input, please input a tuple with lat & lon'
            return print(text)
        
        self.lats, self.lons = np.meshgrid(self.lats, self.lons)

        # colapse grid into 1D
        self.lats, self.lons = self.lats.flatten(), self.lons.flatten()
        
    def distance_matrix(self):
        """ Make a distance matrix between pairwise observations.
        Note: from <http://stackoverflow.com/questions/1871536> 
        """
        
        obs = np.vstack((self.lat, self.lon)).T
        interp = np.vstack((self.lats, self.lons)).T

        d0 = np.subtract.outer(obs[:,0], interp[:,0])
        d1 = np.subtract.outer(obs[:,1], interp[:,1])
    
        # calculate hypotenuse
        return np.hypot(d0, d1) 
       
    def Interpolate(self):
        try:
            """ Simple inverse distance weighted (IDW) interpolation 
            Weights are proportional to the inverse of the distance, so as the distance
            increases, the weights decrease rapidly.
            The rate at which the weights decrease is dependent on the value of power.
            As power increases, the weights for distant points decrease rapidly.
            """
            
            dist = self.distance_matrix(self.lat,self.lon, self.lats,self.lons)

            # In IDW, weights are 1 / distance
            weights = 1.0/(dist+1e-12)**self.power

            # Make weights sum to one
            weights /= weights.sum(axis=0)

            # Multiply the weights for each interpolated point by all observed Z-values
            return np.dot(weights.T, self.data)
        except TypeError:
            text = 'wrong dataset input, please input a pd.DataFrame or xr.DataArray'
            return print(text)

#krigging:
#   need: data, new grid resolution, semivariogram
class krigging():
    #ds = the dataset that were using
    #gr = new grid resolution, tuple of a lat & lon
    #nds = new interpolated dataset
    def __init__(self,ds,gr):
        self.ds = ds
        if isinstance(self.ds, xr.Dataset):
            self.ds = self.ds.to_dataframe().reset_index()
        self.ds = self.ds.set_axis(['lat','lon','data'],axis=1)

        self.lat = self.ds['lat']
        self.lon = self.ds['lat']
        if self.lat.size < self.lon.size:
            self.lat.size = np.linspace(self.lat[0],self.lat[-1],num=self.lon.size)
        if self.lon.size < self.lat.size:
            self.lon.size = np.linspace(self.lat[0],self.lat[-1],num=self.lat.size)

        try:
            self.lats = gr[0]
            self.lons = gr[1]
        except IndexError:
            text = 'wrong grid resolution input, please input a tuple with lat & lon'
            return print(text)
        
    def Interpolate(self):
        try:
            OK = OrdinaryKriging(
            self.lat,
            self.lon,
            self.ds['data'])
            nds,sm = OK.execute("grid", self.lats, self.lons)
            return nds
        except TypeError:
            text = 'wrong dataset input, please input a pd.DataFrame or xr.DataArray'
            return print(text)

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

    ds_fine_xr = xr.Dataset(
        {'t2m': (['lat', 'lon'], T, {'units': 'K'})},
        coords={'lat': lats_fine, 'lon': lons_fine}
    )
    ds_fine_pd = pd.DataFrame(data={"lat":LAT.flatten(),"lon":LON.flatten(),'temp':T.flatten()})

    #check if xr & pd give same result for nn
    ds_nn_xr = NearestNeighbour(ds_fine_xr, new_grid).Interpolate()
    ds_nn_pd = NearestNeighbour(ds_fine_pd, new_grid).Interpolate()
    # print(ds_nn_pd)
    # print(ds_nn_xr)
    if ds_nn_pd['temp'] == ds_nn_xr:
        print('nn gives same result for xr and pd')
    else:
        print(ds_nn_pd)
        print(ds_nn_xr)
        print('nn does not give same result for xr and pd')

    # #check if xr & pd give same result for bl
    ds_bl_xr = Bilinear(ds_fine_xr, new_grid).Interpolate()
    ds_bl_pd = Bilinear(ds_fine_pd, new_grid).Interpolate()
    if ds_bl_pd['temp'] == ds_bl_xr:
        print('bl gives same result for xr and pd')
    else:
        print('bl does not give same result for xr and pd')

    ds_idw_xr = idw(ds_fine_xr, new_grid).Interpolate()
    ds_idw_pd = idw(ds_fine_pd, new_grid).Interpolate()
    if (ds_idw_pd == ds_idw_xr):
        print('idw gives same result for xr and pd')
    else:
        print('idw does not give same result for xr and pd')

    ds_kr_xr = krigging(ds_fine_xr, new_grid).Interpolate()
    ds_kr_pd = krigging(ds_fine_pd, new_grid).Interpolate()
    if (ds_kr_pd == ds_kr_xr).all():
        print('kr gives same result for xr and pd')
    else:
        print('kr does not give same result for xr and pd')
