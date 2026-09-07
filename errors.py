class ConfigurationException(Exception):
	def __init__(self, message: str="Unknown configuration erro") -> None:
		self.message = message
		super().__init__(self.message)

	def __str__(self) -> str:
		return f"{self.message}"