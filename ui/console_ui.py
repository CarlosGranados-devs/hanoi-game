"""Interfaz de consola para la Torre de Hanói.

Responsabilidad: SOLO mostrar información y leer lo que escribe el usuario.
No contiene reglas del juego (eso vive en game/hanoi_game.py).

Convención de torres:
- Hacia el usuario se muestran como 1, 2 y 3.
- Hacia el resto del código se devuelven como índices 0, 1 y 2,
- que es lo que espera HanoiGame.move(origen, destino).
"""

import re

NUM_TOWERS = 3
POLE_CHAR = "|"
DISK_CHAR = "="
QUIT_WORDS = ("q", "salir")


def render_towers(towers, num_disks=None):
    """Dibuja las 3 torres en consola.

    towers: lista de listas, de base a cima (lo que devuelve game.get_state()).
    num_disks: opcional; si no se da, se deduce del disco más grande.
    """
    if num_disks is None:
        num_disks = max((max(t) for t in towers if t), default=1)

    # Ancho de cada columna: el disco más grande (2n+1) más un margen.
    width = 2 * num_disks + 1 + 4

    def cell(disk):
        # disk == 0 significa "no hay disco": solo se ve el palo.
        if disk == 0:
            return POLE_CHAR.center(width)
        return (DISK_CHAR * (2 * disk + 1)).center(width)

    lines = [" ".join(cell(0) for _ in towers)]  # punta de los palos
    for level in range(num_disks - 1, -1, -1):  # de arriba hacia abajo
        row = []
        for tower in towers:
            disk = tower[level] if level < len(tower) else 0
            row.append(cell(disk))
        lines.append(" ".join(row))

    lines.append(" ".join("-" * width for _ in towers))
    lines.append(" ".join(f"Torre {i + 1}".center(width) for i in range(len(towers))))

    print()
    print("\n".join(lines))
    print()


def ask_move():
    """Pide origen y destino al usuario.

    Devuelve (origen, destino) con índices base 0, o None si el usuario
    quiere salir (escribe 'q' o 'salir', o cierra la entrada con Ctrl+C/Ctrl+D).
    Repite la pregunta hasta que el formato sea válido. Que el movimiento
    sea legal según las reglas lo decide HanoiGame, no esta función.
    """
    while True:
        try:
            text = input("Mover (origen destino, ej: 1 3; 'q' para salir): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            return None

        if text in QUIT_WORDS:
            return None

        # Acepta "1 3", "1,3", "1-3", "1>3" y "13".
        parts = re.findall(r"\d", text) if re.fullmatch(r"\d{2}", text) else re.split(r"[\s,\-]+|>", text)
        parts = [p for p in parts if p != ""]

        if len(parts) != 2 or not all(p.isdigit() for p in parts):
            show_error("Escribe dos números, por ejemplo: 1 3")
            continue

        origin, destination = int(parts[0]), int(parts[1])
        if not (1 <= origin <= NUM_TOWERS and 1 <= destination <= NUM_TOWERS):
            show_error(f"Las torres van de 1 a {NUM_TOWERS}.")
            continue

        return origin - 1, destination - 1


def show_message(message):
    """Muestra un mensaje informativo."""
    print(message)


def show_error(message):
    """Muestra un mensaje de error con un prefijo visible."""
    print(f"[!] {message}")


def show_victory(moves, min_moves):
    """Muestra la pantalla de victoria con los movimientos usados y el mínimo."""
    print()
    print("=" * 40)
    print("   ¡FELICIDADES, GANASTE!")
    print("=" * 40)
    print(f"Movimientos realizados: {moves}")
    print(f"Mínimo posible:         {min_moves}")
    if moves == min_moves:
        print("¡Partida perfecta, lo resolviste en el mínimo de movimientos!")
    else:
        print(f"Te pasaste por {moves - min_moves} movimientos del mínimo.")
    print()