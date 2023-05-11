# Structural improvements 


What we have done to improve the structure of our code by:

## Decomposition
- We decomposed our code by creating different modules for individual tasks that are coherent with the main file to run the program
- Within each module further code decomposition was achieved through the use of multiple functions and one class (number might increase in the future) 

Why we did it: 
Decomposing our project made it easier to work independently on subproblems, which reduced the number of merge conflicts and the stress resulting from those :sweat_smile:. Furthermore, code decomposition helped to structure the code and keep it better organized.

## Abstraction
- We have used functions to abstract specific actions of the program such as displaying images or extracting metadata. We did not change much the structure of our code per se as we had already tried to follow that approach for the first release and we have continued for the second release. The naming of the functions is hopefully clear enough so that there is no need to read all the function code and details to understand what it does and returns. 
- We have added a class that is the representation of an event during which specific images have been taken. It allows to englobe in one object the « event » entity as the user knows it (name, description) and as the os system knows it (path in file system).
- We have added docstrings in the module image_upload and display_images (others will follow) to provide an overview of what the module is and what functions it contains. Similarly, we have added docstrings to diverse functions (hopefully in the end all of them) so that it is clear what the function does and what are its parameters without having each time to read the code of the function.

Why we did it: in case new developers or maybe the user him/herself would have to look at the source code, it would not require to understand what every piece of code does. It is also helpful for ourselves when working collaboratively on the program. The abstraction into diverse functions (=program actions) and diverse classes (=program entities) and the provided documentation should be easy to understand.
