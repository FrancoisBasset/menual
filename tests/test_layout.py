import pytest

from menual.menual import (
    MIN_WINDOW_HEIGHT,
    MIN_WINDOW_WIDTH,
    get_menu_layout,
)


@pytest.mark.parametrize(
    ("shortcut_count", "expected_grid"),
    [
        (0, (1, 1)),
        (1, (1, 1)),
        (4, (2, 2)),
        (6, (3, 2)),
        (9, (3, 3)),
        (16, (4, 4)),
    ],
)
def test_layout_dimensions_for_common_shortcut_counts(
    shortcut_count: int,
    expected_grid: tuple[int, int],
) -> None:
    layout = get_menu_layout(shortcut_count)

    assert (layout.columns, layout.rows) == expected_grid


@pytest.mark.parametrize("shortcut_count", range(50))
def test_layout_always_has_enough_cells(shortcut_count: int) -> None:
    layout = get_menu_layout(shortcut_count)

    assert layout.columns * layout.rows >= max(1, shortcut_count)


def test_layout_respects_minimum_window_size() -> None:
    layout = get_menu_layout(0)

    assert layout.window_width >= MIN_WINDOW_WIDTH
    assert layout.window_height >= MIN_WINDOW_HEIGHT
