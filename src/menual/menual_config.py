from dataclasses import dataclass
from pathlib import Path


@dataclass
class LineConfig:
    label: str
    command: str
    is_gui: bool


def get_path() -> Path:
    return Path(str(Path.home()) + "/.menual.conf")


def get_config() -> list[LineConfig]:
    path: Path = get_path()

    config: list[LineConfig] = []

    if path.exists():
        for line in path.open().readlines():
            line = line.removesuffix("\n")
            config.append(
                LineConfig(
                    label=line.split(",")[0],
                    command=line.split(",")[1],
                    is_gui=(line.split(",")[2] == "1"),
                )
            )
    else:
        path.touch()

    return config
