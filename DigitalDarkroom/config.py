""" This module contains the global variables of the program.
"""
import os
import pandas as pd

# Define constant global variables for program paths
program_path = os.path.dirname(os.path.realpath(__file__))
images_path = os.path.join(program_path, "Images")

# Get the image database from pickle file
DB = pd.read_pickle(os.path.join(program_path, "image_DB.pkl"))