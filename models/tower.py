class Tower:
    def __init__(self):
        self._disks = []

    def push(self, disk):
        if not self.is_empty() and disk > self.peek():
            raise ValueError("No se puede colocar un disco más grande sobre uno más pequeño")
        self._disks.append(disk)

    def pop(self):
        if self.is_empty():
            raise IndexError("La torre está vacía")
        return self._disks.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("La torre está vacía")
        return self._disks[-1]

    def is_empty(self):
        return len(self._disks) == 0

    def size(self):
        return len(self._disks)

    def get_disks(self):
        return self._disks.copy()