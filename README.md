# Digital Darkroom

:musical_note: Welcome! Willkommen! Bienvenue! Benvenuti! :musical_note: :v:  
Are you a fan of travel? Do you have lots of friends and/or a big family who never miss an opportunity to gather? Or perhaps you have an artistic fiber and enjoy photography during your spare time. You must then probably know the nightmare of handling tons of photos after each event. This project aims at designing a fast and easy-to-use photo album where images can be uploaded, classified according to events, date or places and edited. No specific knowledge is required to use and install the program, it is aimed at any user that has access to a computer (-> [how to install the program](#installation)).

## Installation
##### Current release : DigitalDarkroom-1.0

To install Digital Darkroom, you must first download the [latest release](https://github.com/AdvPyS23/DigitalDarkroom/releases) from our repository on GitHub. This can be done either:  
 
* In the command line interface (Bash terminal):  
Open a terminal window and enter:   
`wget https://github.com/AdvPyS23/DigitalDarkroom/releases`  
__Note__ : this will download the folder in your current working directory. To specify another directory use:  
`wget -P path_to_local_directory https://github.com/AdvPyS23/DigitalDarkroom/releases `  
where `path_to_local_directory` should be replaced with the path to the desired directory.
    
* Directly on GitHub:  
Simply go to our GitHub repository [DigitalDarkroom](https://github.com/AdvPyS23/DigitalDarkroom) and check the latest release on the right of the page to download the folder as a zip file.   
<!--![Download release folder from GitHub](/download_release.png "Download release_x.x")-->  

Before installing the program, you might want to check [the requirements](/requirements.txt) that are needed both to install and run the program. 

Once the release folder has been downloaded and unzipped and [the requirements](/requirements.txt) are met, open a terminal window and go to the directory containing the release folder. You can use the following command to retrieve the path of the release folder:  
`find ~ -name DigitalDarkroom-1.0 2>/dev/null`  
Then, enter:  
`cd path_to_release/DigitalDarkroom-1.0`  
`python3 install.py`  
__Note__: you can directly specify where you would like to store the program DigitalDarkroom using the option --path or -p (provide the absolute path from your home directory).  
`python3 install.py -p path`

##### Upcoming release : :construction:
See the [ROADMAP](/ROADMAP.md) for expected version release.

## Usage

The installation went on smoothly?!? Great! Then, it is time to launch the program. To run DigitalDarkroom, enter the following command in the terminal:  
`python3 run_program.py`  
__Note__: the command must be run from the DigitalDarkroom directory. If you do not remember where you have installed the program, type the following command in the terminal:
`find ~ -name « DigitalDarkroom » 2>/dev/null`  
It will output the path to the program in the terminal. You can then go to the program directory using:  
`cd <path_to_program>`  


## Support

We will do our best to provide a stable and foolproof program version at any time (see [Installation](#installation)). However, as programs do always contain unexpected bugs, if you encounter some problems or need to contact us, you can reach us by email at : michaela.amherd@students.unibe.ch or giliane.rochat@students.unibe.ch  
You can also open a [new issue](https://github.com/AdvPyS23/DigitalDarkroom/issues) to share your thoughts or explain your issue.

## Roadmap

In the [ROADMAP](/ROADMAP.md) you can find the major milestones of the project with their corresponding deadlines.

## Contributing 
We welcome anyone willing to contribute to the project :pray:   
See [CONTRIBUTING](/CONTRIBUTING.md) for information on how to contribute.   
See also the [open issues](https://github.com/AdvPyS23/DigitalDarkroom/issues) that are still of dire need of contributors. :bell:

## Acknowledgements

Authors : Michaela Amherd and Giliane Rochat. 

## Licence

All code published in this repository is under the GPLv3 licence.  
All contents published in this repository are under the Creative Commons licence CC-BY-SA.
