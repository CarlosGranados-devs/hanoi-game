"""Punto de entrada de la Torre de Hanói (versión consola, v1)."""

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
    """Bucle de una partida. Devuelve True si ganó, False si salió."""
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


def main():
    show_message("=== TORRE DE HANÓI ===")
    while True:
        num_disks = ask_num_disks()
        if num_disks is None:
            break

        play(HanoiGame(num_disks))

        if not ask_yes_no("¿Jugar otra vez?"):
            break

    show_message("¡Hasta pronto!")


if __name__ == "__main__":
    main()