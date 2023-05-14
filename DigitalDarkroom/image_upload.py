# To do
# -----------------
# improve function choose file type -> see comments
# Include error handling, try-except
# Make user interaction more friendly

"""
Module to upload images from a local folder into DigitalDarkroom.

Classes
-------
Event
    The event of a set of images.
    
Functions
---------
upload_images
    Function to upload images in DigitalDarkroom.

create_event
    Function to create an Event folder in DigitalDarkroom.
    
single_file
    Function to select a single image only to upload.
    
choose_file_type
    Function to select a multiple images to upload using file extensions.
"""

import os
import shutil
import glob
import config
import numpy as np
import pandas as pd
from extract_metadata import extract_metadata_upload

class Event():
    """ The Event class that corresponds to a set of images.
    
    Attributes:
    -----------
    name
        Name of the event.
    description 
        The description of the event.
    path
        The file path to the event in DigitalDarkroom.
    
    """

    def __init__(self, name = "", description = ""):
        self.name = name
        self.description = description
        if self.name != "":
            self.path = os.path.join(config.images_path, self.name)
        else:
            self.path = None
        print("Your event has been created!\n")


def create_event():
    """ Creates an Event instance for the images that are uploaded.
    """

    # Ask user for information about event to create
    event_name = input("What is the name of the event?\n").strip()
    print()
    event_description = input("Provide a short description of the event: "
                              "(Press enter to skip the description)\n").strip()
    print()

    # Create event folder in DigitalDarkroom
    try:
        event_path = os.path.join(config.images_path, event_name)
        if not os.path.exists(event_path):
            os.makedirs(event_path)
        else:
            print("Sorry, the event already exists...")
            
    except Exception:
        print("Error! You must enter a valid name to create the event folder...")
        raise SystemExit

    return Event(name = event_name, description = event_description)

def single_file(source, dest):
    """ Copies a single image to Digital Darkroom.
    """
    filename = input("Enter the filename of the image you would like to upload: (Q/Quit)\n")
    print()

    if filename.lower() in ['q', "quit"]:
        print("You decided to stop the image upload.")
        raise SystemExit
        
    path_to_file = os.path.join(source, filename)

    # Check if results are files
    if os.path.isfile(path_to_file):
        shutil.copy(path_to_file, dest)
        print("Image has been copied!\n")
    else:
        print("Sorry, the image could not be found... Upload aborted.")
        raise SystemExit

def choose_file_type(source, dest):
    """ Copies an entire list of images based on the image extension to Digital Darkroom.
    """
    options = ["all", "png", "jpg", "jpeg", "cr2", "nef", "tif", "bmp", "other"]
    index_list = [str(i) for i in range(1, len(options) + 1)]
    extensions_display = "\n".join([f'{index+1}) {item}' for index, item in enumerate(options)])
    
    # Display possible extensions to the user
    answer = False
    while (answer not in options) and (answer not in index_list):
        print(extensions_display)
        answer = input("What files would you like to upload? "
                       "Pick an option by entering the number "
                       "or typing the file extension: (Q/Quit)\n").lower()
        print()

        if answer in ['q', "quit"]:
            raise SystemExit
        elif answer in ["all", "1"]:
            file_extension = '*.*'
        elif answer == 'other' or answer == str(len(options)):
            user_input = input("Enter the extension of the images you would like to add: ")
            print()
            file_extension = '*.' + user_input
        elif answer.isdigit():
            ending = options[int(answer)-1]
            file_extension = '*.' + ending
        else:
            file_extension = '*.' + answer

    # copy whole tree (with subdirs), glob.glob("path/to/dir/*.*") to get list of all filenames
    for full_file_name in glob.glob(os.path.join(source, file_extension)):
        file_name = os.path.basename(full_file_name)
        
        # Copy only files from given directory
        if os.path.isfile(full_file_name): 
            extract_metadata_upload(full_file_name, dest, file_name)
    
    print("Images have been copied!\n")

def upload_images():
    """ Uploads images from specified folder by the user in Digital Darkroom.
    """

    # Ask for path to folder from which images will be uploaded
    upload_from = input("Where are the images you want to upload?\n"
                        "Please enter the full path from your home directory:"
                        " (Example: Documents/Images/MyPhotos)\n")
    print()
    upload_from = os.path.join(os.environ["HOME_PATH"], upload_from)

    # Quit function if path cannot be found
    if not os.path.exists(upload_from):
        print("Sorry, the provided path could not be found... Upload aborted.")
        raise SystemExit

    # Ask the user if an event is to be created
    answer = False
    while not answer:
        event_creation = input("Do you want to create an event for your images"
                               " or add them to an existing event?"
                               " (C/Create or A/Add or N/No or Q/Quit) :\n").lower()
        print()
        
        if event_creation in ["c", "create"]:
            event = create_event()
            upload_to = event.path
            answer = True
            
        elif event_creation in ["a", "add"]:
            
            # Display list of available events
            list_event = np.unique(config.DB["Event"].dropna())
            for event_name in list_event:
                print(event_name)
            event = input("To which event from the given list would you like to add images:\n")
            print()
            
            upload_to = os.path.join(config.images_path, event)
            answer = True
            
            # Check that the event exists in Images
            if not os.path.exists(upload_to):
                print("Sorry, the event was not found... \n")
                answer = False
                
        elif event_creation in ["n", "no"]:
            upload_to = config.images_path
            answer = True
            
        elif event_creation in ["q", "quit"]:
            raise SystemExit
            
        else:
            print("Error! Please enter one of the valid options as displayed...")

    # Ask the user how to select images to upload
    answer = input("Would you like to add a single image or choose images based on file type? "
                   "Press 1 for single image or " 
                   "2 for selection based on file type: (Q/Quit)\n").lower()
    print()

    while answer not in ["1", "2", "q", "quit"]:
        answer = input("The chosen option is not available."
                       "Press 1 for single image upload or 2 for upload based on extension: "
                       "(Q/Quit)\n").lower()
        print()

    if answer in ['q', "quit"]:
        print("You decided to stop the image upload.")
        raise SystemExit
    if int(answer) == 1:
        single_file(upload_from, upload_to)
    if int(answer) == 2:
        choose_file_type(upload_from, upload_to)
