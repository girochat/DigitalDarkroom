"""
Module to display images from a local folder in DigitalDarkroom.

Functions
---------
get_event
    Function to get the path of a specific event chosen by the user.
    
load_images
    Function to load new images in an existing or new event.
    
update_view
    Function to get the current image in the stack during the image display. 
    Added as a public method to NavigationToolbar2.
    
stack_back
    Function to move back in the stack of images during the image display. 
    Added as a public method to NavigationToolbar2.

stack_forward
    Function to move forward in the stack of images during the image dispaly. 
    Added as a public method to NavigationToolbar2.

save_image
    Function to save an edited image.

preview
    Function to preview an edited image before saving the changes.

display
    Function to display the images of an event in a dynamic interface.

display_diaporama

display_panorama
   
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cbook as cbk
from matplotlib.backend_bases import NavigationToolbar2
from PIL import Image, UnidentifiedImageError

def get_event():
    """ Prompts the user to enter the event from which images will be displayed.
    """
    
    # Ask user to select an event to view images
    answer = False
    while not answer:
        from_event = input("Would you like to view images of a specific event?"
                           " (Y/Yes or N/No or Q/Quit) :\n").lower()
        print()
        if from_event in ["y", "yes"]:
            
            # Display the list of available events
            list_event = np.unique(pd.read_pickle(os.path.join(os.environ["PROGRAM_PATH"],"image_DB.pkl"))["Event"].dropna())
            for event_name in list_event:
                print(event_name)
            event = input("Enter the name of the event from the given list:\n")
            print()
            
            # Handle the case where the event is not in the Images directory
            if not event in os.listdir(os.environ["IMAGES_PATH"]):
                print("Sorry, the event was not found... \n")
            else:
                event = os.path.join(os.environ["IMAGES_PATH"], event)
                answer = True

        elif from_event in ["n", "no"]:
            answer = True
            event = os.environ["IMAGES_PATH"]
            
        elif from_event in ["q", "quit"]:
            raise SystemExit
        else:
            print("Error! Please enter one of the valid options as displayed...")
     
    return event

def load_images():
    """ Loads images from a given list of image filenames.
    """
    
    # Ask user for a particular event to load images
    path_event = get_event()
    
    # Get list of images in event
    images_list = [image for image in os.listdir(path_event) if os.path.isfile(os.path.join(path_event, image))]
    all_images = []
    
    # Load images from file
    for image in images_list:
        
        # Handle the case where the file is not an image (=> use the df image_DB?)
        try:
            loaded_img = Image.open(os.path.join(path_event, image))
            all_images.append(loaded_img)
        except UnidentifiedImageError:
            pass
    
    return all_images

def save_image(edited_image, event_path):
    """ Allows to save an edited image in DigitalDarkroom.
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
            plt.imshow(image)
            plt.show()
            answer = input("Would you like to save the edited image?"
                           " (S/Save or Q/Quit)\n").lower()
            print()
            
        elif answer in ["s", "save"]:
            image_name = input("Enter the name for your edited image: "
                               "(Please specify the extension, ex: .jpg)\n")
            print()
            try:
                edited_image.save(os.path.join(event_path, image_name))
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
            for index, image in enumerate(current):
                i = int(index / 5)
                j = int(index % 5)
                if image is None:
                    axes[i, j].imshow(empty_image)
                else:
                    
                    # Handle the case where the filepath is not an image 
                    try:
                        image = Image.open(os.path.join(NavigationToolbar2.event, image))
                        height = int(image.size[0] / 4)
                        width = int(image.size[1] / 4)
                        axes[i, j].imshow(image.resize((height, width)))
                        axes[i, j].set_title(f"Image number = {index + 15 * self.image_stack._pos}", fontsize=7)
                    except UnidentifiedImageError:
                        axes[i, j].imshow(empty_image)
                axes[i, j].set_axis_off() 
            plt.show()
        
        # Update the diaporama display
        else:
            plt.close()
            try:
                image = Image.open(os.path.join(NavigationToolbar2.event, current))
                height = int(image.size[0] / 4)
                width = int(image.size[1] / 4)
                plt.imshow(image.resize((height, width)))
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
            
def display_diaporama(images):
    """ Displays images in a diaporama using a dynamic interface.
    """
    # Personalise the toolbar by adding the stack of images
    image_stack = cbk.Stack()
    image_stack._elements = images
    image_stack._pos = 0
    NavigationToolbar2.image_stack = image_stack

    # Start the image display
    image = Image.open(os.path.join(NavigationToolbar2.event, images[0])) 
    height = int(image.size[0] / 4)
    width = int(image.size[1] / 4)
    plt.imshow(image.resize((height, width)))
    plt.axis("off")
    plt.show()
    
def display_panorama(images):
    """ Displays images in a panorama using a dynamic interface. 
    """
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
    figure, axes = plt.subplots(3, 5)
    for index, image in enumerate(group_images[0]):
        i = int(index / 5)
        j = int(index % 5)
        if image is None:
            axes[i, j].imshow(empty_image)
        else:
            try:
                image = Image.open(os.path.join(NavigationToolbar2.event, image))
                height = int(image.size[0] / 4)
                width = int(image.size[1] / 4)
                axes[i, j].imshow(image.resize((height, width)))
                axes[i, j].set_title(f"Image number = {index}", fontsize=7)
            except UnidentifiedImageError:
                axes[i, j].imshow(empty_image)
        axes[i, j].set_axis_off()
    plt.show()
    
def display():
    """ Asks the user if the display must be a diaporama or panorama and launches the display. 
    """
    answer = input("Would you like to view the images in a diaporama or panorama?"
                   " (D/Diaporama or P/Panorama or Q/Quit):\n").lower()
    print()
    
    if answer in ["q", "quit"]:
        raise SystemExit
    else:
        
        # Load images to display
        event_path = get_event()
        event = os.path.basename(event_path)
        event_DB = pd.read_pickle(os.path.join(os.environ["PROGRAM_PATH"],"image_DB.pkl"))["Event"]
        images = list(pd.Series(event_DB[event_DB == event].index))
        
        # Personalise the toolbar by adding a viewing method and keeping track of the current event
        NavigationToolbar2.update_view = update_view
        NavigationToolbar2.event = event_path
        
        # Override the toolbar functions 'back' and 'forward' to move in the image stack
        original_back = NavigationToolbar2.back
        NavigationToolbar2.back = stack_back
        original_forward = NavigationToolbar2.forward
        NavigationToolbar2.forward = stack_forward
        
        # Launch the appropriate display
        if answer in ["d", "diaporama"]:
            NavigationToolbar2.view = "diaporama"
            display_diaporama(images)
        
        elif answer in ["p", "panorama"]:
            NavigationToolbar2.view = "panorama"
            display_panorama(images)
            
        # Re-implement default toolbar functions
        NavigationToolbar2.back = original_back
        NavigationToolbar2.forward = original_forward