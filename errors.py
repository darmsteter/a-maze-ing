class ConfigurationException(Exception):
    def __init__(self, message: str = "Unknown configuration error") -> None:
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"{self.message}"


class ActionInterrupted(Exception):
    def __init__(self, key_code: str):
        self.key_code = key_code


class InvalidConfigError(Exception):
    pass
