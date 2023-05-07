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
from extract_metadata import extract_metadata_upload
import pandas as pd

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
            self.path = os.path.join(os.environ["IMAGES_PATH"], self.name) 
        else:
            self.path = None
        print("Your event has been created!\n")


def create_event():
    """ Creates an Event instance for the images that are uploaded.
    """
    
    # Ask user for information about event to create
    event_name = input("What is the name of the event?\n").strip()
    event_description = input("Provide a short description of the event: (Press enter to skip the description)\n").strip()
    
    # Create event folder in DigitalDarkroom
    try:
        event_path = os.path.join(os.environ["IMAGES_PATH"], event_name) 
        if not os.path.exists(event_path):
            os.makedirs(event_path)
    except Exception:
        print("Error! You must enter a valid name to create the event foler...") 
    
    return Event(name = event_name, description = event_description)

def single_file(source, dest):
    """ Copies a single image to Digital Darkroom.
    """
    filename = input("Enter the filename of the image you would like to upload: (Q for Quit)\n")
    
    if filename.lower() in ['q', "quit"]:
        print("You decided to stop the image upload.")
        return
    path_to_file = os.path.join(source, filename)
    
    # Check if results are files
    if os.path.isfile(path_to_file): 
        shutil.copy(path_to_file, dest)
        print("Image has been copied!\n")
    else:
        print("Sorry, the image could not be found... Upload aborted.")
        return

    
# if user is in folder with his images, ask the user for file extension
# copy all images in folder with specific file ending -> which file endings should be available? 
# Issue: Select all extensions will also import text files (needs to be changed) -> Done
# Question: use select or switch instead? Or let user just enter one or several extensions?
# Add option to add a list of images?
def choose_file_type(source, dest):
    """ Copies an entire list of images based on the image extension to Digital Darkroom.
    """
    options = ["all", "png", "jpg", "jpeg", "cr2", "nef", "tif", "bmp", "other"] # need to be adjusted -> should user be able to type ending?
    user_input = ''
    input_message = input("What files would you like to upload? Press enter and pick an option by entering the number or typing the file extension. Press q to quit.")

    if input_message.lower() == 'q':
        print("You decided to stop the image upload.")
        return

    for index, item in enumerate(options):
        input_message += f'{index+1}) {item}\n'
    while (user_input not in options) and (user_input not in [str(i) for i in range(1, len(options) + 1)]):
        user_input = input(input_message)
    if user_input == 'all' or user_input == "1":
        file_extension = '*.*'
    elif user_input == 'other' or user_input == str(len(options)):
        user_input = input("Enter the extension of the images you would like to add: ")
        file_extension = '*.' + user_input
    elif user_input.isdigit():
        ending = options[int(user_input)-1]
        file_extension = '*.' + ending
    else:
        file_extension = '*.' + user_input

    for full_file_name in glob.glob(os.path.join(source, file_extension)): # copy the whole tree (with subdirs etc), use or glob.glob("path/to/dir/*.*") to get a list of all the filenames
        file_name = os.path.basename(full_file_name)
        if os.path.isfile(full_file_name): # check if results are files
            extract_metadata_upload(full_file_name, dest, file_name)
    print("Images have been copied!\n")

def upload_images():
    """ Uploads images from specified folder by the user in Digital Darkroom.
    """

    # Ask for path to folder from which images will be uploaded 
    upload_from = input("Where are the images you want to upload?\n" 
                            "Please enter the full path from your home directory: (Example: Documents/Images/MyPhotos)\n")
    upload_from = os.path.join(os.environ["HOME_PATH"], upload_from) 

    # Quit function if path cannot be found
    if not os.path.exists(upload_from):
        print("Sorry, the provided path could not be found... Upload aborted.")
        return

    # Ask the user if an event is to be created
    answer = False
    while not answer:
        event_creation = input("Do you want to create an event for your images? (Y/Yes or N/No or Q/Quit) :\n").lower()
        if event_creation in ["y", "yes"]:
            event = create_event()
            
            upload_to = event.path
            answer = True
        elif event_creation in ["n", "no"]:
            answer = True
            upload_to = os.environ["IMAGES_PATH"]
        elif event_creation in ["q", "quit"]:
            return
        else:
            print("Error! Please enter one of the valid options as displayed...")
    
    # Ask the user how to select images to upload
    answer = input("Would you like to add a single image or choose images based on file type?"
                   " Press 1 for single image or 2 for selection based on file type: (Q for Quit)\n").lower() 
                
    while answer not in ["1", "2", "q", "quit"]:
        answer = input("The chosen option is not available. Press 1 for single image upload or 2 for upload based on extension: "
                       "(Q for Quit)\n").lower()
    
    if answer in ['q', "quit"]:
            print("You decided to stop the image upload.")
            return
    if int(answer) == 1:
        single_file(upload_from, upload_to)   
    if int(answer) == 2:
        choose_file_type(upload_from, upload_to)
    
