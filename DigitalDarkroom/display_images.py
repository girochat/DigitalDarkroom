"""
Module to display images from a local folder in DigitalDarkroom.

Functions
---------
get_event   
    
load_images  
    
update_view  
    
stack_back

stack_forward

save_image

preview

display
   
"""
import os
import numpy as np
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
        from_event = input("Would you like to view images of a specific event? (Y/Yes or N/No or Q/Quit) :\n").lower()
        if from_event in ["y", "yes"]:
            event = input("Enter the name of the event:\n")       # improvement : displaying the list of events in images DB?
            while event not in os.listdir(os.environ["IMAGES_PATH"]):
                event = input("Sorry, the event was not found... Try again: (Q for Quit)\n") 
                if event.lower() in ["quit", 'q']:
                    return
            event = os.path.join(os.environ["IMAGES_PATH"], event)
            answer = True
            
        elif from_event in ["n", "no"]:
            answer = True
            event = os.environ["IMAGES_PATH"]
            
        elif from_event in ["q", "quit"]:
            return
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

def update_view(self):
    """ Updates image display from the current position in the image stack. Triggered by the dynamic toolbar.
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
        
def stack_back(self, *args, **kwargs):
    """ Goes backward in the stack of image. Triggered by the dynamic toolbar.
    """
    self.image_stack.back()
    self.update_view()
    #back(self, *args, **kwargs)
        
def stack_forward(self, *args, **kwargs):
    """ Goes forward in the stack of image. Triggered by the dynamic toolbar.
    """
    self.image_stack.forward()
    self.update_view()
    #forward(self, *args, **kwargs)
    
def save_image(edited_image, event_path):
    """ Allows to save an edited image in DigitalDarkroom.
    """
    
    # Ask user for confirmation
    answer = False
    while not answer:
        answer = input("You asked to save the edited image. Would you like to preview the changes"
                        " or directly save the edited image?"
                        " (P for Preview or S for Save or Q for Quit)\n").lower()
        if answer in ["p", "preview"]:
            plt.imshow(image)
            plt.show()
            answer = input("Would you like to save the edited image? (S for Save or Q for Quit)\n").lower()
            
        elif answer in ["s", "save"]:
            image_name = input("Enter the name for your edited image: "
                               "(Please specify the extension, ex: .jpg)\n")
            try:
                edited_image.save(os.path.join(event_path, image_name))
            except ValueError:
                print("Error! The file extension is not valid. Saving aborted.")
                return
            
        elif answer in ["q", "quit"]:
            return
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
        answer = input("Would you like to save the edited image? (S for Save or Q for Quit)\n").lower()
        if answer in ["s", "save"]:
            save_image(edited_image, event_path)
        elif answer in ["q", "quit"]:
            return
        else:
            print("Error! Please enter one of the valid options as displayed...")
            answer = False
            
            
def display():
    """ Displays images in a dynamic interface.
    """
    # Load images to display
    images = load_images()

    # Personalise the toolbar by adding the stack of images and a viewing method
    image_stack = cbk.Stack()
    image_stack._elements = images
    image_stack._pos = 0
    NavigationToolbar2.image_stack = image_stack
    NavigationToolbar2.update_view = update_view

    # Override the toolbar functions 'back' and 'forward' to move in the image stack
    original_back = NavigationToolbar2.back
    NavigationToolbar2.back = stack_back

    original_forward = NavigationToolbar2.forward
    NavigationToolbar2.forward = stack_forward
 

    # Start the image display
    plt.imshow(images[0])
    plt.axis("off")
    plt.show()
    
    # Re-implement default toolbar functions
    NavigationToolbar2.back = original_back
    NavigationToolbar2.forward = original_forward


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
