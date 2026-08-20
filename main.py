from config import read_config_file, Config
from errors import ConfigurationException

if __name__ == "__main__":
	try:
		config = read_config_file()
		print(config)
	except ConfigurationException as e:
		print(f"Configuration error: {e}")