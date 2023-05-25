"""
Module to display images from a local folder in DigitalDarkroom.

Functions
---------
get_event
    Function to get the path of a specific event chosen by the user.

save_image
    Function to save an edited image.

preview
    Function to preview an edited image before saving the changes.
    
update_view
    Function to get the current image in the stack during the image display. 
    Added as a private method to NavigationToolbar2.
    
stack_back
    Function to move back in the stack of images during the image display. 
    Added as a private method to NavigationToolbar2.

stack_forward
    Function to move forward in the stack of images during the image dispaly. 
    Added as a private method to NavigationToolbar2.
    
set_figure
    Function to initialise a new figure with a personalised NavigationToolbar2.

display
    Function to choose the type of image display in the dynamic interface.
    Display can be panorama or diaporama.

display_diaporama
    Function to display images of specific event in diaporama view.
    
display_panorama
    Function to display images of specific event in panorama view.

select_image
    Function to select an image for editing. Called by a pick event on the figure.

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
    
    # Ask user to select an event from which to view images
    event = False
    while not event:

        # Display the list of available events
        list_event = np.unique(config.DB["Event"].dropna())
        for event_name in list_event:
            print(event_name)
        event = input("Enter the name of an event (Press 'enter' for no event or Q/Quit):\n").strip()
        print()
            
        # Handle the case where the event is not in the Images directory
        if event in os.listdir(config.images_path) or event == "":
            event = os.path.join(config.images_path, event)
            
        elif event in ["q", "quit"]:
            raise SystemExit
        else:
            print("Sorry, the event was not found... \n")
            event = False
            
    return event

def save_image(edited_image, image_name):
    """ Allows to save an edited image in DigitalDarkroom.
    
    Parameters
    ----------
    edited_image : PIL.Image
        the edited image to save
    image_name : str
        the name of the original image
    """
    
    # Ask user for confirmation
    answer = False
    while not answer:
        answer = input("Would you like to replace the original or"
                        " save the edited image as a new image?"
                        " (R/Replace or S/Save or Q/Quit)\n").lower()
        print()
   
        if answer in ["s", "save"]:
            
            # Create new name for the edited image
            name_components = image_name.split(".")
            edited_image_name = name_components[0] + "_2." + name_components[1]
            duplicate = 3
            while edited_image_name in config.DB.index:
                edited_image_name = name_components[0] + f"_{duplicate}." + name_components[1]
                duplicate += 1
            
            # Save image file in Images
            event = config.DB.loc[image_name, "Event"]
            edited_image.save(os.path.join(config.images_path, event, edited_image_name))
                
            # Update DB
            new_row = config.DB.loc[image_name].copy()
            new_row["Edited"] = True
            config.DB.loc[edited_image_name] = new_row
            config.DB.to_pickle(os.path.join(config.program_path, "image_DB.pkl"))
            answer = True

        elif answer in ["r", "replace"]:
            
            # Replace image file in Images
            event = config.DB.loc[image_name, "Event"]
            edited_image.save(os.path.join(config.images_path, event, image_name))
                
            # Update DB
            config.DB.loc[image_name, "Edited"] = True
            config.DB.to_pickle(os.path.join(config.program_path, "image_DB.pkl"))
            
        elif answer in ["q", "quit"]:
            raise SystemExit
        else:
            print("Error! Please enter one of the valid options as displayed...")
            answer = False
    raise SystemExit
    
def preview(edited_image, image_name):
    """ Preview edited changes of an image.
    
    Parameters
    ----------
    edited_image : PIL.Image 
        the edited image to preview
    image_name : str
        the name of the original image
    """ 
    
    # Initialise a new figure of fixed size
    toolbar = plt.rcParams['toolbar']
    plt.rcParams['toolbar'] = 'None'
    plt.figure()
    fig_manager = plt.get_current_fig_manager()
    fig_manager.resize(2500, 1500)  
    
    # Preview edited image
    plt.imshow(edited_image)
    plt.axis('off')
    plt.show()
    
    # Save the edited image
    plt.rcParams['toolbar'] = toolbar
    save_image(edited_image, image_name)

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
            plt.close('all')
            figure, axes = plt.subplots(3, 5)
            fig_manager = plt.get_current_fig_manager()
            fig_manager.resize(2500, 1500)
            
            # Create an empty image to fill the gaps of the panorama
            empty_image = Image.new("1", (600, 480), 1)
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
            plt.close('all')
            figure = plt.figure()
            fig_manager = plt.get_current_fig_manager()
            fig_manager.resize(2500, 1500)
            
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

def set_figure(picker):
    """ Creates a new figure with personalised methods for the NavigationToolbar2.
    
    Parameters
    ----------
    picker : bool
        specify if the images can be picked or not on the display.
    """
    # Create new figure
    figure = plt.figure()
    fig_manager = plt.get_current_fig_manager()
    fig_manager.resize(2500, 1500)
    
    # Personalise the figure toolbar by adding a viewing method and keeping track of the current event
    NavigationToolbar2.update_view = update_view
    
    # Specify if the image names can be picked
    NavigationToolbar2.picker = picker
    
    # If picking mode, allow selecting the image by picking its name
    if picker:
        plt.connect(s = "pick_event", func = select_image)
    
    # Override the toolbar functions 'back' and 'forward' to move in the image stack
    original_back = NavigationToolbar2.back
    NavigationToolbar2.back = stack_back
    original_forward = NavigationToolbar2.forward
    NavigationToolbar2.forward = stack_forward
    
    return figure
            
def display_diaporama(images, picker):
    """ Displays images in a diaporama using a dynamic interface.
        
    Parameters
    ----------
    images : list
        the list of images to display in diaporama
        
    picker : bool
        specify if the images can be picked or not on the display.
    """
    figure = set_figure(picker)
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
    figure = set_figure(picker)
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
            images = list(config.DB[config.DB["Event"] == event].index)

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
        plt.close('all')
        title = pick_event.artist
        image = title.get_text()
        try:
            imedit.edit(image)
        except SystemExit:
            pass
    else:
        raise SystemExit