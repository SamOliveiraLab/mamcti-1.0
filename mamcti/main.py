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

# Python Imports
from phase_stretch_transform import *

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
        self.display_image_left = None;
        self.display_image_right = None;
        self.default_file_path = os.getcwd();

    ########## Setters ##########
    def set_core(self, core):
        self.core = core;

    ########### Positional Functions ###########
    # Stage to the right 50 pixels away
    def move_right_50(self, frame, file_path, filename, ttk):
        # If a image existed, delete it
        if (os.path.isfile("./" + filename)):
            self.delete_snapshot(file_path, filename);

        print("Old Coordinates:", self.curr_coord_array);
        self.curr_coord_array[0] = self.curr_coord_array[0] - 50;
        self.core.set_xy_position(self.curr_coord_array[0], self.curr_coord_array[1]);

        # Move the micrscope and take a snapshot
        self.capture_and_save(file_path);
        self.set_display_image(frame, 2, file_path, filename, ttk);

        # Conduct Image processing (PST);
        results = PST_Output(file_path, filename);
        print("orig type:", type(results[0]));
        print("orig:", results[0]);
        print("orig type:", type(results[1]));
        print("edge:", results[1]);
        print("orig type:", type(results[2]));
        print("overlay:", results[2]);
        os.chdir(file_path);

        im = Image.fromarray(results[1]);
        im.save("edge.png");

        os.chdir(self.default_file_path);


        print("New Coordinates:", self.curr_coord_array);

    # Stage to the left 50 pixels away 
    def move_left_50(self, frame, file_path, filename, ttk):
        print("Old Coordinates:", self.curr_coord_array);
        self.curr_coord_array[0] = self.curr_coord_array[0] + 50;
        self.core.set_xy_position(self.curr_coord_array[0], self.curr_coord_array[1]);

        # Image Display Protocol
        self.capture_and_save(file_path);
        self.set_display_image(frame, 2, file_path, filename, ttk);

        print("New Coordinates:", self.curr_coord_array);

    # Reset Stage to hard coded value
    def reset_pos(self, frame, file_path, filename, ttk):
        self.curr_coord_array[0] = -11943.1;
        self.curr_coord_array[1] = -2523;
        self.core.set_xy_position(-11943.1, -2523); # Reset Position

        # Image Display Protocol
        self.capture_and_save(file_path);
        self.set_display_image(frame, 2, file_path, filename, ttk);

        print("New Coordinates:", self.curr_coord_array);

    ########### Image Capture Functions ###########
    def capture_and_save(self, file_path):
        time.sleep(0.5);
        self.core.set_exposure(300);
        self.core.snap_image();
        tagged_image = self.core.get_tagged_image();
        pixels = np.reshape(tagged_image.pix, newshape=[tagged_image.tags['Height'], tagged_image.tags['Width']]);

        os.chdir(file_path);
        cv2.imwrite("temp.png", pixels);
        os.chdir(self.default_file_path);
        print("Save operation complete");

    def delete_snapshot(self, file_path, filename):
        os.chdir(file_path);
        if (os.path.isfile("./" + filename)):
            os.remove("./" + filename);
            print("Deletion operation complete");
            os.chdir(self.default_file_path);
            return True
        else:
            print("File Error: File does not exist!");
            os.chdir(self.default_file_path);
        return False
        

    ########### Image Display Functions ###########
    def set_display_image(self, frame, col, file_path, filename, ttk):
        os.chdir(file_path);
        if (os.path.isfile("./" + filename)):
            cv_img = cv2.cvtColor(cv2.imread("./" + filename), cv2.COLOR_BGR2RGB) # Use OpenCV read as its more robust
            im_pil = Image.fromarray(cv_img).resize((500, 500)); # OpenCV format --> PIL format
            img = ImageTk.PhotoImage(im_pil);
            if (col == 2):
                self.display_image_left = img; # Do this to prevent garbage collection;
            elif(col == 3):
                self.display_image_right = img; # Do this to prevent garbage collection;

            ttk.Label(frame, image=img).grid(column=col, row=0);
            print("Display File Found");
        else:
            # Display Text if Empty
            ttk.Label(frame, text="[No Microscope Image]").grid(column=col, row=0);
        os.chdir(self.default_file_path);

    def clear_display_image_cache(self, frame, file_path, filename):
        if (self.delete_snapshot(file_path, filename)):
            print("Cache is cleared!");
        else:
            print("Cache is empty");
        # Display Text if Empty
        ttk.Label(frame, text="[No Microscope Image]").grid(column=col, row=0);

###########################################################

root = Tk()
root.title("MAMCTI-2.0")

# Bootstrap phase
core = Core(); # Pycro Core initialization

display_file_path = "D:\CIDAR\Sam\Zach\mamcti\mamcti-2.0\mamcti\staging_env";

# Create Micro ENV Object
obj = Micro_Env();
obj.set_core(core); # Assign pycro core to Micro_env object

# Print initializer (for some style!)
print();
print("███╗░░░███╗░█████╗░███╗░░░███╗░█████╗░████████╗██╗░░░░░░░░███╗░░░░░░█████╗░\n" 
    + "████╗░████║██╔══██╗████╗░████║██╔══██╗╚══██╔══╝██║░░░░░░░████║░░░░░██╔══██╗\n"
    + "██╔████╔██║███████║██╔████╔██║██║░░╚═╝░░░██║░░░██║█████╗██╔██║░░░░░██║░░██║\n"
    + "██║╚██╔╝██║██╔══██║██║╚██╔╝██║██║░░██╗░░░██║░░░██║╚════╝╚═╝██║░░░░░██║░░██║\n"
    + "██║░╚═╝░██║██║░░██║██║░╚═╝░██║╚█████╔╝░░░██║░░░██║░░░░░░███████╗██╗╚█████╔╝\n"
    + "╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░░░░╚═╝░╚════╝░░░░╚═╝░░░╚═╝░░░░░░╚══════╝╚═╝░╚════╝░\n");
print();
print("######################## Initialization Parameters ########################")
print("______________________________________________________________________________________________________");
print("File Display Path set at     | ", display_file_path);
print("Core initialized and set at  | ", obj.core);
print("Current [X,Y] coordinates    | ", obj.curr_coord_array);
print("Init [X,Y] coordinates       | ", obj.coord_init_array);
print();
print("######### PY Modules #########");
print("____________________________________");
check_module_phase_stretch_transform();
print();
print("######################## Console/Print Output ########################");
print("______________________________________________________________________________________________________");

# TKINT SCRIPT
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# TKINT FRAMES
Middle_Frame_Left = ttk.Frame(root, width=500, height=500).grid(column=2, row=0);
Middle_Frame_Right = ttk.Frame(root, width=500, height=500).grid(column=3, row=0);

# Left side Command Column
ttk.Label(mainframe, text="Commands").grid(column=1, row=0);
ttk.Button(mainframe, text="Display Microscopic Array", command=HelloWorld).grid(column=1, row=1, sticky=W)
ttk.Button(mainframe, text="Move Microscope to the RIGHT by 50 pixels", command=partial(obj.move_right_50, Middle_Frame_Left, display_file_path, "temp.png", ttk)).grid(column=1, row=2, sticky=W)
ttk.Button(mainframe, text="Move Microscope to the LEFT by 50 pixels", command=partial(obj.move_left_50, Middle_Frame_Left, display_file_path, "temp.png", ttk)).grid(column=1, row=3, sticky=W)
ttk.Button(mainframe, text="Take a Snapshot", command=partial(obj.capture_and_save, display_file_path)).grid(column=1, row=4, sticky=W)
ttk.Button(mainframe, text="Clear Image Cache", command=partial(obj.clear_display_image_cache, Middle_Frame_Left, display_file_path, "temp.png")).grid(column=1, row=5, sticky=W)
ttk.Button(mainframe, text="Reset Position", command=partial(obj.reset_pos, Middle_Frame_Left, display_file_path, "temp.png", ttk)).grid(column=1, row=6, sticky=W)
ttk.Button(mainframe, text="Exit", command=root.quit).grid(column=1, row=7, sticky=W)

# Setting Middle Section
obj.set_display_image(Middle_Frame_Left, 2, display_file_path, "temp.png", ttk);
obj.set_display_image(Middle_Frame_Right, 3, display_file_path, "edge.png", ttk);

# Some padding and polish
for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5);


root.mainloop();