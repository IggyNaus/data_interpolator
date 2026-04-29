import numpy as np
import xarray as xr
import pandas as pd

import pykrige.kriging_tools as kt
from pykrige.ok import OrdinaryKriging
from fastbarnes import interpolation


class NearestNeighbour():
    """
    Nearest-neighbor interpolation for gridded latitude/longitude data.

    This class selects the closest existing data point for each point on a
    requested output grid. It is useful as a simple baseline interpolation
    method because it does not create new values by averaging or weighting.

    Parameters
    ----------
    ds : xr.Dataset or pd.DataFrame
        Input dataset containing latitude, longitude, and data values.
        If a pandas DataFrame is provided, it should contain columns named
        ``lat`` and ``lon``.
    gr : tuple or list
        Target grid in the form ``(new_lats, new_lons)``, where each element
        is an array-like sequence of coordinates.

    Attributes
    ----------
    ds : xr.Dataset
        Dataset converted to xarray format if needed.
    lats, lons : array-like
        Target latitude and longitude coordinates.
    """

    def __init__(self, ds, gr):
        self.ds = ds
        self.gr = gr

        # Convert DataFrame input to xarray so xarray's coordinate-based
        # selection tools can be used consistently.
        if isinstance(self.ds, pd.DataFrame):
            self.ds = self.ds.set_index(['lat', 'lon']).to_xarray()

        # Extract target latitude and longitude arrays from the grid input.
        try:
            self.lats = self.gr[0]
            self.lons = self.gr[1]
        except IndexError:
            text = 'wrong grid resolution input, please input a tuple with lat & lon'
            return print(text)

    def Interpolate(self):
        """
        Interpolate the dataset to the requested grid using nearest neighbors.

        Returns
        -------
        xr.Dataset
            Dataset sampled at the nearest original latitude/longitude points.
        """
        try:
            nds = self.ds.sel(lat=self.lats, lon=self.lons, method='nearest')
            return nds
        except TypeError:
            text = 'wrong dataset input, please input a pd.DataFrame or xr.DataArray'
            return print(text)


class Bilinear():
    """
    Bilinear interpolation for gridded latitude/longitude data.

    This class uses xarray's interpolation method to estimate values at new
    latitude and longitude coordinates. Unlike nearest-neighbor interpolation,
    bilinear interpolation creates smoother values by interpolating between
    surrounding grid points.

    Parameters
    ----------
    ds : xr.Dataset or pd.DataFrame
        Input dataset containing latitude, longitude, and data values.
        If a pandas DataFrame is provided, it should contain columns named
        ``lat`` and ``lon``.
    gr : tuple or list
        Target grid in the form ``(new_lats, new_lons)``.
    """

    def __init__(self, ds, gr):
        self.ds = ds
        self.gr = gr

        # Convert DataFrame input to xarray format for coordinate interpolation.
        if isinstance(self.ds, pd.DataFrame):
            self.ds = self.ds.set_index(['lat', 'lon']).to_xarray()

        # Extract target latitude and longitude arrays from the grid input.
        try:
            self.lats = gr[0]
            self.lons = gr[1]
        except IndexError:
            text = 'wrong grid resolution input, please input a tuple with lat & lon'
            return print(text)

    def Interpolate(self):
        """
        Interpolate the dataset to the requested grid using bilinear interpolation.

        Returns
        -------
        xr.Dataset
            Interpolated dataset on the requested latitude/longitude grid.
        """
        try:
            nds = self.ds.interp(lat=self.lats, lon=self.lons)
            return nds
        except TypeError:
            text = 'wrong dataset input, please input a pd.DataFrame or xr.DataArray'
            return print(text)


class IDW():
    """
    Inverse Distance Weighting (IDW) interpolation.

    This class interpolates scattered or gridded data onto a new latitude/
    longitude grid. IDW estimates each target value as a weighted average of
    observed values, where closer observations receive larger weights.

    Parameters
    ----------
    ds : xr.Dataset or pd.DataFrame
        Input dataset containing latitude, longitude, and data values.
    gr : tuple or list
        Target grid in the form ``(new_lats, new_lons)``.
    power : float, optional
        Power parameter controlling how quickly weights decrease with distance.
        Larger values give more influence to nearby points. Default is 2.

    Notes
    -----
    IDW weights are proportional to ``1 / distance**power``. A small constant
    is added to distances during weighting to avoid division by zero when a
    target point exactly matches an observation point.
    """

    def __init__(self, ds, gr, power=2):
        self.ds = ds
        self.gr = gr
        self.power = power

        # Convert xarray input into a DataFrame so the IDW calculation can
        # operate on 1D coordinate and value arrays.
        if isinstance(self.ds, xr.Dataset):
            self.ds = self.ds.to_dataframe().reset_index()

        # Standardize the first three columns to lat/lon/data.
        self.ds = self.ds.set_axis(['lat', 'lon', 'data'], axis=1)

        self.lat = self.ds['lat']
        self.lon = self.ds['lat']
        self.data = self.ds['data']

        # Attempt to align coordinate array lengths before interpolation.
        if self.lat.size < self.lon.size:
            self.lat.size = np.linspace(self.lat[0], self.lat[-1], num=self.lon.size)
        if self.lon.size < self.lat.size:
            self.lon.size = np.linspace(self.lat[0], self.lat[-1], num=self.lat.size)

        # Extract target latitude and longitude arrays from the grid input.
        try:
            self.lats = gr[0]
            self.lons = gr[1]
        except IndexError:
            text = 'wrong grid resolution input, please input a tuple with lat & lon'
            return print(text)

        # Convert target latitude/longitude vectors into a full grid.
        self.lats, self.lons = np.meshgrid(self.lats, self.lons)

        # Collapse the target grid into 1D arrays so distances can be computed
        # between every observation and every target point.
        self.lats, self.lons = self.lats.flatten(), self.lons.flatten()

    def distance_matrix(self, x0, y0, x1, y2):
        """
        Compute pairwise Euclidean distances between observations and targets.

        Parameters
        ----------
        x0, y0 : array-like
            Coordinates of the original observation points.
        x1, y2 : array-like
            Coordinates of the target interpolation points.

        Returns
        -------
        np.ndarray
            Distance matrix where rows correspond to observation points and
            columns correspond to target points.

        Notes
        -----
        Adapted from a common pairwise-distance approach using NumPy outer
        subtraction.
        """
        obs = np.vstack((x0, y0)).T
        interp = np.vstack((x1, y2)).T

        d0 = np.subtract.outer(obs[:, 0], interp[:, 0])
        d1 = np.subtract.outer(obs[:, 1], interp[:, 1])

        # Hypotenuse gives straight-line distance between each pair of points.
        return np.hypot(d0, d1)

    def Interpolate(self):
        """
        Interpolate values onto the target grid using IDW.

        Returns
        -------
        np.ndarray
            Interpolated values at each target grid point.
        """
        try:
            # Compute distance from each observed point to each target grid point.
            dist = self.distance_matrix(self.lat, self.lon, self.lats, self.lons)

            # Convert distances to inverse-distance weights.
            # The small constant avoids division by zero at coincident points.
            weights = 1.0 / (dist + 1e-12) ** self.power

            # Normalize weights so contributions to each target point sum to one.
            weights /= weights.sum(axis=0)

            # Apply weights to observed data values to estimate target values.
            return np.dot(weights.T, self.data)
        except TypeError:
            text = 'wrong dataset input, please input a pd.DataFrame or xr.DataArray'
            return print(text)


class Krigging():
    """
    Ordinary kriging interpolation for spatial data.

    This class uses PyKrige's ``OrdinaryKriging`` implementation to interpolate
    input data onto a new grid. Kriging is a geostatistical interpolation method
    that estimates values based on spatial covariance structure.

    Parameters
    ----------
    ds : xr.Dataset or pd.DataFrame
        Input dataset containing latitude, longitude, and data values.
    gr : tuple or list
        Target grid in the form ``(new_lats, new_lons)``.

    Returns
    -------
    np.ndarray
        Interpolated values on the requested grid.
    """

    def __init__(self, ds, gr):
        self.ds = ds
        self.gr = gr

        # Convert xarray input into a DataFrame for PyKrige.
        if isinstance(self.ds, xr.Dataset):
            self.ds = self.ds.to_dataframe().reset_index()

        # Standardize column names expected by the kriging setup.
        self.ds = self.ds.set_axis(['lat', 'lon', 'data'], axis=1)

        self.lat = self.ds['lat']
        self.lon = self.ds['lat']

        # Attempt to align coordinate array lengths before interpolation.
        if self.lat.size < self.lon.size:
            self.lat.size = np.linspace(self.lat[0], self.lat[-1], num=self.lon.size)
        if self.lon.size < self.lat.size:
            self.lon.size = np.linspace(self.lat[0], self.lat[-1], num=self.lat.size)

        # Extract target latitude and longitude arrays from the grid input.
        try:
            self.lats = gr[0]
            self.lons = gr[1]
        except IndexError:
            text = 'wrong grid resolution input, please input a tuple with lat & lon'
            return print(text)

    def Interpolate(self):
        """
        Interpolate values onto the target grid using ordinary kriging.

        Returns
        -------
        np.ndarray
            Kriged values on the requested output grid.
        """
        try:
            # Build the kriging model from observed coordinates and values.
            OK = OrdinaryKriging(
                self.lat,
                self.lon,
                self.ds['data']
            )

            # Evaluate the kriging model on the requested grid.
            nds, sm = OK.execute("grid", self.lats, self.lons)
            return nds
        except TypeError:
            text = 'wrong dataset input, please input a pd.DataFrame or xr.DataArray'
            return print(text)


class Barnes():
    """
    Barnes interpolation for spatial data.

    Barnes interpolation estimates values on a grid using distance-based
    weighting and smoothing. This class uses the ``fastbarnes`` package to
    apply Barnes interpolation to latitude/longitude data.

    Parameters
    ----------
    ds : xr.Dataset or pd.DataFrame
        Input dataset containing latitude, longitude, and data values.
    gr : tuple or list
        Target grid in the form ``(new_lats, new_lons)``.
    res : float, optional
        Resolution parameter used to determine the interpolation step size.
        Default is 1.

    Returns
    -------
    np.ndarray
        Barnes-interpolated values.
    """

    def __init__(self, ds, gr, res=1):
        self.ds = ds
        self.gr = gr
        self.res = res

        # Convert xarray input into a DataFrame for the fastbarnes routine.
        if isinstance(self.ds, xr.Dataset):
            self.ds = self.ds.to_dataframe().reset_index()

        # Standardize column names expected by the interpolation setup.
        self.ds = self.ds.set_axis(['lat', 'lon', 'data'], axis=1)

        self.lat = self.ds['lat']
        self.lon = self.ds['lat']
        self.lonlat = np.column_stack([self.lat, self.lon])

        # Attempt to align coordinate array lengths before interpolation.
        if self.lat.size < self.lon.size:
            self.lat.size = np.linspace(self.lat[0], self.lat[-1], num=self.lon.size)
        if self.lon.size < self.lat.size:
            self.lon.size = np.linspace(self.lat[0], self.lat[-1], num=self.lat.size)

        # Extract target latitude and longitude arrays from the grid input.
        try:
            self.lats = gr[0]
            self.lons = gr[1]
        except IndexError:
            text = 'wrong grid resolution input, please input a tuple with lat & lon'
            return print(text)

    def Interpolate(self):
        """
        Interpolate values onto the target grid using Barnes interpolation.

        Returns
        -------
        np.ndarray
            Barnes-interpolated values with missing values removed.
        """
        try:
            # fastbarnes expects a step size and the lower-left starting point.
            step = 1.0 / self.res
            x0 = np.asarray([self.lat[0], self.lon[0]], dtype=np.float64)
            size = self.lats.size, self.lons.size
            value = self.ds['data'].to_numpy()

            # Sigma controls the smoothing scale used by Barnes interpolation.
            sigma = 1.0

            # Apply Barnes interpolation to the input coordinate/value pairs.
            nds = interpolation.barnes(self.lonlat, value, sigma, x0, step, size)

            # Remove missing values produced outside the interpolation domain.
            nds = nds[~np.isnan(nds)]
            return nds

        except TypeError:
            text = 'wrong dataset input, please input a pd.DataFrame or xr.DataArray'
            return print(text)


if __name__ == "_main_":
    # Create synthetic fine-resolution latitude and longitude arrays.
    lats_fine = np.arange(25, 50, 0.5)
    lons_fine = np.arange(-120, -70, 0.5)

    # Create a coarser target grid for interpolation.
    lats_coarse = np.arange(26, 50, 2.0)
    lons_coarse = np.arange(-119, -70, 2.0)
    new_grid = [lats_coarse, lons_coarse]

    # Generate synthetic temperature data with a latitudinal gradient,
    # longitudinal wave pattern, and small random noise.
    LON, LAT = np.meshgrid(lons_fine, lats_fine)
    T = 300 - 0.5 * (LAT - 25) + 3 * np.sin(np.radians(LON + 100))
    T += np.random.default_rng(42).normal(0, 0.5, T.shape)

    # Store the same synthetic data as both xarray and pandas objects so
    # interpolation methods can be tested on both supported input formats.
    ds_fine_xr = xr.Dataset(
        {'t2m': (['lat', 'lon'], T, {'units': 'K'})},
        coords={'lat': lats_fine, 'lon': lons_fine}
    )
    ds_fine_pd = pd.DataFrame(
        data={"lat": LAT.flatten(), "lon": LON.flatten(), 'temp': T.flatten()}
    )

    # Check whether xarray and pandas inputs give the same result for
    # nearest-neighbor interpolation.
    ds_nn_xr = NearestNeighbour(ds_fine_xr, new_grid).Interpolate()
    ds_nn_pd = NearestNeighbour(ds_fine_pd, new_grid).Interpolate()
    if ds_nn_pd['temp'] == ds_nn_xr:
        print('nn gives same result for xr and pd')
    else:
        print(ds_nn_pd)
        print(ds_nn_xr)
        print('nn does not give same result for xr and pd')

    # Check whether xarray and pandas inputs give the same result for
    # bilinear interpolation.
    ds_bl_xr = Bilinear(ds_fine_xr, new_grid).Interpolate()
    ds_bl_pd = Bilinear(ds_fine_pd, new_grid).Interpolate()
    if ds_bl_pd['temp'] == ds_bl_xr:
        print('bl gives same result for xr and pd')
    else:
        print('bl does not give same result for xr and pd')

    # Check whether xarray and pandas inputs give the same result for IDW.
    ds_idw_xr = IDW(ds_fine_xr, new_grid).Interpolate()
    ds_idw_pd = IDW(ds_fine_pd, new_grid).Interpolate()
    if (ds_idw_pd == ds_idw_xr).all():
        print('idw gives same result for xr and pd')
    else:
        print('idw does not give same result for xr and pd')

    # Check whether xarray and pandas inputs give the same result for kriging.
    ds_kr_xr = Krigging(ds_fine_xr, new_grid).Interpolate()
    ds_kr_pd = Krigging(ds_fine_pd, new_grid).Interpolate()
    if (ds_kr_pd == ds_kr_xr).all():
        print('kr gives same result for xr and pd')
    else:
        print('kr does not give same result for xr and pd')

    # Check whether xarray and pandas inputs give the same result for Barnes.
    ds_br_xr = Barnes(ds_fine_xr, new_grid, 1).Interpolate()
    ds_br_pd = Barnes(ds_fine_pd, new_grid, 1).Interpolate()
    if (ds_br_pd == ds_br_xr).all():
        print('barnes gives same result for xr and pd')
    else:
        print('barnes does not give same result for xr and pd')