from pydantic import BaseModel, Field, model_validator
from enum import StrEnum


class PerfectEnum(StrEnum):
    TRUE = 'True'
    FALSE = 'False'


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
    algorithm: str | None = "dfs"

    @model_validator(mode='after')
    def config_check(self) -> 'Config':
        if self.entry.x >= self.width or self.entry.y >= self.height:
            raise ValueError("Entry should be inside maze.")
        if self.exit.x >= self.width or self.exit.y >= self.height:
            raise ValueError("Exit should be inside maze.")
        if self.entry.x == self.exit.x and self.entry.y == self.exit.y:
            raise ValueError("Exit and enty shouldn't be same point.")
        if not self.output_file.endswith('.txt'):
            raise ValueError("Output file should end with .txt")
        if self.algorithm.lower() not in ["dfs", "prim"]:
            raise ValueError(f"Invalid algorithm {self.algorithm}. Choose either 'dfs' or 'prim'.")
        return self
