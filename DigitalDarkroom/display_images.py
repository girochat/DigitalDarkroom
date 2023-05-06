import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cbook as cbk
from matplotlib.backend_bases import NavigationToolbar2
from PIL import Image, UnidentifiedImageError

def get_event_name():
    """ Prompts the user to enter the event from which images will be displayed.
    """
    event = input("Of which event would you like to generate an album?\n") # improvement : displaying the list of events in DD
    
    while event not in os.listdir(os.environ["IMAGES_PATH"]):
        print("Sorry, the event was not found.")
        event = input("Try another event name or press q to interrupt:\n") 
        if event.lower() == 'q':
            return
    return event

def load_images():
    """ Loads images from a given list of image filenames
    """
    event = get_event_name()
    path_to_event_folder = os.path.join(os.environ["IMAGES_PATH"], event) 
    
    images_list = os.listdir(path_to_event_folder)
    all_images = []
    
    # Load images from file in a list
    for image in images_list:
        
        # Handle the case where the file is not an image (has to be changed using the df image_DB)
        try:
            loaded_img = Image.open(os.path.join(path_to_event_folder, image))
            all_images.append(loaded_img)
        except UnidentifiedImageError:
            pass
    
    return all_images

def update_view(self):
    """ Updates image display from the current position in the image stack.
    """
    
    # Get current image
    cur_image = self.image_stack()
    
    # Handle the case where no stack was stored
    if cur_image is None:
        return
        
    # Plot new image
    else:
        plt.close()
        plt.imshow(cur_image)
        plt.axis('off')
        plt.show()

        
def display():

    # Load images to display
    images = load_images()

    # Personalise the toolbar by adding the stack of images and a viewing method
    image_stack = cbk.Stack()
    image_stack._elements = images
    image_stack._pos = 0
    NavigationToolbar2.image_stack = image_stack

    NavigationToolbar2.update_view = update_view

    # Override the toolbar functions 'back' and 'forward' to move in the image stack
    back = NavigationToolbar2.back

    def my_back(self, *args, **kwargs):
        self.image_stack.back()
        self.update_view()
        back(self, *args, **kwargs)
    
    NavigationToolbar2.back = my_back


    forward = NavigationToolbar2.forward

    def my_forward(self, *args, **kwargs):
        self.image_stack.forward()
        self.update_view()
        back(self, *args, **kwargs)
    
    NavigationToolbar2.forward = my_forward

    # Start the image display
    plt.imshow(images[0])
    plt.show()

"""
# grid -> how to decide how many images are in a row -> adjust and ask user if panorama or diaporama
def display_images_rows(loaded_images):
    f, ax = plt.subplots(1, len(loaded_images)) 
    for idx, img in enumerate(loaded_images):
        ax[idx].imshow(img)
        ax[idx].axis('off') # same for y axis.
    plt.show()
    return
"""
