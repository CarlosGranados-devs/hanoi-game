# Documentación Técnica

Resumen de las estructuras y funciones principales del MVP (v1, consola).

## Arquitectura

Tres capas con responsabilidades separadas:

```
main.py ──► ui/console_ui.py   (mostrar y leer)
   │   └──► utils/helpers.py   (validar entradas)
   └──────► game/hanoi_game.py (reglas y estado) ──► models/tower.py (pila)
```

- **models**: estructura de datos.
- **game**: reglas del juego, sin `print` ni `input`.
- **ui**: solo muestra información y lee la entrada; no conoce las reglas.
- **main / utils**: integran todo y validan formato de entradas.

Esta separación permite reemplazar la consola por una GUI (v2) sin tocar `game` ni `models`.

## models/tower.py — `Tower`

Pila (LIFO) de enteros; cada entero es el tamaño de un disco. La base está en el índice 0 y la cima al final.

| Método | Descripción |
|--------|-------------|
| `push(disk)` | Apila un disco. `ValueError` si es mayor que el de la cima. |
| `pop()` | Quita y devuelve el disco de la cima. `IndexError` si está vacía. |
| `peek()` | Devuelve la cima sin quitarla. `IndexError` si está vacía. |
| `is_empty()` | `True` si no hay discos. |
| `size()` | Cantidad de discos. |
| `get_disks()` | Copia de la lista de discos (base → cima). |

## game/hanoi_game.py — `HanoiGame`

Constantes: `NUM_TOWERS = 3`, `MIN_DISKS = 1`, `MAX_DISKS = 10`.

`HanoiGame(num_disks)` valida que sea un entero entre 1 y 10 (`ValueError` si no) y coloca todos los discos en la torre 0, con el más grande abajo.

| Método | Descripción |
|--------|-------------|
| `move(from_tower, to_tower)` | Mueve el disco de la cima. Devuelve el disco movido y suma 1 al contador. Lanza `ValueError` si la torre es inválida, origen = destino, el origen está vacío o se pone un disco grande sobre uno pequeño. |
| `is_valid_move(from_tower, to_tower)` | `True`/`False` sin modificar el estado ni lanzar excepciones. |
| `is_finished()` | `True` cuando todos los discos están en la torre 3 (índice 2). |
| `get_state()` | Lista de 3 listas con los discos de cada torre (base → cima). |
| `get_moves()` | Movimientos realizados. |
| `get_min_moves()` | Mínimo teórico: 2ⁿ − 1. |
| `reset()` | Reinicia torres y contador. |

Alias: `is_won()` = `is_finished()`, `get_towers()` = `get_state()`.

Las torres se indexan 0-2 internamente.

## ui/console_ui.py

| Función | Descripción |
|---------|-------------|
| `render_towers(towers, num_disks=None)` | Dibuja las 3 torres con discos proporcionales. Recibe `game.get_state()`. |
| `ask_move()` | Pide origen y destino. Acepta `1 3`, `1,3`, `1-3`, `1>3` y `13`. Devuelve `(origen, destino)` en base 0, o `None` si el usuario sale (`q`, `salir`, Ctrl+C/Ctrl+D). Solo valida el formato. |
| `show_message(message)` | Mensaje informativo. |
| `show_error(message)` | Error con prefijo `[!]`. |
| `show_victory(moves, min_moves)` | Pantalla de victoria; avisa si fue partida perfecta. |

Convención: el usuario ve torres 1-3; el resto del código usa índices 0-2.

## utils/helpers.py

| Función | Descripción |
|---------|-------------|
| `calculate_min_moves(num_disks)` | Devuelve 2ⁿ − 1. |
| `parse_num_disks(text)` | Convierte texto a entero y valida el rango. `ValueError` con mensaje claro si no es válido. |
| `ask_num_disks()` | Pide el número de discos hasta recibir uno válido. `None` si el usuario sale. |
| `ask_yes_no(question)` | Pregunta sí/no (`s`, `si`, `sí`, `y`, `yes` / `n`, `no`). `False` si se cierra la entrada. |

## main.py

- `play(game)`: bucle de una partida. Muestra el tablero y los contadores, pide el movimiento y captura el `ValueError` de `game.move()` para mostrarlo con `show_error`. Devuelve `True` si se ganó, `False` si el usuario salió.
- `main()`: pide el número de discos, juega y pregunta si se quiere repetir.

## Flujo de un turno

1. `render_towers(game.get_state(), ...)` y se muestran movimientos y mínimo.
2. `ask_move()` devuelve `(origen, destino)` o `None`.
3. `game.move(origen, destino)`. Si falla, `show_error`.
4. Si `game.is_finished()`, se muestra `show_victory`.

## Criterios de aceptación del MVP

- [x] Tower como pila con validación de tamaño
- [x] Inicialización con N discos (1-10)
- [x] Movimiento con validación de todas las reglas
- [x] Detección de victoria
- [x] Contador de movimientos y mínimo teórico (2ⁿ − 1)
- [x] Render claro de las 3 torres
- [x] Mensajes de error y de victoria
- [x] Entrada de origen y destino
- [x] Flujo principal con validación del número de discos
- [x] Lógica de juego independiente de la interfaz