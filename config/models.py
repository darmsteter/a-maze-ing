from pydantic import BaseModel, Field, model_validator
from enum import StrEnum


class ConfigKey(StrEnum):
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
        return (
            cls.WIDTH,
            cls.HEIGHT,
            cls.ENTRY,
            cls.EXIT,
            cls.OUTPUT_FILE,
            cls.PERFECT
        )


class PerfectEnum(StrEnum):
    TRUE = 'True'
    FALSE = 'False'


class AlgorithmEnum(StrEnum):
    DFS = 'dfs'
    PRIM = 'prim'


class Pair(BaseModel):
    x: int = Field(..., ge=0)
    y: int = Field(..., ge=0)


class Config(BaseModel):
    width: int = Field(..., gt=0)
    height: int = Field(..., gt=0)
    entry: Pair = Field(...)
    exit: Pair = Field(...)
    output_file: str = Field(..., min_length=1)
    perfect: PerfectEnum = Field(...)
    seed: int | None = Field(None)
    algorithm: AlgorithmEnum | None = AlgorithmEnum.DFS

    @model_validator(mode='after')
    def config_check(self) -> 'Config':
        if self.entry.x >= self.width or self.entry.y >= self.height:
            raise ValueError("Entry should be inside maze.")
        if self.exit.x >= self.width or self.exit.y >= self.height:
            raise ValueError("Exit should be inside maze.")
        if self.entry.x == self.exit.x and self.entry.y == self.exit.y:
            raise ValueError("Exit and enty shouldn't be same point.")
        if self.width < 5 or self.height < 5:
            raise ValueError(
                f"Maze dimensions too small ({self.width}x{self.height}).\n"
                "Minimum allowed is 5x5!"
            )
        if self.width > 25 or self.height > 25:
            raise ValueError(
                f"Maze dimensions too large ({self.width}x{self.height}).\n"
                "Maximum allowed is 25x25!"
            )
        if not self.output_file.endswith('.txt'):
            raise ValueError("Output file should end with .txt")
        return self
