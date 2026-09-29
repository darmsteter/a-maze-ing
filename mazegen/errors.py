class MazeGenerationError(Exception):
	"""Represent an error that occurs during maze generation."""
	
	def __init__(self, message: str = "Unknown configuration error") -> None:
		"""Initialize a maze generation error.

        Args:
            message: Description of the maze generation error.
        """

		self.message = message
		super().__init__(self.message)

	def __str__(self) -> str:
		"""Return the maze generation error message.

        Returns:
            The maze generation error message as a string.
        """

		return f"{self.message}"