from pydantic import ValidationError

from .models import Pair, Config, AlgorithmEnum, ConfigKey, PerfectEnum
from errors import ConfigurationException, ConfigurationFileError


def store_config_value(
    values: dict[ConfigKey, str], key: str, value: str
) -> None:
    """Store a configuration value after validating its key and value.

    Args:
        values: Dictionary containing parsed configuration values.
        key: Configuration key as a string.
        value: Configuration value as a string.

    Raises:
        ConfigurationException: If the key or value is empty, the key is
            unknown, or the key has already been defined.
    """

    if not key:
        raise ConfigurationException(
            "Empty key. " "Expected a key in the format KEY=VALUE."
        )
    if not value:
        raise ConfigurationException(
            "Empty value. " f"Expected a value after '{key}='."
        )
    try:
        config_key = ConfigKey(key)
    except ValueError as e:
        raise ConfigurationException(
            f"Unknown configuration key: {key}"
        ) from e

    if config_key in values:
        raise ConfigurationException(
            f"Duplicate configuration key: {key}. "
            "Each configuration key must appear only once."
        )

    values[config_key] = value


def parse_coordinates(field_name: str, coordinates: str) -> Pair:
    """Parse a coordinate string into a Pair.

    Args:
        field_name: Name of the configuration field being parsed.
        coordinates: Coordinates in the expected ``x,y`` format.

    Returns:
        A Pair containing the parsed x and y coordinates.

    Raises:
        ConfigurationException: If the coordinates do not contain exactly
            two non-empty values or if they are not valid integers.
    """

    split_coordinates = coordinates.split(",")
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
        return Pair(x=int(split_coordinates[0]), y=int(split_coordinates[1]))
    except ValueError:
        raise ConfigurationException(
            f"{field_name} coordinates must be non-negative integers "
            f"in the format x,y; received: '{coordinates}'"
        )


def parse_config_lines(line: str, values: dict[ConfigKey, str]) -> None:
    """Parse a single line from the configuration file.

    Empty lines and comments are ignored. Configuration lines must use
    the ``KEY=VALUE`` format.

    Args:
        line: A line read from the configuration file.
        values: Dictionary containing parsed configuration values.

    Raises:
        ConfigurationException: If the line has an invalid format or
            contains an invalid configuration key or value.
    """

    line = line.strip()
    if not line.startswith("#") and line != "":
        if "=" not in line:
            raise ConfigurationException(
                "Invalid configuration line. "
                "Expected a key in the format KEY=VALUE."
            )
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        store_config_value(values, key, value)


def validate_required_keys(values: dict[ConfigKey, str]) -> None:
    """Check that all required configuration keys are present.

    Args:
        values: Dictionary containing parsed configuration values.

    Raises:
        ConfigurationException: If one or more required configuration
            keys are missing.
    """

    missing_keys: list[str] = [
        key.value for key in ConfigKey.required() if key not in values
    ]
    if missing_keys:
        missing_str = ", ".join(key for key in missing_keys)
        raise ConfigurationException(
            f"Missing required configuration key(s): {missing_str}"
        )


def build_config(values: dict[ConfigKey, str]) -> Config:
    """Build and validate a Config object from parsed values.

    Optional configuration values use their default values when they are
    not present.

    Args:
        values: Dictionary containing parsed configuration values.

    Returns:
        A validated Config instance.

    Raises:
        ConfigurationException: If any configuration value is invalid
            or cannot be converted to the expected type.
    """

    try:
        entry_coordinate = parse_coordinates(
            ConfigKey.ENTRY, values[ConfigKey.ENTRY]
        )
        exit_coordinate = parse_coordinates(
            ConfigKey.EXIT, values[ConfigKey.EXIT]
        )
        config = Config(
            width=int(values[ConfigKey.WIDTH]),
            height=int(values[ConfigKey.HEIGHT]),
            entry=entry_coordinate,
            exit=exit_coordinate,
            output_file=values[ConfigKey.OUTPUT_FILE],
            perfect=PerfectEnum(
                values[ConfigKey.PERFECT]
                if ConfigKey.PERFECT in values
                else PerfectEnum.FALSE
            ),
            seed=(
                int(values[ConfigKey.SEED])
                if ConfigKey.SEED in values
                else None
            ),
            algorithm=(
                AlgorithmEnum(values[ConfigKey.ALGORITHM].lower())
                if ConfigKey.ALGORITHM in values
                else AlgorithmEnum.DFS
            ),
        )
    except ValidationError as e:
        error_dict = e.errors()
        if error_dict[0]["type"] == "value_error":
            error_message = error_dict[0]["msg"].replace("Value error, ", "")
        else:
            error_message = "\n".join(
                [
                    f"Invalid value for field '{error['loc'][0]}':"
                    f" {error['msg']}"
                    f", but received '{error['input']}'."
                    for error in error_dict
                ]
            )
        raise ConfigurationException(error_message)
    except ValueError as e:
        raise ConfigurationException(str(e))
    return config


def read_config_file(file_name: str) -> Config:
    """Read, parse, and validate a maze configuration file.

    Args:
        file_name: Path to the configuration file.

    Returns:
        A validated Config instance created from the file contents.

    Raises:
        ConfigurationFileError: If the configuration file cannot be
            opened or accessed.
        ConfigurationException: If the configuration contains invalid
            data or is missing required keys.
    """

    values: dict[ConfigKey, str] = {}
    try:
        with open(file_name, "r") as config_file:
            for line in config_file:
                parse_config_lines(line, values)
    except (FileNotFoundError, PermissionError, IsADirectoryError) as e:
        raise ConfigurationFileError(str(e)) from e
    validate_required_keys(values)
    return build_config(values)
