# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 08:47:36 2023

@author: HP
"""

import cdsapi
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

# set up the CDS API client
c = cdsapi.Client()

# define the request parameters
request = {
    'product_type': 'reanalysis',
    'variable': ['10m_u_component_of_wind', '10m_v_component_of_wind'],
    'year': '2023',
    'month': '04',
    'day': '01',
    'time': ['00:00', '01:00', '02:00'],
    'area': [60, -80, 40, -55],
    'format': 'netcdf'
}

# submit the request and download the data
c.retrieve('reanalysis-era5-single-levels', request, 'download.nc')

# open the downloaded file with xarray
ds = xr.open_dataset('download.nc')

# extract the wind components
u = ds['u10']
v = ds['v10']

# create a plot
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
ax.coastlines()
ax.set_extent([-90, 60, 35, 80], crs=ccrs.PlateCarree())

lat = u.latitude.values
lon = u.longitude.values

u = u[0,:,:].values.reshape(81, 101)
v = v[0,:,:].values.reshape(81, 101)

u = xr.DataArray(u, coords=[lat, lon], dims=['latitude', 'longitude'])
v = xr.DataArray(v, coords=[lat, lon], dims=['latitude', 'longitude'])

# calculate the wind speed
wind_speed = (u**2 + v**2)**0.5

# create a contour plot
contour_levels = 10
contourf = ax.contourf(lon, lat, wind_speed, contour_levels, cmap='coolwarm', transform=ccrs.PlateCarree())
cbar = plt.colorbar(contourf, orientation='horizontal', shrink=0.5, pad=0.05)
cbar.set_label('Wind speed (m/s)')

plt.title('ERA5 Surface Wind\n'+ request['day'] + request['month'] + request['year'] + '\n' + 'Quebec' )
plt.show()
