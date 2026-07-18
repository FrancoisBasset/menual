import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from menual import menual_config
from menual.menual_config import LineConfig


class MenualConfigTests(unittest.TestCase):
    def test_reads_shortcuts_from_config_file(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            config_path = Path(temporary_directory) / ".menual.conf"
            _ = config_path.write_text(
                "Firefox,firefox,1\nSystem monitor,btop,0\n",
                encoding="utf-8",
            )

            with patch.object(menual_config, "get_path", return_value=config_path):
                config = menual_config.get_config()

        self.assertEqual(
            config,
            [
                LineConfig("Firefox", "firefox", True),
                LineConfig("System monitor", "btop", False),
            ],
        )

    def test_creates_missing_config_file(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            config_path = Path(temporary_directory) / ".menual.conf"

            with patch.object(menual_config, "get_path", return_value=config_path):
                config = menual_config.get_config()

            self.assertEqual(config, [])
            self.assertTrue(config_path.is_file())
