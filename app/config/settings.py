import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    env: str
    debug: bool

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            env=os.getenv("APP_ENV", "dev"),
            debug=os.getenv("DEBUG", "0") == "1",
        )
