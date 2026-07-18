from pathlib import Path

import pytest

from menual import menual_config
from menual.menual_config import LineConfig


def test_reads_shortcuts_from_config_file(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    config_path = tmp_path / ".menual.conf"
    config_path.write_text(
        "Firefox,firefox,1\nSystem monitor,btop,0\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(menual_config, "get_path", lambda: config_path)

    config = menual_config.get_config()

    assert config == [
        LineConfig("Firefox", "firefox", True),
        LineConfig("System monitor", "btop", False),
    ]


def test_creates_missing_config_file(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    config_path = tmp_path / ".menual.conf"
    monkeypatch.setattr(menual_config, "get_path", lambda: config_path)

    config = menual_config.get_config()

    assert config == []
    assert config_path.is_file()
