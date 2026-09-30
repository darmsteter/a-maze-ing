from pydantic import BaseModel, Field, model_validator
from enum import StrEnum


class ConfigKey(StrEnum):
    """Keys used to identify configuration parameters."""

    WIDTH = "WIDTH"
    HEIGHT = "HEIGHT"
    ENTRY = "ENTRY"
    EXIT = "EXIT"
    OUTPUT_FILE = "OUTPUT_FILE"
    PERFECT = "PERFECT"
    SEED = "SEED"
    ALGORITHM = "ALGORITHM"

    @classmethod
    def required(cls) -> tuple["ConfigKey", ...]:
        """Return configuration keys that are required.

        Returns:
            A tuple containing all required configuration keys.
        """
        return (
            cls.WIDTH,
            cls.HEIGHT,
            cls.ENTRY,
            cls.EXIT,
            cls.OUTPUT_FILE,
        )


class PerfectEnum(StrEnum):
    """Possible values for the maze perfection setting."""

    TRUE = "True"
    FALSE = "False"


class AlgorithmEnum(StrEnum):
    """Algorithms available for maze generation."""

    DFS = "dfs"
    PRIM = "prim"


class Pair(BaseModel):
    """Represent a pair of non-negative integer coordinates."""

    x: int = Field(..., ge=0)
    y: int = Field(..., ge=0)


class Config(BaseModel):
    """Store and validate maze generation configuration."""

    width: int = Field(..., gt=0)
    height: int = Field(..., gt=0)
    entry: Pair = Field(...)
    exit: Pair = Field(...)
    output_file: str = Field(..., min_length=1)
    perfect: PerfectEnum = Field(...)
    seed: int | None = Field(None, ge=0)
    algorithm: AlgorithmEnum | None = AlgorithmEnum.DFS

    @model_validator(mode="after")
    def config_check(self) -> "Config":
        """Validate configuration values that depend on multiple fields.

        Returns:
            The validated configuration instance.

        Raises:
            ValueError: If the entry or exit is outside the maze,
                if they are the same point, if the maze is larger
                than 72x32, or if the output file is not a TXT file.
        """

        if self.entry.x >= self.width or self.entry.y >= self.height:
            raise ValueError("Entry should be inside maze.")
        if self.exit.x >= self.width or self.exit.y >= self.height:
            raise ValueError("Exit should be inside maze.")
        if self.entry.x == self.exit.x and self.entry.y == self.exit.y:
            raise ValueError("Exit and enty shouldn't be same point.")
        if self.width > 72 or self.height > 32:
            raise ValueError(
                f"Maze dimensions too big ({self.width}x{self.height}). "
                "Maximum allowed is 72x32!"
            )
        if not self.output_file.endswith(".txt"):
            raise ValueError("Output file should end with .txt")
        return self
