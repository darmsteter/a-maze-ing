class ConfigurationException(Exception):
    """Represent an error in the maze configuration."""

    def __init__(self, message: str = "Unknown configuration error") -> None:
        """Initialize a configuration error.

        Args:
            message: Description of the configuration error.
        """

        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        """Return the configuration error message.

        Returns:
            The error message as a string.
        """

        return f"{self.message}"


class ActionInterrupted(Exception):
    """Represent an interruption caused by a user action."""

    def __init__(self, key_code: str):
        """Initialize an action interruption.

        Args:
            key_code: Keyboard key that caused the interruption.
        """

        self.key_code = key_code


class ConfigurationFileError(Exception):
    """Represent an error while accessing the configuration file."""

    def __init__(self, message: str = "Unknown file error") -> None:
        """Initialize a configuration file error.

        Args:
            message: Description of the file-related error.
        """
        
        self.message = message
        super().__init__(self.message)
