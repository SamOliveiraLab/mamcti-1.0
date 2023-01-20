print("Program initiated. Starting Microscope Scripts...");
print();

# Imports
from pycromanager import Core
import os

# Temporary functions (will move this to seperate python module...)
def reset_pos(core, current_coordinates):
	current_coordinates[0] = -6001.6;
	current_coordinates[1] = -4008.6000000000004;
	core.set_xy_position(-6001.6, -4008.6000000000004); # Reset Position
	return current_coordinates

def move_right_50(core, current_coordinates):
	current_coordinates[0] = current_coordinates[0] - 50;
	core.set_xy_position(current_coordinates[0], current_coordinates[1]);
	return current_coordinates;

def move_left_50(core, current_coordinates):
	current_coordinates[0] = current_coordinates[0] + 50;
	core.set_xy_position(current_coordinates[0], current_coordinates[1]);
	return current_coordinates;

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


def main():
	core = Core(); # Pycro Core initialization

	# Get Microscope init parameters
	xy_coord_init = core.get_xy_stage_position(); # Note this is a Java double Object
	coord_init_array = [xy_coord_init.get_x(), xy_coord_init.get_y()];
	curr_coord_array = coord_init_array;

	# Note good starting POS for depth 60 Monolayer cell is [-6001.6, -4008.6000000000004] 
	print("Initial [X,Y] coordinates: ",str(coord_init_array));

	# Get Microsope ENV
	micro_env_arr = microscope_env_init();
	micro_pos_arr = microscope_pos_init();
	micro_pointer = 0;

	# Exit condition
	exit = False;

	# Main Loop
	while (not exit):
		os.system("cls");
		print();
		print("=======================================");
		print("Program Menu: ");
		print("1: Display Micrscope Array");
		print("2: Move Microscope to the RIGHT by 50 pixels");
		print("3: Move Microscope to the LEFT by 50 pixels");
		print("4: Move to next Monolayer Chamber RIGHT");
		print("5: Move to next Monolayer Chamber LEFT");
		print("8: Reset to init position");
		print("9: Exit");
		print("=======================================");

		user_input = int(input("[USER_CMD]>>: "));
		print();

		print("================= OUTPUT =================")
		match user_input:
			case 1: 
				print("Microscope Env:");
				print("0 ~ Signifies unvisited monolayer chamber.");
				print("1 ~ Signifies visited monolayer chamber.");
				print("-1 ~ Signifies error in the environment.");
				print();
				print(micro_env_arr);
				print();
				exit = input("[Press enter to continue]");
			case 2:
				curr_coord_array = move_right_50(core, curr_coord_array);
				print("New Coordinates: ", curr_coord_array);
				print();
				exit = input("[Press enter to continue]");
			case 3:
				curr_coord_array = move_left_50(core, curr_coord_array);
				print("New Coordinates: ", curr_coord_array);
				print();
				exit = input("[Press enter to continue]");
			case 4:
				if (micro_pointer <= len(micro_env_arr) - 1): 
					micro_pos_arr[micro_pointer] = "_";
					micro_pointer = micro_pointer + 1;
					micro_pos_arr[micro_pointer] = "^";
					curr_coord_array = move_chamber_right(core, curr_coord_array);
					print("New Coordinates: ", curr_coord_array);
					print("Pointer POS: ", str(micro_pointer));
					print("Current Position is signified by: ^");
					print(micro_pos_arr);
					print();
					exit = input("[Press enter to continue]");
				else:
					print("Invalid Position: Reached the Rightmost field!");
					print();
					exit = input("[Press enter to continue]");
			case 8:
				curr_coord_array = reset_pos(core, curr_coord_array);
				print("New Coordinates (resetted): ", curr_coord_array);
				print();
				exit = input("[Press enter to continue]");
			case 9:
				exit = True;
				print("Exited!");

main();

print("Operation done.");
