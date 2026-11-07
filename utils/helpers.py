"""Funciones auxiliares para la Torre de Hanói (versión consola).

Aquí vive la validación de entradas y cálculos sueltos. No contiene reglas
del juego (eso es de game/hanoi_game.py) ni dibuja el tablero (ui/console_ui.py).
"""

from game.hanoi_game import HanoiGame
from ui.console_ui import show_error

YES_WORDS = ("s", "si", "sí", "y", "yes")
NO_WORDS = ("n", "no")


def calculate_min_moves(num_disks):
    """Mínimo teórico de movimientos para resolver n discos: 2^n - 1."""
    return 2 ** num_disks - 1


def parse_num_disks(text):
    """Convierte el texto del usuario a número de discos.

    Devuelve el entero si es válido. Lanza ValueError con un mensaje
    claro si no es un número o está fuera del rango permitido.
    """
    text = text.strip()
    if not text.lstrip("-").isdigit():
        raise ValueError("Escribe un número entero, por ejemplo: 3")
    value = int(text)
    if value < HanoiGame.MIN_DISKS or value > HanoiGame.MAX_DISKS:
        raise ValueError(
            f"El número de discos debe estar entre "
            f"{HanoiGame.MIN_DISKS} y {HanoiGame.MAX_DISKS}."
        )
    return value


def ask_num_disks():
    """Pide el número de discos hasta recibir uno válido.

    Devuelve el entero, o None si el usuario quiere salir
    ('q', 'salir', Ctrl+C o Ctrl+D).
    """
    prompt = (
        f"¿Con cuántos discos quieres jugar "
        f"({HanoiGame.MIN_DISKS}-{HanoiGame.MAX_DISKS})? "
    )
    while True:
        try:
            text = input(prompt).strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            return None
        if text in ("q", "salir"):
            return None
        try:
            return parse_num_disks(text)
        except ValueError as error:
            show_error(str(error))


def ask_yes_no(question):
    """Hace una pregunta de sí/no. Devuelve True/False (False si cierra la entrada)."""
    while True:
        try:
            text = input(f"{question} (s/n): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            return False
        if text in YES_WORDS:
            return True
        if text in NO_WORDS:
            return False
        show_error("Responde 's' o 'n'.")