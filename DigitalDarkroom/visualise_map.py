""" Module to visualise picture locations on a world map.

Functions
---------
select_images
    Function to select images from their locations on the worldmap. Called by a pick event on the figure.
    
plot_locations
    Function to plot the image locations on the worldmap.
    
plot_geo_heatmap
    Function to plot the density of the image locations on the worldmap.
"""
import os
import config
import numpy as np
import pandas as pd
import geopandas as gpd
import geoplot as gplt
import matplotlib.pyplot as plt
import display_images as implay

def select_images(pick_event):
    """ Launches display of images that correspond to map location picked by user.
    
    Parameters
    ----------
    pick_event : matplotlib.backend_bases.PickEvent
        the event that was picked on the map.
    """
    # Get list of images that correspond to locations
    plt.close()
    images = list(config.DB.iloc[pick_event.ind, :].index)

    # Launch image diaporama if right click 
    if pick_event.mouseevent.button == 1:
        implay.display_diaporama(images, picker = False)

    # Launch image panorama if left click
    elif pick_event.mouseevent.button == 3:
        implay.display_panorama(images, picker = False)

    
    
def plot_locations():
    """ Plots image locations on world map.
    """
    # Initialise figure
    figure, axis = plt.subplots()

    # Plot the world map
    world_map = gpd.read_file('worldmap.shp')
    world_map.plot(ax = axis, column = 'LABEL_Y', cmap = "viridis")
    axis.set_axis_off()

    # Create geopandas dataframe with the image locations
    geodata_locations = gpd.GeoDataFrame(config.DB[["Latitude", "Longitude", "Location"]], 
                                         geometry = gpd.points_from_xy(config.DB["Longitude"], 
                                                                       config.DB["Latitude"]))


    # Plot image locations
    geodata_locations.plot(ax = axis, color = "red", picker = True)
    plt.connect(s = "pick_event", func = select_images)
    plt.show()
    
def plot_geo_heatmap():
    """ Plots density of image locations on worldmap.
    """
    # Load the world map and the image locations
    world_map = gpd.read_file('worldmap.shp')
    images = gpd.GeoDataFrame(config.DB[["Latitude", "Longitude", "Location"]], 
                              geometry = gpd.points_from_xy(config.DB["Longitude"],
                                                            config.DB["Latitude"],
                                                            crs = world_map.crs))
    # Set the projection
    proj = gplt.crs.PlateCarree()

    # Plot geo heatmap of the image locations
    ax1 = gplt.kdeplot(images,
                cmap = 'Blues',
                projection=proj,
                fill = True,
                levels = 1,
                thresh = 0.05,
                extent = (-180, -90, 180, 90))
    
    # Plot the worldmap in the background
    gplt.polyplot(world_map, zorder=1, ax=ax1)
    ax1.set_axis_off()
    plt.show()
