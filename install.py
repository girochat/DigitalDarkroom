import os
import shutil
import argparse
import pandas as pd

# Display welcoming message
print("Thanks for downloading 'Digital Darkroom'! This is the procedure to install the program on your computer.")

# Retrieve command line argument 
parser = argparse.ArgumentParser(
    prog='InstallDigitalDarkroom',
    description='Install Digital Darkroom program on local computer')

# Get path where to install program folder
parser.add_argument('-p', '--path') 
args = parser.parse_args()

# Check if a path was given in argument
if args.path is None:

    # Ask the user where to store the program
    input_path = input("Where do you want to store 'Digital Darkroom'?\n"
                       "Please provide the full path from your home directory. Example : Documents/MyProgramFolder\n"
                       "(Q for Quit installation)\n")
else:
    input_path = args.path   
    
# Install program folder at given location and initialise program environment
installed = False
while not installed:

    if input_path == "Q":
        break

    # Remove first backslash if present
    if input_path.startswith("/") or input_path.startswith("\\"):
        input_path = input_path[1:]

    # Build absolute path to destination program folder
    try:
        path_to_program = os.path.join(os.environ['HOME'], input_path)
    except KeyError:
        path_to_program = os.path.join(os.environ['HOMEPATH'], input_path)
    
    # Copy source program folder if path exists 
    if os.path.exists(path_to_program):
        path_to_program = os.path.join(path_to_program, "DigitalDarkroom")
        
        # Handle the case when the program folder already exists
        try:
            current_directory = os.path.dirname(os.path.realpath(__file__))
            shutil.copytree(os.path.join(current_directory, "DigitalDarkroom"), path_to_program) 

        except FileExistsError:
            
            # Ask user if the installation should be forced
            forcing = input("Error! 'Digital Darkroom' seems to already exist at that location...\n"
                            "The installation will be aborted unless you enter 'force' to force the installation " 
                            "and erase the existing version of Digital Darkroom. " 
                            f"Beware! {path_to_program} will be erased.\n").lower()
            
            if forcing == "force":
                shutil.rmtree(path_to_program)
                
            else: 
                print("Installation aborted. Digital Darkroom already exists at that location.")
                break
                
        installed = True  

        # Create images folder
        path_to_images = os.path.join(path_to_program, "Images")
        if not os.path.exists(path_to_images):
            os.makedirs(path_to_images)

        # Create DataFrame to store image metadata
        image_DB = pd.DataFrame(columns = ['Filename', 'Event', 'Format', 'Width', 'Height', 'Megapixels', 'Channels', 'Mode', 'Timestamp', 'Creation', 
                                                'Date_Time', 'Date']).set_index("Filename")
        
        # Save DataFrame in pickle file
        image_DB.to_pickle(os.path.join(path_to_program, "image_DB.pkl"))
                
        print(f"Installation completed! 'Digital Darkroom' has been successfully installed at '{path_to_program}'.")

    else:
        input_path = input("The folder could not be found...\n"
                            "Please enter a valid path from your home directory (Q for Quit installation):\n")



