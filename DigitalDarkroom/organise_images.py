"""
First draft:
Extract metadata for images
Change information fo an image or event: name or location -> add option to change the description
Delete events or images (not tested correctly yet, but should delete images and events from database as well as from the DD folder)
"""

# import modules
import os
import shutil
import config
from datetime import datetime
from geopy.geocoders import Nominatim
import pandas as pd
import numpy as np
from PIL import (Image, UnidentifiedImageError)

#######################################################################
#Extract metadata
#######################################################################
def date_taken(path_to_event_folder):
    """ Get the date when the picture was taken from the exif data
    """
    return Image.open(path_to_event_folder).getexif()[306]

def get_date_from_string(date_str):
    """ Convert string output from exif to date
    """
    date = date_str.split(" ")[0]
    date = np.array(date.replace(':', '-'), dtype = np.datetime64)
    return date

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


def extract_metadata_upload(full_file_name, dest, filename, add_geo = False, single = False, coords = None):
    """ Extract metadata when images are uploaded and include it into the database image_DB
    """
    try:
        img = Image.open(full_file_name)
        exifdata = img.getexif()
        if exifdata is None or 306 not in exifdata.keys():
            date_time = pd.NaT
            date = pd.NaT
        else:
            date_time = exifdata[306]
            date = get_date_from_string(date_time)
        event = os.path.basename(os.path.normpath(dest))
        megapixels = img.size[0]*img.size[1]/1000000 # Megapixels
        nr_channels = len(Image.Image.getbands(img)) # Number of channels
        timestamp = os.path.getctime(full_file_name) # Timestamp
        creation = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        new_row = {'Filename':filename,
                   'Event':event,
                   'Format':img.format,
                   'Width':img.size[0],
                   'Height':img.size[1],
                   'Megapixels':megapixels,
                   'Channels':nr_channels,
                   'Mode':img.mode,
                   'Timestamp': timestamp,
                   'Creation':creation,
                   'Date_Time':date_time,
                   'Date': date}
        config.DB.loc[filename] = pd.Series(new_row)
        if add_geo:
            if single:
                print(f'Image name: {filename}')
                new_location = input("Enter the location name you want to add to this image: ")
                coords = get_coords(new_location)
                config.DB.loc[filename, ["Latitude", "Longitude", "Location"]] = coords
            if coords:
                config.DB.loc[filename, ["Latitude", "Longitude", "Location"]] = coords
        config.DB.to_pickle(os.path.join(os.environ["PROGRAM_PATH"], "image_DB.pkl")) 
        shutil.copy(full_file_name, dest)
    except UnidentifiedImageError:
        print("Not an image")


###############################################
#### Change information from events or images
###############################################

def location_event_db(event_name, location_name):
    """Function to add or change coordinates for all pictures from the same event
    input: 
        event_name:     event for which coordinates will be added or changed
        location_name:  Location for which coordinates will be looked up and added to database
    output:
        image_db:       updated database
    """
    coords = get_coords(location_name)
    config.DB.loc[config.DB.Event ==event_name, ["Latitude", "Longitude", "Location"]] = coords  #location for event
    config.DB.to_pickle(os.path.join(os.environ["PROGRAM_PATH"], "image_DB.pkl"))
    return config.DB


def location_image_db(image_name, location_name): 
    """Function to change coordinates for all pictures from the same event
    input: 
        image_name:     image for which coordinates will be added or changed
        location_name:  Location for which coordinates will be looked up and added to database
    output:
        image_db:       updated database
    """
    coords = get_coords(location_name)
    config.DB.loc[image_name, ["Latitude", "Longitude", "Location"]] = coords # location for image
    config.DB.to_pickle(os.path.join(os.environ["PROGRAM_PATH"], "image_DB.pkl"))
    return config.DB

def change_info_event():
    """Function to get ask user if coordinates should be added and to gather the location name
    """
    list_event = np.unique(config.DB["Event"].dropna())
    for event_name in list_event:
        print(event_name)
    event = input("For which event would you like to change the information?\n").strip()
    while event not in list_event:
        print("Sorry, the event was not found. Try again or type q to quit.")
        event = input("For which event would you like to change the information?\n").strip().lower()
        if event in ["q", "quit"]:
            print("You decided not to change the event information.")
            raise SystemExit

    change = input("What would you like to change?\n"
                   "- Name => type 'N' or name\n"
                   "- Location => type 'L' or location \n"
                   "- Quit => type 'Q' or quit \n")

    if change.lower() in ["n", "name"]:
        new_name = input("What should the new name for the event be\n")
        try:
            config.DB.loc[config.DB.Event ==event, ["Event"]] = new_name  #location for event
            config.DB.to_pickle(os.path.join(os.environ["PROGRAM_PATH"], "image_DB.pkl"))
            os.rename(os.path.join(config.images_path, event), os.path.join(config.images_path, new_name))
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))

    if change.lower() in ["l", "location"]:
        location_name = input("To which country, city, village or address should the location be changed?\n")
        location_event_db(event, location_name)

    if change.lower() in ["q", "quit"]:
        print("You decided not to change the event information.")
        raise SystemExit


def change_info_image():
    """Function to get ask user if coordinates should be added and to gather the location name
    """
    list_event = np.unique(config.DB["Event"].dropna())
    for event_name in list_event:
        print(event_name)
    event = input("In which event is the file located?\n")
    while event not in list_event:
        print("Sorry, the event was not found. Try again or type q to quit.")
        event = input("In which event is the file located?\n").strip().lower()
        if event in ["q", "quit"]:
            print("You decided not to change the event information.")
            raise SystemExit
    event_path = os.path.join(config.images_path, event)
    print("The following images are in the event:")
    for file in os.listdir(event_path):
        print(file)

    image_name = input("For which image would you like to change the information?") # needs to be changed -> selection available?
    file_path = os.path.join(event_path, image_name)
    if not os.path.isfile(file_path):
        print("Sorry, the image was not found... \n")
        raise SystemExit

    change = input("What would you like to change?\n"
                   "- Name => type 'N' or name\n"
                   "- Location => type 'L' or location \n"
                   "- Quit => type 'Q' or quit \n")

    if change.lower() in ["n", "name"]:
        new_name = input("What should the new name for the image be\n")
        try:
            config.DB.rename(index={image_name:new_name}, inplace=True)
            config.DB.to_pickle(os.path.join(os.environ["PROGRAM_PATH"], "image_DB.pkl"))
            os.rename(file_path, os.path.join(event_path, new_name))
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))

    if change.lower() in ["l", "location"]:
        location_name = input("Write the name of the location that should be added - "
                              "A country, city, village or address will do\n")
        location_image_db(image_name, location_name)
    
    if change.lower() in ["q", "quit"]:
        print("You decided not to change the image information.")
        raise SystemExit

def change_info():
    answer = input("For what would you like to change the information\n"
                   "- Event => type 'E' or 'event'\n"
                   "- Image => type 'I' or 'image'\n"
                    "- Quit => type 'Q' or quit \n").lower()
    if answer in ["e", "event"]:
        change_info_event()
        print(config.DB)

    if answer in ["i", "image"]:
        change_info_image()
        print(config.DB)

    if answer.lower() in ["q", "quit"]:
        print("You decided not to change the event information.")
        raise SystemExit
    else:
        print("No possible option chosen")

#########################################################
# Delete event or file
#########################################################
def del_event():
    list_event = np.unique(config.DB["Event"].dropna())
    for event_name in list_event:
        print(event_name)
    event = input("Which event would you like to delete?\n")
    print()
    event_path = os.path.join(config.images_path, event)
    config.DB = config.DB.drop(config.DB[config.DB.Event == event].index)
    print("Event deleted from database")
    config.DB.to_pickle(os.path.join(os.environ["PROGRAM_PATH"], "image_DB.pkl"))
    try:
        shutil.rmtree(event_path)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))

def del_file():
    list_event = np.unique(config.DB["Event"].dropna())
    for event_name in list_event:
        print(event_name)
    event = input("In which event is the file located?\n")
    file = input("Which file would you like to delete?\n")
    print()
    event_path = os.path.join(config.images_path, event)
    if not os.path.exists(event_path):
        print("Sorry, the event was not found... \n")
        raise SystemExit

    file_path = os.path.join(event_path, file)
    if not os.path.isfile(file_path):
        print("Sorry, the image was not found... \n")
        raise SystemExit
    # Try to delete the file.
    try:
        os.remove(file_path)
        config.DB = config.DB.drop(index = file)
    except OSError as e:
    # If it fails, inform the user.
        print("Error: %s - %s." % (e.filename, e.strerror))

       
def delete():
    answer = input("What would you like to delete?\n"
                   "- Event => type 'E' or 'event\n"
                   "- File => type 'F' or 'file'\n"
                   "- Quit => type 'Q' or 'quit'\n").lower()
    if answer in ["e", "event"]:
        del_event()
        print(config.DB)
    if answer in ["f", "file"]:
        del_file()
        print(config.DB)
    if answer in ['q', "quit"]:
        print("You decided not to delete anything.")
        raise SystemExit

