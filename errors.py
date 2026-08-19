class ConfigurationException(Exception):
	def __init__(self, message="Unknown configuration erro"):
		self.message = message
		super().__init__(self.message)

	def __str__(self):
		return f"{self.message}"