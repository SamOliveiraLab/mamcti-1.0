# UI Imports
from tkinter import *
from tkinter import ttk
from functools import partial

# Application imports
from pycromanager import Core
import os
import time
from PIL import Image, ImageTk

# ML/AI imports
import cv2
import numpy as np

def HelloWorld():
    print("Hello World!");

# Micro_Env Object
###########################################################
class Micro_Env:
    def __init__(self):
        # Initialize paremeters
        self.core = None;
        self.xy_coord_init = core.get_xy_stage_position(); # Note this is a Java double Object
        self.coord_init_array = [core.get_xy_stage_position().get_x(), core.get_xy_stage_position().get_y()];
        self.curr_coord_array = [core.get_xy_stage_position().get_x(), core.get_xy_stage_position().get_y()];

        # Other
        self.display_image = None;

    ########## Setters ##########
    def set_core(self, core):
        self.core = core;

    ########### Positional Functions ###########
    # Stage to the right 50 pixels away
    def move_right_50(self, file_path, filename, ttk):
        # If a image existed, delete it
        if (os.path.isfile("./" + filename)):
            self.delete_snapshot(file_path, filename);

        print("Old Coordinates:", self.curr_coord_array);
        self.curr_coord_array[0] = self.curr_coord_array[0] - 50;
        self.core.set_xy_position(self.curr_coord_array[0], self.curr_coord_array[1]);

        # Image Display Protocol
        self.capture_and_save(file_path);
        self.set_display_image(file_path, filename, ttk);

        print("New Coordinates:", self.curr_coord_array);

    # Stage to the left 50 pixels away 
    def move_left_50(self):
        print("Old Coordinates:", self.curr_coord_array);
        self.curr_coord_array[0] = self.curr_coord_array[0] + 50;
        self.core.set_xy_position(self.curr_coord_array[0], self.curr_coord_array[1]);
        print("New Coordinates:", self.curr_coord_array);

    # Reset Stage to hard coded value
    def reset_pos(self):
        self.curr_coord_array[0] = -10192.900000000001;
        self.curr_coord_array[1] = -2561.8;
        self.core.set_xy_position(-10192.900000000001, -2561.8); # Reset Position
        print("New Coordinates:", self.curr_coord_array);

    ########### Image Capture Functions ###########
    def capture_and_save(self, file_path):
        default_file_path = os.getcwd();

        time.sleep(0.5);
        self.core.set_exposure(300);
        self.core.snap_image();
        tagged_image = self.core.get_tagged_image();
        pixels = np.reshape(tagged_image.pix, newshape=[tagged_image.tags['Height'], tagged_image.tags['Width']]);

        os.chdir(file_path);
        cv2.imwrite("temp.png", pixels);
        os.chdir(default_file_path);
        print("Save operation complete");

    def delete_snapshot(self, file_path, filename):
        default_file_path = os.getcwd();

        os.chdir(file_path);
        if (os.path.isfile("./" + filename)):
            os.remove("./" + filename);
            print("Deletion operation complete");
        else:
            print("File Error: File does not exist!");
        os.chdir(default_file_path);

    ########### Image Display Functions ###########
    def set_display_image(self, file_path, filename, ttk):
        default_file_path = os.getcwd();
        Middle_Frame = ttk.Frame(root, width=500, height=500).grid(column=2, row=0);

        os.chdir(file_path);
        if (os.path.isfile("./" + filename)):
            cv_img = cv2.cvtColor(cv2.imread("./" + filename), cv2.COLOR_BGR2RGB) # Use OpenCV read as its more robust
            im_pil = Image.fromarray(cv_img).resize((500, 500)); # OpenCV format --> PIL format
            img = ImageTk.PhotoImage(im_pil);
            self.display_image = img; # Do this to prevent garbage collection;

            ttk.Label(Middle_Frame, image=img).grid(column=2, row=0);
            print("File Found");
        else:
            # Display Text if Empty
            ttk.Label(Middle_Frame, text="[No Microscope Image]").grid(column=2, row=0);
        os.chdir(default_file_path);


###########################################################

# Temporary functions (will move this to seperate python module...)
def microscope_env_init():
    return [[1, 0, 0, 0, 0], [1, 0, 0, 0, 0], [1, 0, 0, 0, 0]]; # Assume the init is good init...

def microscope_pos_init():
    return ["^", "_", "_", "_", "_"]; # Assume the init is good init...

def move_chamber_right(core, current_coordinates):
    current_coordinates[0] = current_coordinates[0] - 125;
    core.set_xy_position(current_coordinates[0], current_coordinates[1] - 7);
    return current_coordinates;

def move_chamber_left(core, current_coordinates):
    current_coordinates[0] = current_coordinates[0] - 125;
    core.set_xy_position(current_coordinates[0], current_coordinates[1] - 7);
    return current_coordinates;

def exit_protocol(root):
    print("Exited Program!");
    root.destroy;

###########################################################

root = Tk()
root.title("MAMCTI-2.0")

# Bootstrap phase
core = Core(); # Pycro Core initialization

display_file_path = "D:\CIDAR\Sam\Zach\mamcti\mamcti-2.0\mamcti\staging_env";

# Create Micro ENV Object
obj = Micro_Env();
obj.set_core(core); # Assign pycro core to Micro_env object
print();
print("######################## Initialization Parameters ########################")
print("File Display Path set at: ", display_file_path);
print("Core initialized and set at: ", obj.core);
print("Current [X,Y] coordinates: ", obj.curr_coord_array);
print("Init [X,Y] coordinates: ", obj.coord_init_array);
print();
print("######################## Console Output ########################");

# TKINT SCRIPT
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Left side Command Column
ttk.Label(mainframe, text="Commands").grid(column=1, row=0);
ttk.Button(mainframe, text="Display Microscopic Array", command=HelloWorld).grid(column=1, row=1, sticky=W)
ttk.Button(mainframe, text="Move Microscope to the RIGHT by 50 pixels", command=partial(obj.move_right_50, display_file_path, "temp.png", ttk)).grid(column=1, row=2, sticky=W)
ttk.Button(mainframe, text="Move Microscope to the LEFT by 50 pixels", command=obj.move_left_50).grid(column=1, row=3, sticky=W)
ttk.Button(mainframe, text="Take a Snapshot", command=partial(obj.capture_and_save, display_file_path)).grid(column=1, row=4, sticky=W)
ttk.Button(mainframe, text="Delete the Snapshot", command=partial(obj.delete_snapshot, display_file_path, "temp.png")).grid(column=1, row=5, sticky=W)
ttk.Button(mainframe, text="Reset Position", command=obj.reset_pos).grid(column=1, row=6, sticky=W)
ttk.Button(mainframe, text="Exit", command=root.quit).grid(column=1, row=7, sticky=W)

# Setting Middle Section
obj.set_display_image(display_file_path, "temp.png", ttk);

# Some padding and polish
for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)


root.mainloop()