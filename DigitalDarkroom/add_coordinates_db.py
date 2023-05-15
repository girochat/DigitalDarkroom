"""
First draft:
Add coordinates to all images from an event or to a single image
Testing plotly to plot location where picture was taken on map
Some simple functions for plotting -> testing out options


Open Questions:
When should the user be asked if coordinates should be added? 
Make function more flexible to allow user input of multiple images?
How should the plots be generated? Plotly?
How can the maps be centered?
"""


import os
import config
from datetime import date
from geopy.geocoders import Nominatim
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px


# Define functions
def get_coords(location_name):
    """Function to get coordinates of a location 
    input: name of a country, city, village or an address
    output: coordinates and location name given by user, tuple
    """
    try:
        geolocator = Nominatim(user_agent="DigitalDarkroom")
        location = geolocator.geocode(location_name)
        #print(location.address)
        loc = (location.latitude, location.longitude, location_name)
        return loc
    except:
        print("Something went wrong")


def location_event_db(event_name, location_name):
    """Function to add or change coordinates for all pictures from the same event
    input: 
        event_name:     event for which coordinates will be added or changed
        location_name:  Location for which coordinates will be looked up and added to database
    output:
        image_db:       updated database
    """
    coords = get_coords(location_name)
    image_db.loc[image_db.Event ==event_name, ["Latitude", "Longitude", "Location"]] = coords  #location for event
    #image_db.to_pickle(os.path.join(os.environ["PROGRAM_PATH"], "image_DB.pkl"))  #update database
    return image_db


# Q: should user be able to add a list of images?
def location_image_db(image_name, location_name): 
    """Function to add or change coordinates for all pictures from the same event
    input: 
        image_name:     image for which coordinates will be added or changed
        location_name:  Location for which coordinates will be looked up and added to database
    output:
        image_db:       updated database
    """
    coords = get_coords(location_name)
    image_db.loc[image_name, ["Latitude", "Longitude", "Location"]] = coords # location for image
    #image_db.to_pickle(os.path.join(os.environ["PROGRAM_PATH"], "image_DB.pkl"))  #update database
    return image_db



# Not sure yet how to handle the user input and when to ask if coordinates should be added
def user_interaction_geo_event(event_name):
    """Function to get ask user if coordinates should be added and to gather the location name
    """
    answer = input("Would you like to add a location to or change the coodinates of the pictures from this event? Y or N ")
    if answer.lower() in ["yes", "y"]:
        location_name = input("Write the name of the location that should be added - "
                              "A country, city, village or address will do\n")
        return location_event_db(event_name, location_name)
    else:
        print("That is ok too.")


# Question: should user be able to select multiple images? 
def user_interaction_geo_image(image_name):
    """Function to get ask user if coordinates should be added and to gather the location name
    """
    answer = input("Would you like to add or change the coodinates of the picture? Y or N ")
    if answer.lower() in ["yes", "y"]:
        location_name = input("Enter the name of the location where the picture was taken- "
                              "A country, city, village or address will do\n")
        return location_image_db(image_name, location_name)
    else:
        print("That is ok too.")


# ---------------------------------------------------------------------
# some additional functions that could potentially be used
def plot_images_per_event(event_name):
    """Histogram: number of pictures per event
    """
    plt.hist(image_db.loc[image_db.Event==event_name].Event)
    plt.show()

def get_time_passed(image_name):
    """Function to get the time since the image was taken
    """
    today = np.datetime64(date.today())
    time_passed = today - image_db.loc[image_name].Date
    return time_passed

def plot_images_per_date():
    """Very basic time series plot
    """
    pictures_per_date = image_db.Date.value_counts()
    pictures_per_date.plot(kind = 'bar') # plot series
    plt.show()
        



if __name__ == "__main__":
    # only for testing purposes -> still needs to be linked to database

    os.environ["PROGRAM_PATH"] = os.getcwd() # for local use only
    image_db = pd.read_pickle(os.path.join(os.environ["PROGRAM_PATH"],"image_DB.pkl"))
    print(image_db)


    
    """

    df = pd.DataFrame(columns = ["Latitude", "Longitude", "Location"]) # will be added directly to database -> change this in extract_metadata
    image_db = pd.concat([image_db, df]) # not necessary once database has been updated
    print(image_db)

    image_db.to_pickle(os.path.join(os.environ["PROGRAM_PATH"], "image_DB.pkl"))


    # run functions as test
    image_db = user_interaction_geo_event("Japan") # set location of all pictures in event folder Japan -> ask user for input
    print(image_db)
    image_db = user_interaction_geo_image("DSCN3552.jpg") # change location for one image
    

    # first draft - plotting on map with plotly
    # problems: if Japan is entered as a location, all the names on the map will be in Japanese
    fig = px.scatter_mapbox(image_db,
                        lat=image_db.Latitude,
                        lon=image_db.Longitude,
                        hover_name="Location",
                        center = {"lat":image_db.Latitude[0], "lon": image_db.Longitude[0]}) # need to have a look at correct centering of the plot 
    fig.update_layout(mapbox_style="open-street-map") 
    fig.show()


    """