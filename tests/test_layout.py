import unittest

from menual.menual import (
    MIN_WINDOW_HEIGHT,
    MIN_WINDOW_WIDTH,
    get_menu_layout,
)


class MenuLayoutTests(unittest.TestCase):
    def test_layout_dimensions_for_common_shortcut_counts(self) -> None:
        cases = {
            0: (1, 1),
            1: (1, 1),
            4: (2, 2),
            6: (3, 2),
            9: (3, 3),
            16: (4, 4),
        }

        for shortcut_count, expected_grid in cases.items():
            with self.subTest(shortcut_count=shortcut_count):
                layout = get_menu_layout(shortcut_count)
                self.assertEqual((layout.columns, layout.rows), expected_grid)

    def test_layout_always_has_enough_cells(self) -> None:
        for shortcut_count in range(0, 50):
            with self.subTest(shortcut_count=shortcut_count):
                layout = get_menu_layout(shortcut_count)
                self.assertGreaterEqual(
                    layout.columns * layout.rows,
                    max(1, shortcut_count),
                )

    def test_layout_respects_minimum_window_size(self) -> None:
        layout = get_menu_layout(0)

        self.assertGreaterEqual(layout.window_width, MIN_WINDOW_WIDTH)
        self.assertGreaterEqual(layout.window_height, MIN_WINDOW_HEIGHT)
