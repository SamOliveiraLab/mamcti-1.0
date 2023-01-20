from tkinter import *
from tkinter import ttk
from functools import partial

# Other imports
from pycromanager import Core
import os

def HelloWorld():
    print("Hello World!");

# Micro_Env Object
###########################################################
class Micro_Env:
    def __init__(self):
        # Initialize paremeters
        self.xy_coord_init = core.get_xy_stage_position(); # Note this is a Java double Object
        self.coord_init_array = [core.get_xy_stage_position().get_x(), core.get_xy_stage_position().get_y()];
        self.curr_coord_array = [core.get_xy_stage_position().get_x(), core.get_xy_stage_position().get_y()];

        # Get Microsope ENV
        # self.micro_env_arr = microscope_env_init();
        # self.micro_pos_arr = microscope_pos_init();
        # self.micro_pointer = 0;

    # Stage to the right 50 pixels away
    def move_right_50(self, core):
        print("Old Coordinates:", self.curr_coord_array);
        self.curr_coord_array[0] = self.curr_coord_array[0] - 50;
        core.set_xy_position(self.curr_coord_array[0], self.curr_coord_array[1]);
        print("New Coordinates:", self.curr_coord_array);

    # Stage to the left 50 pixels away 
    def move_left_50(self, core):
        print("Old Coordinates:", self.curr_coord_array);
        self.curr_coord_array[0] = self.curr_coord_array[0] + 50;
        core.set_xy_position(self.curr_coord_array[0], self.curr_coord_array[1]);
        print("New Coordinates:", self.curr_coord_array);

    # Reset Stage to hard coded value
    def reset_pos(self, core):
        self.curr_coord_array[0] = -6001.6;
        self.curr_coord_array[1] = -4008.6000000000004;
        core.set_xy_position(-6001.6, -4008.6000000000004); # Reset Position
        print("New Coordinates:", self.curr_coord_array);
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

# Create Micro ENV Object
obj = Micro_Env();

# TTK SCRIPT
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

ttk.Button(mainframe, text="Display Micrscopic Array", command=HelloWorld).grid(column=1, row=1, sticky=W)
ttk.Button(mainframe, text="Move Microscope to the RIGHT by 50 pixels", command=partial(obj.move_right_50, core)).grid(column=1, row=2, sticky=W)
ttk.Button(mainframe, text="Move Microscope to the LEFT by 50 pixels", command=partial(obj.move_left_50, core)).grid(column=1, row=3, sticky=W)
ttk.Button(mainframe, text="Reset Position", command=partial(obj.reset_pos, core)).grid(column=1, row=4, sticky=W)
ttk.Button(mainframe, text="Exit", command=root.quit).grid(column=1, row=5, sticky=W)

# Some padding and polish
for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

root.mainloop()