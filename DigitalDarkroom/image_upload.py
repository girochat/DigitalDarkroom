# To do
# -----------------
# change paths so that they work within the DigitalDarkroom folder / env. variables => Done.
# improve function choose file type -> see comments
# Include error handling, try-except
# Make user interaction more friendly

import os
import shutil
import glob
from extract_metadata import extract_metadata_upload
import pandas as pd

#############################################
# create folder for event
#############################################
def create_event_folder():
    """ Creates an event folder for the images to upload.
    """
    name_eventfolder = input("Would you like to name the event folder? Press Y or N\n")
    if name_eventfolder.lower() == "y":
        name_eventfolder = input("Enter a name: ")
        path_to_eventfolder = os.path.join(os.environ["IMAGES_PATH"], name_eventfolder) 
        if not os.path.exists(path_to_eventfolder):
            os.makedirs(path_to_eventfolder)
            print("Your folder has been created")
        dest = path_to_eventfolder
    else:
        print("Lets continue then") # folders will be uploaded into Images  # What happens if no event name? Could we have a miscellaneous folder for no named event? 
        dest = ""
    return dest


################
# upload images 
################


def upload_type(source, dest):
    """ Asks the user what kind of image upload is requested
    """
    answer = input("Would you like to add a single image or choose images based on file type? Press 1 for single image, 2 for selection based on file type or q to quit. ")
    while answer not in ["1", "2", "q"]:
        answer = input("The chosen option is not available. Press 1 for single image upload, 2 for upload based on extension or q to quit. ")
    
    if answer.lower() == 'q':
            print("You decided to stop the image upload.")
            return
    if int(answer) == 1:
        single_file(source, dest)
        
    if int(answer) == 2:
        choose_file_type(source, dest)
    
def single_file(source, dest):
    """ Copies a single image to Digital Darkroom.
    """
    filename = input("Enter the name of the file you would like to upload or press q to quit. ")
    
    if filename.lower() == 'q':
        print("You decided to stop the image upload.")
        return
    path_to_file = os.path.join(source, filename)
    if os.path.isfile(path_to_file): # check if results are files
        shutil.copy(path_to_file, dest)
    else:
        print("Sorry, the image could not be found... Upload aborted.")
        return



#################################################
#different file formats (options to select from) 
##################################################      
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
    print("Files have been copied")

def upload_images():
    """ Uploads images from specified folder by the user in Digital Darkroom.
    """

    # Ask for path to folder where images are to be uploaded 
    path_for_upload = input("Where are the images you want to upload?\n" 
                            "Please enter the full path from your home directory: (Example: Documents/Images/MyPhotos)\n")
    path_for_upload = os.path.join(os.environ["HOME_PATH"], path_for_upload) # folder with images that should be uploaded

    # Quit function if path cannot be found
    if not os.path.exists(path_for_upload):
        print("Sorry, the provided path could not be found...")

    path_to_event_folder = create_event_folder()
    

    upload_type(source = path_for_upload, dest = path_to_event_folder)


"""
path_to_event_folder = os.path.join(os.getcwd(), "DigitalDarkroom/Images/test/")   # add path to folder with images -> needs to be changed
path_to_program = os.path.join(os.getcwd(), "DigitalDarkroom/")
path_for_upload = os.path.join(os.getcwd(), "gallery/")
upload_type(path_for_upload, path_to_event_folder)  
image_DB = pd.read_pickle(os.path.join(path_to_program,"image_DB.pkl"))
print(image_DB)

"""