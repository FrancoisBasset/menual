import os
import shlex
import shutil
import subprocess
import sys

from menual import menual_config
from menual.menual import Menual, get_menu_layout
from menual.menual_config import LineConfig


MENU_WINDOW_CLASS = "menual"
MENU_WINDOW_TITLE = "Menual"


def clean_env() -> dict[str, str]:
    env = os.environ.copy()
    env.pop("MENUAL_IN_KITTY", None)
    return env


def get_menu_window_size() -> tuple[int, int]:
    layout = get_menu_layout(len(menual_config.get_config()))
    return layout.window_width, layout.window_height


def build_menu_command(
    *,
    window_width: int,
    window_height: int,
    detach: bool = True,
) -> list[str]:
    command = [
        "kitty",
        "--class",
        MENU_WINDOW_CLASS,
        "--title",
        MENU_WINDOW_TITLE,
        "--start-as",
        "normal",
        "--override",
        "remember_window_size=no",
        "--override",
        "remember_window_position=no",
        "--override",
        f"initial_window_width={window_width}",
        "--override",
        f"initial_window_height={window_height}",
    ]

    if detach:
        command.append("--detach")

    command.append(sys.argv[0])
    return command


def launch_centered_menu(
    env: dict[str, str],
    *,
    window_width: int,
    window_height: int,
) -> bool:
    is_hyprland = (
        "Hyprland" in os.environ.get("XDG_CURRENT_DESKTOP", "")
        or "HYPRLAND_INSTANCE_SIGNATURE" in os.environ
    )
    if not is_hyprland or shutil.which("hyprctl") is None:
        return False

    command = [
        "env",
        "MENUAL_IN_KITTY=1",
        *build_menu_command(
            detach=False,
            window_width=window_width,
            window_height=window_height,
        ),
    ]
    rules = f"[float; size {window_width} {window_height}; center 1]"

    try:
        result = subprocess.run(
            ["hyprctl", "dispatch", "exec", f"{rules} {shlex.join(command)}"],
            env=env,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=1,
            check=False,
        )
    except OSError, subprocess.TimeoutExpired:
        return False

    return result.returncode == 0


def launch_menu_in_kitty() -> None:
    env = os.environ.copy()
    env["MENUAL_IN_KITTY"] = "1"
    window_width, window_height = get_menu_window_size()

    if launch_centered_menu(
        env,
        window_width=window_width,
        window_height=window_height,
    ):
        return

    try:
        subprocess.Popen(
            build_menu_command(
                window_width=window_width,
                window_height=window_height,
            ),
            env=env,
        )
    except FileNotFoundError as error:
        raise SystemExit("menual: kitty est introuvable dans le PATH.") from error


def run_menu() -> None:
    app_to_launch: LineConfig | None = Menual().run()

    if app_to_launch is None:
        return

    try:
        command = shlex.split(app_to_launch.command)
    except ValueError as error:
        raise SystemExit(
            f"menual: commande invalide: {app_to_launch.command}"
        ) from error

    if not command:
        return

    if app_to_launch.is_gui:
        subprocess.Popen(
            command,
            env=clean_env(),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
    else:
        kitty_command = ["kitty", "--detach"]
        kitty_command.extend(command)

        subprocess.Popen(kitty_command, env=clean_env())


def main() -> None:
    if os.environ.get("MENUAL_IN_KITTY") != "1":
        launch_menu_in_kitty()
        return

    run_menu()
