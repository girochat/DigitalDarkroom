"""
Module to display images from a local folder in DigitalDarkroom.

Functions
---------
get_event
    Function to get the path of a specific event chosen by the user.
    
update_view
    Function to get the current image in the stack during the image display. 
    Added as a private method to NavigationToolbar2.
    
stack_back
    Function to move back in the stack of images during the image display. 
    Added as a private method to NavigationToolbar2.

stack_forward
    Function to move forward in the stack of images during the image dispaly. 
    Added as a private method to NavigationToolbar2.

save_image
    Function to save an edited image.

preview
    Function to preview an edited image before saving the changes.

display
    Function to choose the type of image display in the dynamic interface.
    Display can be panorama or diaporama.

display_diaporama
    Function to display images of specific event in diaporama view.
    
display_panorama
    Function to display images of specific event in panorama view.

select_image
    Function to select an image for editing. Called by a pick event on the figure.
    
pick_image
    Function to activate image picking on the display.
"""
import os
import config
import numpy as np
import pandas as pd
import edit_images as imedit
import matplotlib.pyplot as plt
import matplotlib.cbook as cbk
from matplotlib.text import Text
from matplotlib.backend_bases import NavigationToolbar2
from PIL import Image, UnidentifiedImageError


def get_event():
    """ Prompts the user to enter the event from which images will be displayed.
    
    Returns
    -------
    event : str
        the absolute path to the event or to Images if no event specified.
    """
    
    # Ask user to select an event to view images
    answer = False
    while not answer:
        from_event = input("Would you like to view images of a specific event?"
                           " (Y/Yes or N/No or Q/Quit) :\n").lower()
        print()
        if from_event in ["y", "yes"]:
            
            # Display the list of available events
            list_event = np.unique(config.DB["Event"].dropna())
            for event_name in list_event:
                print(event_name)
            event = input("Enter the name of the event from the given list:\n")
            print()
            
            # Handle the case where the event is not in the Images directory
            if not event in os.listdir(config.images_path):
                print("Sorry, the event was not found... \n")
            else:
                event = os.path.join(config.images_path, event)
                answer = True

        elif from_event in ["n", "no"]:
            answer = True
            event = config.images_path
            
        elif from_event in ["q", "quit"]:
            raise SystemExit
        else:
            print("Error! Please enter one of the valid options as displayed...")
     
    return event

def save_image(edited_image, event_path):
    """ Allows to save an edited image in DigitalDarkroom.
    
    Parameters
    ----------
    edited_image : PIL.Image
        the edited image to save
    event_path : str
        the path to event folder containing original image
    """
    
    # Ask user for confirmation
    answer = False
    while not answer:
        answer = input("You asked to save the edited image."
                       " Would you like to preview the changes"
                        " or directly save the edited image?"
                        " (P/Preview or S/Save or Q/Quit)\n").lower()
        print()
        if answer in ["p", "preview"]:
            plt.imshow(edited_image)
            plt.show()
            
            # Ask for confirmation upon closing the preview window
            answer = input("Would you like to save the edited image?"
                           " (S/Save or Q/Quit)\n").lower()
            print()
            
        if answer in ["s", "save"]:
            image_name = input("Enter the name for your edited image: "
                               "(Please specify the extension, ex: .jpg)\n")
            print()
            try:
                edited_image.save(os.path.join(event_path, image_name))
                answer = True
            except ValueError:
                print("Error! The file extension is not valid. Saving aborted.")
                raise SystemExit
            
        elif answer in ["q", "quit"]:
            raise SystemExit
        else:
            print("Error! Please enter one of the valid options as displayed...")
            answer = False
    
def preview(edited_image, event_path):
    """ Preview edited changes of an image.
    
    Parameters
    ----------
    edited_image : PIL.Image 
        the edited image to preview
    event_path : str
        the path to event folder containing original image
    """ 
    
    plt.imshow(edited_image)
    plt.axis('off')
    plt.show()
    
    answer = False
    while not answer:
        answer = input("Would you like to save the edited image? (S/Save or Q/Quit)\n").lower()
        print()
        if answer in ["s", "save"]:
            save_image(edited_image, event_path)
        elif answer in ["q", "quit"]:
            raise SystemExit
        else:
            print("Error! Please enter one of the valid options as displayed...")
            answer = False

def update_view(self):
    """ Updates image display from the current position in the image stack. 
    Triggered by the dynamic toolbar.
    """
    
    # Get current image
    current = self.image_stack()
    
    # Handle the case where no stack was stored
    if current is None:
        return
    else:
        
        # Update the panorama display
        if NavigationToolbar2.view == "panorama":
            plt.close()
        
            # Create an empty image to fill the gaps of the panorama
            empty_image = Image.new("1", (600, 480), 1)
        
            figure, axes = plt.subplots(3, 5)
            for index, image_name in enumerate(current):
                i = int(index / 5)
                j = int(index % 5)
                if image_name is None:
                    axes[i, j].imshow(empty_image)
                else:
                    
                    # Handle the case where the filepath is not an image 
                    try:
                        image = Image.open(os.path.join(config.images_path, config.DB.loc[image_name, "Event"], image_name))
                        height = int(image.size[0] / 20)
                        width = int(image.size[1] / 20)
                        axes[i, j].imshow(image.resize((height, width)))
                        
                        # Activate selecting the image by picking the title or not
                        if NavigationToolbar2.picker:
                            axes[i, j].set_title(f"{image_name}", fontsize=7).set_picker(True)
                        else:
                            axes[i, j].set_title(f"{image_name}", fontsize=7)
                            
                    except UnidentifiedImageError:
                        axes[i, j].imshow(empty_image)
                axes[i, j].set_axis_off()
                
            if NavigationToolbar2.picker:
                plt.connect(s = "pick_event", func = select_image)
            plt.show()
        
        # Update the diaporama display
        else:
            plt.close()
            try:
                image = Image.open(os.path.join(config.images_path, config.DB.loc[current, "Event"], current))
                height = int(image.size[0] / 4)
                width = int(image.size[1] / 4)
                plt.imshow(image.resize((height, width)))
                
                # Activate selecting the image by picking the title or not
                if NavigationToolbar2.picker:
                    plt.connect(s = "pick_event", func = select_image)
                    plt.title(f"{current}", fontsize=7, picker = True)
                else:
                    plt.title(f"{current}", fontsize=7)
                plt.axis('off')
                plt.show()
            except UnidentifiedImageError:
                pass
        
def stack_back(self, *args, **kwargs):
    """ Goes backward in the stack of image. Triggered by the dynamic toolbar.
    """
    self.image_stack.back()
    self.update_view()
        
def stack_forward(self, *args, **kwargs):
    """ Goes forward in the stack of image. Triggered by the dynamic toolbar.
    """
    self.image_stack.forward()
    self.update_view()

def set_toolbar(picker):
    """ Adds personalised method to the NavigationToolbar2 class for the image display.
    
    Parameters
    ----------
    picker : bool
        specify if the images can be picked or not on the display.
    """
    # Personalise the toolbar by adding a viewing method and keeping track of the current event
    NavigationToolbar2.update_view = update_view
    
    # Specify if the image names can be picked
    NavigationToolbar2.picker = picker
    
    # Override the toolbar functions 'back' and 'forward' to move in the image stack
    original_back = NavigationToolbar2.back
    NavigationToolbar2.back = stack_back
    original_forward = NavigationToolbar2.forward
    NavigationToolbar2.forward = stack_forward
            
def display_diaporama(images, picker):
    """ Displays images in a diaporama using a dynamic interface.
        
    Parameters
    ----------
    images : list
        the list of images to display in diaporama
        
    picker : bool
        specify if the images can be picked or not on the display.
    """
    set_toolbar(picker)
    NavigationToolbar2.view = "diaporama"
    
    # Personalise the toolbar by adding the stack of images
    image_stack = cbk.Stack()
    image_stack._elements = images
    image_stack._pos = 0
    NavigationToolbar2.image_stack = image_stack

    # Start the image display
    image = Image.open(os.path.join(config.images_path, config.DB.loc[images[0], "Event"], images[0])) 
    height = int(image.size[0] / 4)
    width = int(image.size[1] / 4)
    plt.imshow(image.resize((height, width)))
    plt.title(f"{images[0]}", fontsize=7, picker = True)
    plt.axis("off")
    plt.show()
    
def display_panorama(images, picker):
    """ Displays images in a panorama using a dynamic interface.
    
    Parameters
    ----------
    images : list
        the nested list with groups of images to display in panorama

    picker : bool
        specify if the images can be picked or not on the display.
    """
    set_toolbar(picker)
    NavigationToolbar2.view = "panorama"
    
    # Fill the gaps such that the image list is a multiple of 15
    number_gaps = 15 - (len(images) % 15)
    
    # Create an empty image to fill the gaps of the panorama
    empty_image = Image.new("1", (600, 480), 1)
    
    # Create a nested list with elements of 15 images  
    group_images = list(np.concatenate((
        np.array(images), np.repeat((None), number_gaps))).reshape(int(len(images) / 15) + 1, 15))
    
    # Personalise the toolbar by adding the stack of image groups
    image_stack = cbk.Stack()
    image_stack._elements = group_images
    image_stack._pos = 0
    NavigationToolbar2.image_stack = image_stack
    
    # Start the panorama display (15 images in 3 rows and 5 columns)
    figure = plt.gcf()
    axes = figure.subplots(3, 5)
    for index, image_name in enumerate(group_images[0]):
        i = int(index / 5)
        j = int(index % 5)
        if image_name is None:
            axes[i, j].imshow(empty_image)
        else:
            try:
                image = Image.open(os.path.join(config.images_path, config.DB.loc[image_name, "Event"], image_name))
                height = int(image.size[0] / 20)
                width = int(image.size[1] / 20)
                axes[i, j].imshow(image.resize((height, width)))
                axes[i, j].set_title(f"{image_name}", fontsize=7).set_picker(True)
            except UnidentifiedImageError:
                axes[i, j].imshow(empty_image)
        axes[i, j].set_axis_off()
    plt.show()
    
def display(picker = False):
    """ Asks the user if the display must be a diaporama or panorama and launches the display.
    
    Parameters
    ----------
    picker : bool
        specify if the images can be picked or not on the display.
    """
    
    answer = False
    while not answer:
        answer = input("Would you like to view the images in a diaporama or panorama?"
                   " (D/Diaporama or P/Panorama or Q/Quit):\n").lower()
        print()
        
        if answer in ["q", "quit"]:
            raise SystemExit
        elif answer in ["d", "diaporama", "p", "panorama"]:

            # Load images to display
            event_path = get_event()
            event = os.path.basename(event_path)
            images = list(config.DB["Event"].index)

            # Launch the appropriate display
            if answer in ["d", "diaporama"]:
                display_diaporama(images, picker)
            else:
                display_panorama(images, picker)

        else:
            print("Error! Please enter one of the valid options as displayed...")
            answer = False

def select_image(pick_event):
    """ Returns the image name that has been picked by user.
    
    Parameters
    ----------
    pick_event : matplotlib.backend_bases.PickEvent
        the event that was picked on the figure.
    """
    if isinstance(pick_event.artist, Text):
        plt.close()
        title = pick_event.artist
        image = title.get_text()
        imedit.edit(image)
    
def pick_image():
    """ Pick an image in the panorama display.
    
    Returns
    -------
    image : str
        the name of the image.
    """
    
    # Allow selecting the image by picking its name
    plt.connect(s = "pick_event", func = select_image)
    display(picker = True)