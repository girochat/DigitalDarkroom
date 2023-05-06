"""
Issues: 
- not all images have metadata that can be extracted -> creation date of image not always available (how should this be handled)
- datetime issues
- sorting option -> needs to be improved, pandas dataframe should be sortable by date and other options
- open question: do all images have the data stored with the same tags? Or do we have to make separate function for each datatype to get the 
 date of when the picture was taken?

"""
import pandas as pd
import numpy as np
import os
from PIL import Image, ExifTags, UnidentifiedImageError
from datetime import datetime
import shutil

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
    df = []
    ext = ["png", "jpg", "jpeg", "cr2", "nef", "tif", "bmp"]
    with os.scandir(path_to_event_folder) as it:
        for entry in it:
            im_ext = entry.name.split(".")[-1]
            if not entry.name.startswith('.') and entry.is_file() and im_ext in ext:
                path_to_img = os.path.join(path_to_event_folder, entry.name)
                im = Image.open(path_to_img)
                exifdata = im.getexif()
                if exifdata is None or 306 not in exifdata.keys():
                    date_time = pd.NaT
                    date = pd.NaT
                else:
                    date_time = exifdata[306]
                    date = get_date_from_string(date_time)
                event = os.path.basename(os.path.normpath(path_to_event_folder)) 
                megapixels = (im.size[0]*im.size[1]/1000000) # Megapixels
                t = len(Image.Image.getbands(im)) # Number of channels
                timestamp = os.path.getctime(path_to_img)
                creation = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                df.append({'Filename':entry.name, 'Event':event, 'Format':im.format, 'Width':im.size[0], 'Height':im.size[1], 'Megapixels':megapixels, 'Channels':t, 'Mode':im.mode, 'Timestamp': timestamp, 'Creation':creation,  'Date_Time':date_time, 'Date': date})
    filedf = pd.DataFrame(df)  
    return filedf


############################################################
# Create DataFrame to store image metadata and upload images
############################################################

def extract_metadata_upload(full_file_name, dest, filename):
    """ Extract metadata when images are uploaded and include it into the database image_DB
    """
    image_DB = pd.read_pickle(os.path.join(os.environ["PROGRAM_PATH"],"image_DB.pkl"))
    #image_DB = pd.DataFrame(columns = ['Filename', 'Event','Format', 'Width', 'Height', 'Megapixels', 'Channels', 'Mode', 'Timestamp', 'Creation', 
                                                #'Date_Time', 'Date']).set_index("Filename")
                                           
    try:
        im = Image.open(full_file_name)
        exifdata = im._getexif()
        if exifdata is None or 306 not in exifdata.keys():
            date_time = pd.NaT
            date = pd.NaT
        else:
            date_time = exifdata[306]
            date = get_date_from_string(date_time)
        event = os.path.basename(os.path.normpath(dest)) 
        megapixels = (im.size[0]*im.size[1]/1000000) # Megapixels
        t = len(Image.Image.getbands(im)) # Number of channels
        timestamp = os.path.getctime(full_file_name) # Timestamp
        creation = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S') #to convert timestamp to datetime
        new_row = {'Filename':filename, 'Event':event, 'Format':im.format, 'Width':im.size[0], 'Height':im.size[1], 'Megapixels':megapixels, 'Channels':t, 'Mode':im.mode, 'Timestamp': timestamp, 'Creation':creation,  'Date_Time':date_time, 'Date': date}
        image_DB.loc[filename] = pd.Series(new_row)
        image_DB.to_pickle(os.path.join(os.environ["PROGRAM_PATH"], "image_DB.pkl"))
        shutil.copy(full_file_name, dest)
        return image_DB
    except UnidentifiedImageError:
        print("Not an image")

    
# Function to sort image_DB based on a column name
def sort_image_DB(colname = 'Date'):
    """ Sort image_DB based on a column
    """
    return os.path.join(os.environ["PROGRAM_PATH"], "image_DB.pkl").sort_values(colname)

def sort_images_list(metadata_df, column = "Date", ascending = False):
    """ Sort images in an event folder based on a column
    """
    sorted_images = metadata_df.sort_values(column, ascending= ascending)
    sorted_filenames = sorted_images['Filename'].values
    return sorted_filenames


def sorting(path_to_event_folder):
    """ Ask user if images should be sorted by date or size
    """
    choice = input("Would you like to sort the images based on date or size? Press 1 for creation date, 2 for size. ")
    t = extract_metadata(path_to_event_folder)
    if choice == "1":
        order = input("Type True for ascending and False for descending. ")
        images_list = sort_images_list(t, column = "Date", ascending = bool(order))
    elif choice == "2":
        images_list = sort_images_list(t, column = "Megapixels")
    else:
        images_list = t['Filename'].values
        print("The images will not be sorted.")
    return images_list



########################################################
# testing exifdata
########################################################


def get_exifdata(path_to_event_folder, img):
    """ Extract exifdata from image if available and display it
    """
    p = os.path.join(path_to_event_folder, img)
    im = Image.open(p)
    exifdata = im.getexif()
    if exifdata is None:
        print('Sorry, image has no exif data.')
    else:
        for key, val in exifdata.items():
            if key in ExifTags.TAGS:
                print(f'{ExifTags.TAGS[key]}:{val}')
    return exifdata





"""
if __name__ == "__main__":
    
    filename = "chessboard.jpeg"
    path_to_event_folder = os.path.join(os.getcwd(), "DigitalDarkroom/Images/test/")   # add path to folder with images -> needs to be changed
    path_for_upload = os.path.join(os.getcwd(), "gallery/") 
    full_file_name = os.path.join(path_for_upload, filename)
    path_to_program = os.path.join(os.getcwd(), "DigitalDarkroom/")
    
    f = extract_metadata(path_to_event_folder)
    exif = get_exifdata(path_to_event_folder, "IMG_20200401_161104.jpg")
    extract_metadata_upload(full_file_name, dest = path_to_event_folder, filename = filename)
    get_exifdata("gallery", "IMG_6560.jpg")
"""
