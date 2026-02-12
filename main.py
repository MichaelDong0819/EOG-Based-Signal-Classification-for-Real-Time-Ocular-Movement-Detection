print("\nProgram Setup - Starting to Import\n")
print("Main System Modules - Starting to Import")
import os
print("Main System Modules - Finished Importing")
print("Main Custom Modules - Starting to Import")
from interface.interface import Interface
from utils.file_operations import list_videos
print("Main Custom Modules - Finished Importing")
print("\nProgram Setup - Finished Importing\n")

# Note that you must always run the program from the main.py file. This way the python environment can access all modules. 

if __name__ == "__main__":
    video_files = list_videos(os.path.join(os.path.dirname(__file__), 'videos'))
    app = Interface(video_files)
    app.mainloop()