from pydantic import ValidationError
from .keys import ConfigKey
from .models import Pair, Config
from errors import ConfigurationException


def store_config_value(values: dict[ConfigKey, str], key, value):
    if not key:
        raise ConfigurationException(
            "Empty key. "
            "Expected a key in the format KEY=VALUE."
        )
    if not value:
        raise ConfigurationException(
            "Empty value. "
            f"Expected a value after '{key}='."
        )
    try:
        config_key = ConfigKey(key)
    except ValueError:
        raise ConfigurationException(f"Unknown configuration key: {key}")

    if config_key in values:
        raise ConfigurationException(
            f"Duplicate configuration key: {key}. "
            "Each configuration key must appear only once."
            )

    values[config_key] = value


def parse_coordinates(field_name: str, coordinates: str) -> Pair:
    splited_coordinates = coordinates.split(',')
    if len(splited_coordinates) != 2:
        raise ConfigurationException(
            f"{field_name} must contain exactly two coordinates "
            f"in the format x,y; received: '{coordinates}'"
        )
    if not splited_coordinates[0] or not splited_coordinates[1]:
        raise ConfigurationException(
            f"{field_name} must contain two non-empty coordinates "
            f"in the format x,y; received: '{coordinates}'"
        )
    try:
        return Pair(
            x=splited_coordinates[0],
            y=splited_coordinates[1]
        )
    except ValueError as e:
        raise ConfigurationException(
            f"{field_name} coordinates must be non-negative integers "
            f"in the format x,y; received: '{coordinates}'"
        )


def parse_config_lines(line: str, values: dict[ConfigKey, str]) -> None:
    line = line.strip()
    if not line.startswith('#') and line != "":
        key, value = line.split('=', 1)
        key = key.strip()
        value = value.strip()
        store_config_value(values, key, value)


def validate_required_keys(values: dict[ConfigKey, str]) -> None:
    missed_keys: list[str] = [
        key.value for key in ConfigKey
        if key not in values and key not in [ConfigKey.SEED, ConfigKey.ALGORITHM]
    ]
    if missed_keys:
        raise ConfigurationException(
            "Missing required configuration key(s): "
            f"{", ".join(key for key in missed_keys)}"
        )


def build_config(values: dict[ConfigKey, str]) -> Config:
    try:
        entry = parse_coordinates(ConfigKey.ENTRY, values[ConfigKey.ENTRY])
        exit = parse_coordinates(ConfigKey.EXIT, values[ConfigKey.EXIT])
        config = Config(
            width=values[ConfigKey.WIDTH.value],
            height=values[ConfigKey.HEIGHT.value],
            entry=entry,
            exit=exit,
            output_file=values[ConfigKey.OUTPUT_FILE.value],
            perfect=values[ConfigKey.PERFECT.value],
            seed=values[ConfigKey.SEED.value] if ConfigKey.SEED in values else None,
            algorithm=values[ConfigKey.ALGORITHM.value] if ConfigKey.ALGORITHM in values else "dfs"
        )
    except (ValueError, ValidationError) as e:
        error_dict = e.errors()
        if error_dict[0]['type'] == 'value_error':
            error_message = error_dict[0]['msg'].replace("Value error, ", '')
        else:
            error_message = '\n'.join([
                f"Invalid value for field '{error['loc'][0]}':"
                f" {error['msg']}"
                f", but received '{error['input']}'."
                for error in error_dict
            ])
        raise ConfigurationException(error_message)
    return config


def read_config_file(file_name: str) -> Config:
    values: dict[ConfigKey, str] = {}
    try:
        with open(file_name, "r") as config_file:
            for line in config_file:
                parse_config_lines(line, values)
    except (FileNotFoundError, PermissionError, IsADirectoryError) as e:
        raise ConfigurationException(e)
    try:
        validate_required_keys(values)
        return build_config(values)
    except ConfigurationException as e:
        raise ConfigurationException(e)
