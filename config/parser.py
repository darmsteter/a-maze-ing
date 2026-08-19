from pydantic import ValidationError
from .keys import ConfigKey
from .models import Pair, Config

def store_config_value(values: dict[ConfigKey, str], key, value):
	try: 
		config_key = ConfigKey(key)
	except ValueError as e:
		raise ValueError(f"Unknown configuration key: {key}") from e
	
	if config_key in values:
		raise ValueError(f"Duplicate configuration key: {key}")
	
	values[config_key] = value

def parse_coordinates(coordinates: str) -> Pair:
	splited_coordinates = coordinates.split(',')
	if len(splited_coordinates) != 2: 
		raise ValueError("It should be two coordinates!")
	return Pair(
			x=splited_coordinates[0],
			y=splited_coordinates[1]
		)

def parse_config_lines(line: str, values: dict[str, str]) -> None:
	line = line.strip()
	if not line.startswith('#') and line != "":
		key, value = line.split('=', 1)
		key = key.strip()
		value = value.strip()
		store_config_value(values, key, value)

def build_config(values: dict[ConfigKey, str]) -> Config:
	try:
		entry = parse_coordinates(values[ConfigKey.ENTRY])
		exit = parse_coordinates(values[ConfigKey.EXIT])
		config = Config(
			width=values[ConfigKey.WIDTH.value],
			height=values[ConfigKey.HEIGHT.value],
			entry=entry,
			exit=exit,
			output_file=values[ConfigKey.OUTPUT_FILE.value],
			perfect=values[ConfigKey.PERFECT.value]
		)
	except (ValueError, ValidationError) as e:
		print(e)
		return
	return(config)
	
def read_config_file() -> Config:
	values: dict[ConfigKey, str] = {}
	try:
		with open("config.txt", "r") as config_file:
			for line in config_file:
				parse_config_lines(line, values)
		return build_config(values)
	except (FileNotFoundError, PermissionError, ValueError) as e:
		raise ValueError(e)
