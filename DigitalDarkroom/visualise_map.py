""" Module to visualise picture locations on a world map.
"""
import os
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import config
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
    
    # Launch diaporama of these images
    implay.display_diaporama(images)

# Initialise figure
figure, axis = plt.subplots()

# Plot the world map
world_map = gpd.read_file('worldmap.shp')
world_map.plot(ax = axis) 

# Create geopandas dataframe
#locations = gpd.GeoSeries([Point(image_DB.loc[image, "Latitude"], image_DB.loc[image, "Longitude"]) for image in image_DB.index])  # have to create a GeoSeries whereas it's already created when calling for geodata... Should we create a geopandas df for image_DB?

# Plot image locations
locations = config.DB["Event"]                      # just to test, normally it's the locations in image_DB.pkl
geodata_locations = gpd.tools.geocode(locations)    # just to test, normally it's the locations in image_DB.pkl

geodata_locations.plot(ax = axis, color = "red", picker = True)
plt.connect(s = "pick_event", func = select_images)
plt.show()