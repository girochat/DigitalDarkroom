"""
Issues: 
- not all images have metadata that can be extracted 
    -> creation date of image not always available (how should this be handled)
- datetime issues
- sorting option needs to be improved, database should be sortable by date and other options
- open question: do all images have the data stored with the same tags? 
"""
import os
import shutil
from datetime import datetime
import pandas as pd
import numpy as np
from PIL import (Image, ExifTags, UnidentifiedImageError)


##################################
# make pandas dataframe with infos
##################################

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

def extract_metadata(path_to_event_folder):
    """ Extract metadata from an event folder that is already generated
    """
    metadata_event = []
    ext = ["png", "jpg", "jpeg", "cr2", "nef", "tif", "bmp"]
    with os.scandir(path_to_event_folder) as event_images:
        for entry in event_images:
            im_ext = entry.name.split(".")[-1]
            if not entry.name.startswith('.') and entry.is_file() and im_ext in ext:
                path_to_img = os.path.join(path_to_event_folder, entry.name)
                img = Image.open(path_to_img)
                exifdata = img.getexif()
                if exifdata is None or 306 not in exifdata.keys():
                    date_time = pd.NaT
                    date = pd.NaT
                else:
                    date_time = exifdata[306]
                    date = get_date_from_string(date_time)
                event = os.path.basename(os.path.normpath(path_to_event_folder))
                megapixels = img.size[0]*img.size[1]/1000000 # Megapixels
                nr_channels = len(Image.Image.getbands(img)) # Number of channels
                timestamp = os.path.getctime(path_to_img)
                creation = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                metadata_dic = {'Filename':entry.name,
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
                metadata_event.append(metadata_dic)
    metadata_event_pd = pd.DataFrame(metadata_event)
    return metadata_event_pd


############################################################
# Create DataFrame to store image metadata and upload images
############################################################

def extract_metadata_upload(full_file_name, dest, filename):
    """ Extract metadata when images are uploaded and include it into the database image_DB
    """
    image_db = pd.read_pickle(os.path.join(os.environ["PROGRAM_PATH"],"image_DB.pkl"))
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
        image_db.loc[filename] = pd.Series(new_row)
        image_db.to_pickle(os.path.join(os.environ["PROGRAM_PATH"], "image_DB.pkl"))
        shutil.copy(full_file_name, dest)
        return image_db
    except UnidentifiedImageError:
        print("Not an image")


# Function to sort image_DB based on a column name
def sort_image_db(colname = 'Date'):
    """ Sort image_DB based on a column
    """
    sort_by_column = os.path.join(os.environ["PROGRAM_PATH"], "image_DB.pkl").sort_values(colname)
    return sort_by_column

def sort_images_list(metadata_df, column = "Date", ascending = False):
    """ Sort images in an event folder based on a column
    """
    sorted_images = metadata_df.sort_values(column, ascending= ascending)
    sorted_filenames = sorted_images['Filename'].values
    return sorted_filenames


def sorting(path_to_event_folder):
    """ Ask user if images should be sorted by date or size
    """
    choice = input("Would you like to sort the images based on date or size?\n"
                   "Press 1 for creation date, 2 for size. ")
    metadata_event = extract_metadata(path_to_event_folder)
    if choice == "1":
        order = input("Type True for ascending and False for descending. ")
        images_list = sort_images_list(metadata_event, column = "Date", ascending = bool(order))
    elif choice == "2":
        images_list = sort_images_list(metadata_event, column = "Megapixels")
    else:
        images_list = metadata_event['Filename'].values
        print("The images will not be sorted.")
    return images_list



########################################################
# testing exifdata
########################################################


def get_exifdata(path_to_event_folder, img):
    """ Extract exifdata from image if available and display it
    """
    path_to_image = os.path.join(path_to_event_folder, img)
    img = Image.open(path_to_image)
    exifdata = img.getexif()
    if exifdata is None:
        print('Sorry, image has no exif data.')
    else:
        for key, val in exifdata.items():
            if key in ExifTags.TAGS:
                print(f'{ExifTags.TAGS[key]}:{val}')
    return exifdata

