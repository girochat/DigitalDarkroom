"""
Module to edit images and apply different enhancing filters.

Functions
---------
select_image
    Function to select which image to edit.
    
filter_image
    Function to apply filters for contour, edge enhancement, blurring and detail enhancement.
    
enhance_image
    Function to enhance brightness, sharpness, colour or contrast.

rotate_image
    Function to rotate an image by 90, 180 or 270 degrees.

edit
    Function to select the editing option.
"""

# Import the required libraries
import os
import sys
import config
from PIL import (Image, ImageEnhance, ImageFilter)
import display_images as implay

def select_image():
    """ Select an image either by entering its name or picking in image display.
    
    Returns
    -------
    image : str
        the image name to edit.
    """
    # Ask user how to select the image to edit
    answer = False
    while not answer:
        answer = input("Would you like to pick a specific image in the display"
                        " or enter the name of a particular image?"
                       " (P/Pick or N/Name or Q/Quit)\n").lower().strip()
        print()
 
        if answer in ["p", "pick"]:
            implay.display(picker = True)
                
        elif answer in ["n", "name"]:
            image = input("Enter the name of the image: (Q/Quit)\n")
                
            # Check that image exists in program database
            if image not in config.DB.index:
                print("The image could not be found...\n")
                answer = False
            else:
                edit(image)
        
        elif answer in ["q", "quit"]:
            raise SystemExit      
        else:
            print("Error! Please enter one of the valid options as displayed...")
            answer = False
            

def filter_image(img, image_name):
    """ Let the user select a filter from different options to apply to the image
    
    Parameters
    ----------
    img : PIL.Image
        the image to apply filter on.
    
    image_name : str
        the name of the original image
    """
    func_input = input("What type of image filtering would you like to do?\n"
                       "- Changing the contour => type 'c'\n"
                       "- Edge enhancement => type 'e'\n"
                       "- Blurring => type 'b'\n" 
                       "- Enhancing the details => type 'd'\n"
                       "- Quit the program => type 'Q' or 'quit'\n").lower().strip()
    
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
        implay.preview(im2, image_name) 
    
    else:
        print("Sorry, the option could not be found!")


def enhance_image(img, image_name):
    """ Function to let the user apply different image enhancement options
    
    Parameters
    ----------
    img : PIL.Image
        the image to apply filter on.
    
    image_name : str
        the name of the original image.
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
    implay.preview(img_sharped, image_name)

def rotate_image(img, image_name):
    """ Function to let the user rotate an image.
    
    Parameters
    ----------
    img : PIL.Image
        the image to rotate.
    
    image_name : str
        the name of the original image.
    """

    func_map = {'90':Image.ROTATE_90,
                '180':Image.ROTATE_180,
                '270':Image.ROTATE_270}
    
    func_input = input("How many degrees would you like to rotate the image?\n"
                       "Type 90, 180 or 270\n")
    
    while func_input.strip() not in func_map.keys():
        func_input = input("Could not be found. Try again or press q.\n")
        if func_input.strip() in ["q", "quit"]:
            print('goodbye!')
            sys.exit()

    img_transposed = img.transpose(func_map[func_input])
    implay.preview(img_transposed, image_name)    

def edit(image_name):
    """ Function to handle user input for image editing.
    
    Parameters
    ----------
    image_name : str
        the image name to edit.
    """
    # Load the image
    event_path = os.path.join(config.images_path, config.DB.loc[image_name, "Event"])
    image = Image.open(os.path.join(event_path, image_name))

    quit_editing = False
    while not quit_editing:

        # Display (and launch) program activities to the user
        print("What do you want to do?")
        next_task = input("- Filter an image  => type 'F' or 'filter'\n"
                          "- Enhance an image => type 'E' or 'enhance'\n"
                          "- Rotate image => type 'R' or 'rotate'\n"
                          "- Go back to the main program => type 'Q' or 'quit'\n").lower()
        
        if next_task in ["f", "filter"]:
            filter_image(image, image_name)
            
        elif next_task in ["e", "enhance"]:
            enhance_image(image, image_name)

        elif next_task in ["r", "rotate"]:
            rotate_image(image, image_name)

        elif next_task in ["q", "quit"]:
            raise SystemExit

        else:
            print("Error! Please enter one of the valid options as displayed...")