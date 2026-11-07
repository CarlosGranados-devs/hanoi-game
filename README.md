# Hanoi Game

Juego de la Torre de Hanói desarrollado en Python.

El objetivo es mover todos los discos de la torre 1 a la torre 3, respetando dos reglas:

1. Solo se mueve un disco a la vez (el de la cima de una torre).
2. Nunca se puede colocar un disco grande sobre uno más pequeño.

## Estado del proyecto

| Versión | Descripción | Estado |
|---------|-------------|--------|
| v0.1 | Estructura base del repositorio | Completada |
| v1 | MVP en consola | Completada |
| v2 | Interfaz gráfica sencilla | Pendiente |
| v3 | Producto ideal (features avanzadas) | Pendiente |

## Requisitos

- Python 3.10 o superior
- Sin dependencias externas en v1 (la GUI de v2 usará una librería gráfica, aún por decidir)

## Cómo ejecutar

```bash
git clone https://github.com/YonaZakkart/hanoi-game.git
cd hanoi-game
python main.py
```

## Cómo jugar

1. Elige el número de discos (de 1 a 10).
2. En cada turno escribe origen y destino, por ejemplo `1 3` (también valen `1,3`, `1-3`, `1>3` o `13`).
3. Las torres se numeran del 1 al 3.
4. Escribe `q` o `salir` (o Ctrl+C) para abandonar.

Al ganar se muestran tus movimientos y el mínimo teórico (2ⁿ − 1). Si igualas el mínimo, ¡partida perfecta!

```
    |         |         |
   ===        |         |
  =====       |         |
--------- --------- ---------
 Torre 1   Torre 2   Torre 3
```

## Estructura del proyecto

```
hanoi/
├── main.py              # Punto de entrada y bucle principal
├── models/tower.py      # Clase Tower (pila de discos)
├── game/hanoi_game.py   # Clase HanoiGame (reglas y estado)
├── ui/console_ui.py     # Interfaz de consola
├── ui/gui.py            # Placeholder de la GUI (v2)
├── utils/helpers.py     # Validación de entradas y cálculos
├── assets/              # Recursos (v2/v3)
└── docs/tecnico.md      # Documentación técnica
```

La lógica del juego es independiente de la interfaz, así que la GUI de v2 reutilizará `HanoiGame` sin cambios.

Más detalle en [docs/tecnico.md](docs/tecnico.md).

## Flujo de trabajo

Cada punto se desarrolla en su propia rama (`feature/vX-puntoN-...`) y se integra a `main` mediante Pull Request.