## --- Imports ---
from satpy import Scene, find_files_and_readers, MultiScene
from pyresample import create_area_def
from satpy.writers import get_enhanced_image
from satpy.multiscene import timeseries
from glob import glob
from datetime import datetime
from copy import deepcopy
import matplotlib.pyplot as plt
import numpy as np
import math
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib_scalebar.scalebar import ScaleBar
import cmocean
import pandas as pd
import xarray as xr
import netCDF4
import os

## --- Configuration ---
# Paths
INPUT_DIR_MODIS = "/mnt/beegfs/groups/ouri_project/satdata/modis/"
INPUT_DIR_SST = "/mnt/beegfs/groups/ouri_project/satdata/sst/"
OUTPUT_DIR = "/mnt/beegfs/home/jpindell2022/projects/nasa-murep/nasa-murep-hpc/cdom/figures"

# File patterns
MODIS_FILE_PATTERN = "*.hdf"
SST_FILE_PATTERN = "*.TIFF"

# Date range for processing (used in titles and filenames)
DATE_RANGE = "Jun 01-Jun 30"

# Area definition parameters
AREA_EXTENT = [-94, 27.5, -88, 30.5]
PROJECTION_PARAMS = {
    'proj': 'lcc', 
    'lon_0': -91., 
    'lat_0': 29.5, 
    'lat_1': 29.5, 
    'lat_2': 29.5
}
AREA_WIDTH = 1500
AREA_HEIGHT = 750

# CDOM calculation coefficients
B0 = 0.2487
B1 = 14.028
B2 = 4.085

# Plot settings
DPI = 4000
COASTLINE_RESOLUTION = "10m"
LAND_COLOR = "gray"
COLORMAP = "inferno"
COLORBAR_LABEL = "Sed. CDOM Index"
MANUAL_COLOR_SCALE = True
COLOR_SCALES = {
    'full_range': {
        'cmin': 0, 
        'cmax': 0.24, 
        'title': f'{DATE_RANGE} - Sed. CDOM (Full Range)', 
        'filename': f'{DATE_RANGE} SST & CDOM (Full Range).png'
    },
    'high_min': {
        'cmin': 0.08, 
        'cmax': 0.24, 
        'title': f'{DATE_RANGE} - Sed. CDOM (High Min)', 
        'filename': f'{DATE_RANGE} SST & CDOM (High Min).png'
    }
}

## --- Utility Functions ---
def fahrenheit(x): return (x * 9 / 5) + 32
def celcius(x): return (x - 32) * 5 / 9

def sstinvert(x, mode='num'):
    """Invert SST for emphasis on lower values"""
    return -1 * (x / 255) + 1 if mode == 'num' else NotImplementedError("Only 'num' mode supported.")

def create_area():
    """Define projection and area extent"""
    return create_area_def(
        'my_area',
        PROJECTION_PARAMS,
        width=AREA_WIDTH, 
        height=AREA_HEIGHT,
        area_extent=AREA_EXTENT, 
        units='degrees'
    )

def create_cdom_plot(data, lons, lats, cmin, cmax, title, output_path, projection, res=COASTLINE_RESOLUTION):
    """Plot and save Sediment CDOM index data"""
    fig = plt.figure(dpi=DPI)
    ax = plt.axes(projection=projection)
    ax.coastlines(res)
    ax.add_feature(cfeature.NaturalEarthFeature('physical', 'land', res, facecolor=LAND_COLOR))
    mesh = ax.pcolormesh(lons, lats, data, transform=ccrs.PlateCarree(), cmap=COLORMAP, vmin=cmin, vmax=cmax)
    plt.colorbar(mesh, shrink=0.6, label=COLORBAR_LABEL)
    plt.title(title)
    fig.savefig(output_path)
    plt.close(fig)


## --- Main Processing ---
def main():
    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Set up area definition
    area = create_area()
    
    # Load and process MODIS data
    modis_files = glob(f"{INPUT_DIR_MODIS}/{MODIS_FILE_PATTERN}")
    modis = Scene(modis_files, reader='modis_l1b')
    modis.load(['8', '4', '13lo', 'true_color'])
    modis = modis.resample(area)
    
    Rss412, Rss555, Rss667 = modis['8'], modis['4'], modis['13lo']
    
    aCDOM412 = np.log((Rss412 / Rss555 - B0) / B2) / (-B1)
    aCDOM412 = aCDOM412.compute()
    
    # Load and process SST data
    sst_files = glob(f'{INPUT_DIR_SST}/{SST_FILE_PATTERN}')
    sst = Scene(sst_files, reader='generic_image')
    sst.load(['image'])
    sst = sst.resample(area)
    sst_data = sst['image'][0].values
    
    # Combine SST and CDOM into Sediment CDOM Index
    combo = deepcopy(modis['8'].drop_attrs())
    combo_data = np.zeros_like(sst_data)
    
    valid_mask = ~np.isnan(aCDOM412)
    sst_inverted = sstinvert(sst_data)
    
    combo_data[valid_mask] = aCDOM412[valid_mask] * sst_inverted[valid_mask]
    combo.values = combo_data
    
    # Generate plots
    lons, lats = np.meshgrid(combo.x.values, combo.y.values)
    projection = ccrs.PlateCarree()
    
    if not MANUAL_COLOR_SCALE:
        data_min, data_max = float(combo.min()), float(combo.max())
        COLOR_SCALES['full_range']['cmin'] = data_min
        COLOR_SCALES['full_range']['cmax'] = data_max
        COLOR_SCALES['high_min']['cmax'] = data_max
    
    for scale_name, config in COLOR_SCALES.items():
        create_cdom_plot(
            data=combo_data,
            lons=lons,
            lats=lats,
            cmin=config['cmin'],
            cmax=config['cmax'],
            title=config['title'],
            output_path=os.path.join(OUTPUT_DIR, config['filename']),
            projection=projection
        )

if __name__ == "__main__":
    main()
