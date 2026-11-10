"""Punto de entrada de la Torre de Hanói.

Por defecto abre la interfaz gráfica (v2). Con --console usa la consola (v1).
"""

import argparse
import sys

from game.hanoi_game import HanoiGame
from ui.console_ui import (
    ask_move,
    render_towers,
    show_error,
    show_message,
    show_victory,
)
from utils.helpers import ask_num_disks, ask_yes_no


def play(game):
    """Bucle de una partida en consola. Devuelve True si ganó, False si salió."""
    while not game.is_finished():
        render_towers(game.get_state(), game.num_disks)
        show_message(
            f"Movimientos: {game.get_moves()} | Mínimo: {game.get_min_moves()}"
        )

        move = ask_move()
        if move is None:
            return False

        origin, destination = move
        try:
            game.move(origin, destination)
        except ValueError as error:
            show_error(str(error))

    render_towers(game.get_state(), game.num_disks)
    show_victory(game.get_moves(), game.get_min_moves())
    return True


def run_console():
    """Flujo completo en consola (v1): pide discos, juega y repite."""
    show_message("=== TORRE DE HANÓI ===")
    while True:
        num_disks = ask_num_disks()
        if num_disks is None:
            break

        play(HanoiGame(num_disks))

        if not ask_yes_no("¿Jugar otra vez?"):
            break

    show_message("¡Hasta pronto!")


def run_gui():
    """Abre la GUI (v2). Devuelve el código de salida del programa."""
    # Import diferido: así la consola funciona aunque pygame no esté instalado.
    try:
        from ui.gui import HanoiGUI
    except ModuleNotFoundError as error:
        if error.name != "pygame":
            raise
        print(
            "No se encontró pygame. Instálalo con:\n"
            "    pip install -r requirements.txt\n"
            "O juega en consola con:\n"
            "    python main.py --console",
            file=sys.stderr,
        )
        return 1

    HanoiGUI().run()  # arranca en el menú de selección de discos
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description="Torre de Hanói")
    parser.add_argument(
        "--console",
        action="store_true",
        help="jugar en la consola en lugar de la interfaz gráfica",
    )
    args = parser.parse_args(argv)

    if args.console:
        run_console()
        return 0
    return run_gui()


if __name__ == "__main__":
    sys.exit(main())