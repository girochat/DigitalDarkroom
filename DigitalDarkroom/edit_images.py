"""
Module for editing images
"""

# Import the required libraries
import os
import sys
from PIL import (Image, ImageEnhance, ImageFilter)
import display_images as implay

# only to run script locally -> delete later on
#os.environ["IMAGES_PATH"] = os.path.join(os.getcwd(), "Images")

# Define functions
def select_image():
    """ Function to let the user select an image
    """
    image_selected = False
    while not image_selected:

        # Ask user to select an event    (=> used the get_event function in display_images, too much dependency?)
        event_path = implay.get_event()
        if event_path == "":  # => improvement : how to return to run_program directly from get_event in display_images.py?
            return

        # Ask user for name of the image
        image = input("Please enter the full name of the image you would like to edit "
                      "or press 'q'.\n")

        if image in ["q", "quit"]:
            sys.exit()

        path_to_file = os.path.join(event_path, image)
        if os.path.exists(path_to_file):
            img =  Image.open(path_to_file)
            image_selected = True
            return img, event_path
            
        print("Image could not be found. Try again or press q to quit.\n")

def image_filtering(img, event_path):
    """ Let the user select a filter from different options to apply to the image
    """
    func_input = input("What type of image filtering would you like to do?\n"
                       "- Changing the contour => type 'c'\n"
                       "- Edge enhancement => type 'e'\n"
                       "- Blurring => type 'b'\n" 
                       "- Enhancing the details => type 'd'\n"
                       "- Quit the program => type 'Q' or 'quit'\n").lower()
    
    # Define dictionary with the functions the user can use
    func_map = {'c':ImageFilter.CONTOUR,
                'e':ImageFilter.EDGE_ENHANCE,
                'b':ImageFilter.BLUR,
                'd':ImageFilter.DETAIL}
    
    if func_input.strip() == 'quit' or func_input.strip() == 'q':
        print('goodbye!')
        sys.exit()

    if func_input.strip() in func_map.keys():
        func = func_map[func_input]
        im2 = img.filter(func)
        implay.preview(im2, event_path) 
    
    else:
        print("Sorry, the option could not be found!")


def image_enhancement(img, event_path):
    """ Function to let the user apply different image enhancement options
    """
    func_map = {'s':ImageEnhance.Sharpness,
                'b':ImageEnhance.Brightness,
                'col':ImageEnhance.Color,
                'con':ImageEnhance.Contrast}
    
    func_input = input("What type of image enhancement would you like to adjust?\n"
                       "Sharpening => type 's'\n"
                       "Brightness => type 'b'\n"
                       "Color => type 'col'\n"
                       "Contrast => type 'con'\n")
    
    while func_input.strip() not in func_map.keys():
        func_input = input("Could not be found. Try again or press q.\n")
        if func_input.strip() in ["q", "quit"]:
            print('goodbye!')
            sys.exit()
    
    effect = input("How large should the effect be? Enter a number\n"
                   "- smaller than 1 for a reducing effect\n"
                   "- larger than 1 to increase the effect\n"
                   "- or 1 for the original\n"
                   "- or press 'q' or write 'quit' to exit\n")
    
    if func_input.strip() in ["q", "quit"] or effect.strip() in ["q", "quit"]:
        print('goodbye!')
        sys.exit()

    curr_sharp = func_map[func_input](img)
    img_sharped = curr_sharp.enhance(float(effect))
    implay.preview(img_sharped, event_path)
    

def edit():
    """ Function to handle user input for image editing
    """
    # Let the user select the image
    img, event_path = select_image()
    
    quit_editing = False
    while not quit_editing:

        # Display (and launch) program activities to the user
        print("What do you want to do?")
        next_task = input("- Filter an image  => type 'F' or 'filter'\n"
                        "- Enhance an image => type 'E' or 'enhance'\n"
                        "- Go back to the main program => type 'Q' or 'quit'\n").lower()
        
        if next_task in ["f", "filter"]:
            image_filtering(img, event_path)
            
        elif next_task in ["e", "enhance"]:
            image_enhancement(img, event_path)
            
        elif next_task in ["q", "quit"]:
            quit_editing = True
            print("Bye, Bye!\n\n")

        else:
            print("Error! Please enter one of the valid options as displayed...")
           

            