# Hanoi Game

Juego de la Torre de Hanói desarrollado en Python, con interfaz gráfica (Pygame) y modo consola.

El objetivo es mover todos los discos de la torre 1 a la torre 3, respetando dos reglas:

1. Solo se mueve un disco a la vez (el de la cima de una torre).
2. Nunca se puede colocar un disco grande sobre uno más pequeño.

## Estado del proyecto

| Versión | Descripción | Estado |
|---------|-------------|--------|
| v0.1 | Estructura base del repositorio | Completada |
| v1 | MVP en consola | Completada |
| v2 | Interfaz gráfica sencilla | Completada |
| v3 | Producto ideal (features avanzadas) | Pendiente |

## Requisitos

- Python 3.10 o superior
- Para la interfaz gráfica: `pygame-ce` (ver `requirements.txt`)
- El modo consola no necesita dependencias externas

## Cómo ejecutar

```bash
git clone https://github.com/YonaZakkart/hanoi-game.git
cd hanoi-game
pip install -r requirements.txt
python main.py              # interfaz gráfica
python main.py --console    # modo consola
```

> No instales `pygame` y `pygame-ce` a la vez: entran en conflicto. Este proyecto usa `pygame-ce`.

## Cómo jugar (interfaz gráfica)

1. En el menú elige el número de discos (1 a 10) con los botones `-` / `+` o las flechas, y pulsa **START** o `Enter`.
2. Haz clic en la torre de origen (se marca en amarillo) y luego en la torre de destino.
3. Un clic en la misma torre, o fuera de las torres, cancela la selección.
4. Los movimientos inválidos muestran un mensaje en rojo durante unos segundos.
5. Arriba a la izquierda ves el mínimo teórico (2ⁿ − 1) y abajo a la derecha tus movimientos.

| Control | Acción |
|---------|--------|
| Clic izquierdo | Seleccionar origen y destino |
| `R` o botón RETRY | Reiniciar la partida |
| `Esc` en partida | Volver al menú |
| `Esc` en el menú | Salir |
| Cerrar la ventana | Salir |

## Cómo jugar (consola)

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
├── main.py              # Punto de entrada (GUI por defecto, --console para consola)
├── requirements.txt     # Dependencias (pygame-ce)
├── models/tower.py      # Clase Tower (pila de discos)
├── game/hanoi_game.py   # Clase HanoiGame (reglas y estado)
├── ui/console_ui.py     # Interfaz de consola
├── ui/gui.py            # Interfaz gráfica con Pygame
├── utils/helpers.py     # Validación de entradas y cálculos
├── assets/              # Imágenes de la GUI
└── docs/tecnico.md      # Documentación técnica
```

La lógica del juego es independiente de la interfaz: la consola y la GUI usan el mismo `HanoiGame` sin cambios.

Más detalle en [docs/tecnico.md](docs/tecnico.md).

## Flujo de trabajo

Cada punto se desarrolla en su propia rama (`feature/vX-puntoN-...`) y se integra a `main` mediante Pull Request.