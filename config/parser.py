from pydantic import ValidationError

from .models import Pair, Config, AlgorithmEnum, ConfigKey
from errors import ConfigurationException


def store_config_value(values: dict[ConfigKey, str], key: str, value: str) -> None:
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
    except ValueError as e:
        raise ConfigurationException(f"Unknown configuration key: {key}") from e

    if config_key in values:
        raise ConfigurationException(
            f"Duplicate configuration key: {key}. "
            "Each configuration key must appear only once."
            )

    values[config_key] = value


def parse_coordinates(field_name: str, coordinates: str) -> Pair:
    split_coordinates = coordinates.split(',')
    if len(split_coordinates) != 2:
        raise ConfigurationException(
            f"{field_name} must contain exactly two coordinates "
            f"in the format x,y; received: '{coordinates}'"
        )
    if not split_coordinates[0] or not split_coordinates[1]:
        raise ConfigurationException(
            f"{field_name} must contain two non-empty coordinates "
            f"in the format x,y; received: '{coordinates}'"
        )
    try:
        return Pair(
            x=split_coordinates[0],
            y=split_coordinates[1]
        )
    except ValueError as e:
        raise ConfigurationException(
            f"{field_name} coordinates must be non-negative integers "
            f"in the format x,y; received: '{coordinates}'"
        )


def parse_config_lines(line: str, values: dict[ConfigKey, str]) -> None:
    line = line.strip()
    if not line.startswith('#') and line != "":
        if '=' not in line:
            raise ConfigurationException(
                "Invalid configuration line. "
                "Expected a key in the format KEY=VALUE."
            ) 
        key, value = line.split('=', 1)
        key = key.strip()
        value = value.strip()
        store_config_value(values, key, value)


def validate_required_keys(values: dict[ConfigKey, str]) -> None:
    missing_keys: list[str] = [
        key.value for key in ConfigKey.required()
        if key not in values
    ]
    if missing_keys:
        raise ConfigurationException(
            "Missing required configuration key(s): "
            f"{", ".join(key for key in missing_keys)}"
        )


def build_config(values: dict[ConfigKey, str]) -> Config:
    try:
        entry_coordinate = parse_coordinates(ConfigKey.ENTRY, values[ConfigKey.ENTRY])
        exit_coordinate = parse_coordinates(ConfigKey.EXIT, values[ConfigKey.EXIT])
        config = Config(
            width=values[ConfigKey.WIDTH],
            height=values[ConfigKey.HEIGHT],
            entry=entry_coordinate,
            exit=exit_coordinate,
            output_file=values[ConfigKey.OUTPUT_FILE],
            perfect=values[ConfigKey.PERFECT],
            seed=(
                values[ConfigKey.SEED]
                if ConfigKey.SEED in values
                else None),
            algorithm=(
                values[ConfigKey.ALGORITHM].lower()
                if ConfigKey.ALGORITHM in values
                else AlgorithmEnum.DFS
                )
        )
    except ValueError as e:
        raise ConfigurationException(str(e)) from e
    except ValidationError as e:
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
        raise ConfigurationException(str(e)) from e
    validate_required_keys(values)
    return build_config(values)