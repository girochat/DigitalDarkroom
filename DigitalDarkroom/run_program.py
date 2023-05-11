import os
import image_upload as imload 
import display_images as implay
import edit_images as imedit

# Define constant global variables for program paths
os.environ["PROGRAM_PATH"] = os.path.dirname(os.path.realpath(__file__))  
os.environ["IMAGES_PATH"] = os.path.join(os.environ["PROGRAM_PATH"], "Images")
try:
    os.environ["HOME_PATH"] = os.environ['HOME']
except KeyError:
    os.environ["HOME_PATH"] = os.environ['HOMEPATH']

# Display welcoming message (with figlet if module pyfiglet installed)
try:
    from pyfiglet import Figlet 
    font = Figlet(font='thin')
    print(font.renderText('Welcome to Digital Darkroom!!!\n'))
    figlet = True
    
except ModuleNotFoundError:
    print('Welcome to Digital Darkroom!!!\n\n')

# Start the program
quit = False
while not quit:
    
    # Display (and launch) program activities to the user
    print("What do you want to do?")
    next_task = input("- Upload new images in Digital Darkroom => type 'U' or 'upload'\n"
                     "- View your images stored in Digital Darkroom => type 'V' or 'view'\n"
                     "- Edit an image stored in one of your event folders => type 'E' or 'edit'\n"
                     "- Quit the program => type 'Q' or 'quit'\n").lower()
    print()
    
    if next_task in ["u", "upload"]:
        try:
            imload.upload_images()
        except SystemExit:
            pass
        
    elif next_task in ["v", "view"]:
        try:
            implay.display()
        except SystemExit:
            pass

    elif next_task in ["e", "edit"]:
        try:
            imedit.edit()
        except SystemExit:
            pass
        
    elif next_task in ["q", "quit"]:
        quit = True
        
        if figlet:
            font = Figlet(font='thin')
            print(font.renderText('Bye, Bye!\n'))
        else:
            print("Bye, Bye!\n\n")

    else:
        print("Error! Please enter one of the valid options as displayed...")
        
  