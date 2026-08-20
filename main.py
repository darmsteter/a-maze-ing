from config import read_config_file, Config
from errors import ConfigurationException
import sys

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print(
			"Your program must be run with the following command: "
			"python3 a_maze_ing.py file_name.txt"
		)
		exit()
	try:
		config = read_config_file(sys.argv[1])
	except ConfigurationException as e:
		print(f"Configuration error: {e}")
		exit()