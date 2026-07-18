import math
import random
from dataclasses import dataclass

from textual.app import App, ComposeResult
from textual.containers import Grid, VerticalScroll
from textual.widgets import Button

from menual import menual_config


@dataclass(frozen=True)
class MenuLayout:
    columns: int
    rows: int
    window_width: int
    window_height: int


BUTTON_COLOR_CLASSES = (
    "color-rose",
    "color-coral",
    "color-amber",
    "color-lime",
    "color-mint",
    "color-teal",
    "color-sky",
    "color-blue",
    "color-violet",
    "color-fuchsia",
    "color-grape",
    "color-ruby",
    "color-apricot",
    "color-leaf",
    "color-aqua",
    "color-indigo",
)

MIN_WINDOW_WIDTH = 380
MIN_WINDOW_HEIGHT = 190
BUTTON_WIDTH = 166
BUTTON_HEIGHT = 82
BUTTON_ROW_HEIGHT = 5
WINDOW_HORIZONTAL_PADDING = 76
WINDOW_VERTICAL_PADDING = 70


def get_menu_layout(shortcut_count: int) -> MenuLayout:
    item_count = max(1, shortcut_count)
    rows = max(1, math.floor(math.sqrt(item_count)))
    columns = math.ceil(item_count / rows)

    return MenuLayout(
        columns=columns,
        rows=rows,
        window_width=max(
            MIN_WINDOW_WIDTH, columns * BUTTON_WIDTH + WINDOW_HORIZONTAL_PADDING
        ),
        window_height=max(
            MIN_WINDOW_HEIGHT, rows * BUTTON_HEIGHT + WINDOW_VERTICAL_PADDING
        ),
    )


class Menual(App):
    BINDINGS = [("escape", "quit_launcher", "Quitter")]

    CSS: str = """
    Screen {
        background: #fffaf4;
        color: #243142;
    }

    #launcher-scroll {
        width: 100%;
        height: 100%;
    }

    #launcher {
        width: 100%;
        height: auto;
        padding: 1 2;
        grid-gutter-horizontal: 2;
        grid-gutter-vertical: 1;
    }

    Button.launcher-button {
        width: 100%;
        height: 100%;
        min-width: 8;
        color: #18202d;
        text-style: bold;
        content-align: center middle;
    }

    Button.launcher-button:hover {
        text-style: bold;
    }

    Button.color-rose {
        background: #ff9bb5;
    }

    Button.color-rose:hover {
        background: #ffc0cf;
    }

    Button.color-coral {
        background: #ffb199;
    }

    Button.color-coral:hover {
        background: #ffd1c3;
    }

    Button.color-amber {
        background: #ffd166;
    }

    Button.color-amber:hover {
        background: #ffe29b;
    }

    Button.color-lime {
        background: #c8ec67;
    }

    Button.color-lime:hover {
        background: #def697;
    }

    Button.color-mint {
        background: #8ee9c3;
    }

    Button.color-mint:hover {
        background: #b8f4db;
    }

    Button.color-teal {
        background: #78dce8;
    }

    Button.color-teal:hover {
        background: #a8edf4;
    }

    Button.color-sky {
        background: #8ecaff;
    }

    Button.color-sky:hover {
        background: #bbddff;
    }

    Button.color-blue {
        background: #a6b8ff;
    }

    Button.color-blue:hover {
        background: #cbd4ff;
    }

    Button.color-violet {
        background: #c9a7ff;
    }

    Button.color-violet:hover {
        background: #ddc8ff;
    }

    Button.color-fuchsia {
        background: #f0a6ff;
    }

    Button.color-fuchsia:hover {
        background: #f7cbff;
    }

    Button.color-grape {
        background: #d8b4fe;
    }

    Button.color-grape:hover {
        background: #ead6ff;
    }

    Button.color-ruby {
        background: #ff8a9a;
    }

    Button.color-ruby:hover {
        background: #ffb6c0;
    }

    Button.color-apricot {
        background: #ffc078;
    }

    Button.color-apricot:hover {
        background: #ffdab0;
    }

    Button.color-leaf {
        background: #9ee493;
    }

    Button.color-leaf:hover {
        background: #c1f0bb;
    }

    Button.color-aqua {
        background: #8be3ff;
    }

    Button.color-aqua:hover {
        background: #bdefff;
    }

    Button.color-indigo {
        background: #b7b2ff;
    }

    Button.color-indigo:hover {
        background: #d2cfff;
    }
    """

    def __init__(self):
        super().__init__()
        self.config: list[menual_config.LineConfig] = menual_config.get_config()
        self.layout_config: MenuLayout = get_menu_layout(len(self.config))
        self.button_color_classes: list[str] = list(BUTTON_COLOR_CLASSES)
        random.shuffle(self.button_color_classes)

    def compose(self) -> ComposeResult:
        with VerticalScroll(id="launcher-scroll"):
            with Grid(id="launcher") as launcher:
                launcher.styles.grid_size_columns = self.layout_config.columns
                launcher.styles.grid_size_rows = self.layout_config.rows
                launcher.styles.grid_columns = " ".join(
                    ["1fr"] * self.layout_config.columns
                )
                launcher.styles.grid_rows = " ".join(
                    [str(BUTTON_ROW_HEIGHT)] * self.layout_config.rows
                )

                for index, line_config in enumerate(self.config):
                    color_class = self.button_color_classes[
                        index % len(self.button_color_classes)
                    ]
                    button = Button(
                        line_config.label,
                        classes=f"launcher-button {color_class}",
                        compact=True,
                    )
                    setattr(button, "config", line_config)
                    yield button

    def on_button_pressed(self, event: Button.Pressed):
        line_config = getattr(event.button, "config", None)
        if line_config is None:
            return

        self.exit(line_config)

    def on_app_blur(self) -> None:
        self.exit()

    def action_quit_launcher(self) -> None:
        self.exit()
