# 1. Welcome to the Roadmap!

Never knew how to read a roadmap?? No worry, this one doesn't require a good sense of orientation... :wink:  
Our project is to create a Photo Album Organizer <!-- to be refined -->, a simple tool with image storing, organizing and editing functionality. On this page you'll find all the relevant information you need to get a first impression of the project, what milestones we have set for ourselves, how well on our way we are at achieving them and how you might get involved.


# 2. Willing to participate? 

Here you'll find important documentation about the project. If you have suggestions feel free to [contact us](/README.md/#support).

## Documentation to check out

[README.md](README.md) : this file contains all the general information about the project. If you haven't installed the program yet, this is the way to go.

[Contributor Covenant](https://www.contributor-covenant.org/version/1/4/code-of-conduct/) : please check this code of conduct. It might seem a formality but it is important to us that certain core and universal principles are respected between collaborators. 

[GPLv3 LICENSE](https://www.gnu.org/licenses/gpl-3.0.en.html) :page_facing_up:
[CC LICENSE](https://creativecommons.org/licenses/by-sa/4.0/legalcode) :page_facing_up:

## How can I contribute?

- Report bugs
- Suggest improvements
- Code extensions
- Fix [issues](https://github.com/AdvPyS23/DigitalDarkroom/issues)


# 3. Timeline :hourglass_flowing_sand:

In the following section you'll find a brief overview of our milestones with a rough timeframe, what tasks we are currently working on and what the next steps will be.

<!--Those points should be described:
- Project status goals (feature release, minimum viable project)
- Dates / Events (Presentations, Release, Exams, etc)
- Timeframes (short, medium, long term)-->

## Milestones
<!--
Include for each task:
- What needs to be done
- What does success look like
- Pointers to get started
- Why this task is important – link to your project goals-->



| Tasks | Timeframe |
|-----:|-----------|
|     [Project management](#project-management)| April 27 | 
|     [Image Upload and Organization](#task-1-image-upload-and-organization)| May 4 |
|     [Basic Image Editing](#task-2-basic-image-editing) | May 11 |
|     [Image Metadata and Analysis](#task-3-image-metadata-and-analysis)| May 18 |
|     [Minimum viable project](#minimum-viable-project) | May 25 :construction:|
|     [Presentation](#presentation-of-our-project) | June 1   |


### Project management 
Timeframe: April 27

- define our mission, goals and the scope of the project
- structre the project into milestones and break those further down into smaller tasks

### Task 1: Image Upload and Organization 
Timeframe: May 4
 - Prepare repository on GitHub
     - decide how to structure the repository (main, branches...)
     - agree on how to work collaboratively on same branch
 - Allow users to upload and store images in various formats (e.g., JPEG, PNG).
     - decide how images are stored in dependencies (main folder, folder per event/date?)
     - handle case where images are uploaded via folder or many files
     - upload via CLI ? -> many choices available to the user
     - list necessary dependencies in a file
 - Organize images into event folders.
     - create Image class
     - user can call Images by event but also by dates or locations
     - diaporama or panaroma preview of the images in an event folder

### Task 2: Basic Image Editing 
Timeframe: May 11

- Enable users to perform basic image editing tasks via input to the terminal.
    - ameliorate user interface : dynamic interface
    - select image to be edited directly from panorama or diaporama view
    - choose editing options : adjust brightness/contrast, image enhancement
- Provide a preview of the edited image before saving the changes.
    - ask for confirmation before saving changes
    - provide a preview 
    - allow for duplicate image with edited feature
- Input via terminal 
    - update dependencies file

### Task 3: Image Metadata and Analysis 
Timeframe: May 18

- Allow users to view and edit metadata associated with their images. 
    - allow the user to add geo-data to images or events
    - offer to the user to edit the name and location (all attributes of class Image) of an image and an event folder
    - add option to delete event folders or images


- Provide visualizations and analysis of image metadata.
    - visualise map of image locations
    - plot density maps for the image locations


- Implement Unit tests :white_check_mark:



### Minimum viable project 
Timeframe: May 25
- Virtual environment



### Presentation 
Timeframe: June 1

The day we have all been waiting for - or so :sweat_smile:

Task:
- Stay calm
- Try to articulate and speak loud enough
- Celebrate :clinking_glasses:





