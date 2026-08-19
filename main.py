from config import read_config_file, Config

if __name__ == "__main__":
	try:
		config = read_config_file()
		print(config)
	except (FileNotFoundError, PermissionError, ValueError) as e:
		print(e)
