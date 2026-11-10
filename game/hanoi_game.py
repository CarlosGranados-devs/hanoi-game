from models.tower import Tower


class HanoiGame:
    NUM_TOWERS = 3
    MIN_DISKS = 1
    MAX_DISKS = 10

    MODE_NORMAL = "normal"
    MODE_PERFECT = "perfect"
    MODE_TIMED = "timed"
    MODES = (MODE_NORMAL, MODE_PERFECT, MODE_TIMED)

    def __init__(self, num_disks, mode=MODE_NORMAL):
        if not isinstance(num_disks, int) or isinstance(num_disks, bool):
            raise ValueError("El número de discos debe ser un entero.")
        if num_disks < self.MIN_DISKS or num_disks > self.MAX_DISKS:
            raise ValueError(
                f"El número de discos debe estar entre {self.MIN_DISKS} y {self.MAX_DISKS}."
            )
        if mode not in self.MODES:
            raise ValueError(
                f"Modo inválido. Debe ser uno de: {', '.join(self.MODES)}."
            )
        self.num_disks = num_disks
        self.mode = mode
        self.min_moves = 2 ** num_disks - 1
        self.towers = []
        self.moves = 0
        self.lost = False
        self.reset()

    def reset(self):
        self.towers = [Tower() for _ in range(self.NUM_TOWERS)]
        for disk in range(self.num_disks, 0, -1):
            self.towers[0].push(disk)
        self.moves = 0
        self.lost = False

    def _validate_index(self, index):
        if not isinstance(index, int) or isinstance(index, bool):
            raise ValueError("La torre debe indicarse con un número entero.")
        if index < 0 or index >= self.NUM_TOWERS:
            raise ValueError(
                f"Torre inválida. Debe estar entre 1 y {self.NUM_TOWERS}."
            )

    def is_valid_move(self, from_tower, to_tower):
        try:
            self._validate_index(from_tower)
            self._validate_index(to_tower)
        except ValueError:
            return False
        if from_tower == to_tower:
            return False
        origin = self.towers[from_tower]
        destination = self.towers[to_tower]
        if origin.is_empty():
            return False
        if destination.is_empty():
            return True
        return origin.peek() < destination.peek()

    def move(self, from_tower, to_tower):
        if self.lost:
            raise ValueError("La partida ya está perdida.")
        self._validate_index(from_tower)
        self._validate_index(to_tower)
        if from_tower == to_tower:
            raise ValueError(
                "La torre origen y la torre destino deben ser distintas.")
        origin = self.towers[from_tower]
        destination = self.towers[to_tower]
        if origin.is_empty():
            raise ValueError("La torre origen está vacía.")
        if not destination.is_empty() and origin.peek() > destination.peek():
            raise ValueError(
                "No se puede colocar un disco grande sobre uno más pequeño.")
        disk = origin.pop()
        destination.push(disk)
        self.moves += 1

        if self.mode == self.MODE_PERFECT and self.moves > self.min_moves:
            self.lost = True

        return disk

    def is_finished(self):
        if self.mode == self.MODE_PERFECT:
            return self.towers[2].size() == self.num_disks and not self.lost
        return self.towers[2].size() == self.num_disks

    def is_won(self):
        return self.is_finished()

    def is_lost(self):
        return self.lost

    def is_over(self):
        """Partida terminada (ganada o perdida)."""
        return self.is_finished() or self.is_lost()

    def get_mode(self):
        return self.mode

    def get_state(self):
        return [tower.get_disks() for tower in self.towers]

    def get_towers(self):
        return self.get_state()

    def get_moves(self):
        return self.moves

    def get_min_moves(self):
        return self.min_moves
