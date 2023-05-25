"""
Extract metadata for images
Change information fo an image or event: name or location
Delete events or images 
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
from display_images import get_event

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
                   'Date': date,
                   'Edited': False}
        config.DB.loc[filename] = pd.Series(new_row)
        if add_geo:
            if single:
                print(f'Image name: {filename}')
                new_location = input("Enter the location name you want to add to this image: ")
                coords = get_coords(new_location)
                config.DB.loc[filename, ["Latitude", "Longitude", "Location"]] = coords
            if coords:
                config.DB.loc[filename, ["Latitude", "Longitude", "Location"]] = coords
        config.DB.to_pickle(os.path.join(config.program_path, "image_DB.pkl")) 
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
    config.DB.to_pickle(os.path.join(config.program_path, "image_DB.pkl"))
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
    config.DB.loc[image_name, ["Latitude", "Longitude", "Location"]] = coords 
    config.DB.to_pickle(os.path.join(config.program_path, "image_DB.pkl"))
    print("The location has been changed.")
    return config.DB

def change_info_event():
    """Function to change the information of an event (name or location)
    """
    event_path = get_event()

    if os.path.normpath(event_path) == os.path.normpath(config.images_path):
        print("You decided not to change the event info")
        raise SystemExit
    
    event = os.path.basename(event_path)

    # list options and let user choose one of them
    while True:
        change = input("What would you like to change?\n"
                "- Name => type 'N' or name\n"
                "- Location => type 'L' or location \n"
                "- Quit => type 'Q' or quit \n")
        
        if change.lower() in ["n", "name"]:
            new_name = input("What should the new name for the event be\n")
            try:
                config.DB.loc[config.DB.Event ==event, ["Event"]] = new_name  #location for event
                config.DB.to_pickle(os.path.join(config.program_path, "image_DB.pkl"))
                os.rename(os.path.join(config.images_path, event), os.path.join(config.images_path, new_name))
                break
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))

        if change.lower() in ["l", "location"]:
            location_name = input("To which country, city, village or address should the location be changed?\n")
            location_event_db(event, location_name)
            print("The event location has been changed.")
            break

        if change.lower() in ["q", "quit"]:
            print("You decided not to change the event information.")
            raise SystemExit

        else:
            print("No available option chosen. Try again or press 'q' to quit.")


def change_info_image():
    """Function to change the name or location of an image
    """
    # get the event path
    event_path = get_event()

    # list picture names and test if picture exists
    print("The following images are in the event:")
    for file in os.listdir(event_path):
        # check if current path is a file
        if os.path.isfile(os.path.join(event_path, file)):
            print(file)
    image_name = input("For which image would you like to change the information?\n"
                       "Enter the name or press 'q' to quit.\n") # select from panorama

    if image_name.lower() in ["q", "quit"]:
        print("You decided not to change the image information.\n")
        raise SystemExit
    
    file_path = os.path.join(event_path, image_name)

    while not os.path.isfile(file_path):
        print("Sorry, the image was not found... \n")
        image_name = input("Try again to enter the image name or press 'q' to quit.\n")
        if image_name.lower() in ["q", "quit"]:
            print("You decided not to change the event information.")
            raise SystemExit
        print()

    # list options for the changes
    while True:
        change = input("What would you like to change?\n"
                    "- Name => type 'N' or name\n"
                    "- Location => type 'L' or location \n"
                    "- Quit => type 'Q' or quit \n")

        if change.lower() in ["n", "name"]:
            new_name = input("What should the new name for the image be? \n")
            try:
                config.DB.rename(index={image_name:new_name}, inplace=True)
                config.DB.to_pickle(config.program_path, "image_DB.pkl")
                os.rename(file_path, os.path.join(event_path, new_name))
                print("The name has been changed.")
                break
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))

        if change.lower() in ["l", "location"]:
            location_name = input("Write the name of the location that should be added - "
                                "A country, city, village or address will do\n")
            location_image_db(image_name, location_name)

        if change.lower() in ["q", "quit"]:
            print("You decided not to change the image information.")
            raise SystemExit

        else:
            print("No available option chosen. Try again or press 'q' to quit.")


def change_info():
    """Function to change the information of an event or a file (name or location)
    """
    while True:
        answer = input("For what would you like to change the information\n"
                    "- Event => type 'E' or 'event'\n"
                    "- Image => type 'I' or 'image'\n"
                        "- Quit => type 'Q' or quit \n").lower()

        if answer in ["e", "event"]:
            change_info_event()
            break

        if answer in ["i", "image"]:
            change_info_image()
            break

        if answer in ["q", "quit"]:
            print("You decided not to change the event information.")
            raise SystemExit

        else:
            print("Invalid input. Try again.")




#########################################################
# Delete event or file
#########################################################
def del_event():
    """Function to delete an entire event
    """
    event_path = get_event()
    if os.path.normpath(event_path) == os.path.normpath(config.images_path):
        print("You decided not to delete the event")
        raise SystemExit
    
    event = os.path.basename(event_path)
    config.DB = config.DB.drop(config.DB[config.DB.Event == event].index)
    print("Event deleted from database")
    config.DB.to_pickle(config.program_path, "image_DB.pkl")
    try:
        shutil.rmtree(event_path)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))


def del_file():
    """Function to delete a file within an event 
    """
    event_path = get_event()

    # list images in event
    print("The following images are in the event:")
    # check if current path is a file
    for file in os.listdir(event_path):
    # check if current path is a file
        if os.path.isfile(os.path.join(event_path, file)):
            print(file)

    file = input("Which file would you like to delete?\n"
                 "Enter its name or press q to quit.\n")
    print()
    if file.lower() in ["q", "quit"]:
        print("You decided not to delete the image.\n")
        raise SystemExit
    while file not in os.listdir(event_path):
        print("Sorry, the file was not found. Try again or type q to quit.")
        file = input("Type the name of the file you would like to quit?\n").strip()
        if file.lower() in ["q", "quit"]:
            print("You decided not to delete the file.")
            raise SystemExit

    file_path = os.path.join(event_path, file)

    # Try to delete the file
    try:
        os.remove(file_path)
        config.DB = config.DB.drop(index = file)
        print("Image has been deleted.")
    except OSError as e:
    # If it fails, inform the user.
        print("Error: %s - %s." % (e.filename, e.strerror))
        
def delete():
    """Function to delete an event or a file from DigitalDarkroom
    """
    while True:
        answer = input("What would you like to delete?\n"
                "- Event => type 'E' or 'event\n"
                "- File => type 'F' or 'file'\n"
                "- Quit => type 'Q' or 'quit'\n").lower()

        if answer in ["e", "event"]:
            del_event()
            break

        if answer in ["f", "file"]:
            del_file()
            break

        if answer in ['q', "quit"]:
            print("You decided not to delete anything.")
            raise SystemExit

        else:
            print("The chosen option is not available. Try again or press 'q' to quit.")