import os
import pygame
from game.hanoi_game import HanoiGame

# Carpeta assets/ en la raíz del proyecto (funciona sin importar desde dónde se ejecute)
ASSETS_DIR = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets"))


def load_image(name):
    """Carga una imagen de assets/. Devuelve None si no existe (se usa un dibujo simple)."""
    path = os.path.join(ASSETS_DIR, name)
    try:
        return pygame.image.load(path).convert_alpha()
    except (pygame.error, FileNotFoundError):
        return None

class HanoiGUI:
    WIDTH = 960
    HEIGHT = 640
    FPS = 60

    # Colores tomados de la imagen de referencia (estilo pixel)
    COLOR_BG = (45, 25, 95)
    COLOR_BASE = (139, 90, 43)
    COLOR_POLE = (160, 110, 60)
    COLOR_TEXT = (255, 255, 255)
    COLOR_DISK_BORDER = (16, 10, 24)

    # Un color por tamaño de disco (el juego admite hasta 10 discos)
    DISK_COLORS = [
        (231, 76, 60),    # 1 rojo
        (230, 126, 34),   # 2 naranja
        (241, 196, 15),   # 3 amarillo
        (46, 204, 113),   # 4 verde
        (26, 188, 156),   # 5 turquesa
        (52, 152, 219),   # 6 azul
        (155, 89, 182),   # 7 morado
        (233, 30, 99),    # 8 rosa
        (121, 85, 72),    # 9 café
        (149, 165, 166),  # 10 gris
    ]

    # --- Estilo pixel: cada "pixel" del arte ocupa PIXEL x PIXEL pixeles reales ---
    PIXEL = 4

    # --- Distribución de la escena ---
    NUM_TOWERS = 3
    PLATFORM_X = 30           # esquina de la base de madera (imagen base.png, 900x152)
    PLATFORM_Y = 468
    PLATFORM_TOP_H = 40       # alto de la superficie donde apoyan los discos
    BASE_Y = 492              # y donde apoyan los discos y los palos
    POLE_HEIGHT = 300         # alto del palo (pole_*.png, 24x300)
    POLE_WIDTH = 24

    # --- Discos (medidas en "pixeles de arte") ---
    DISK_UNITS_H = 7          # alto de cada disco
    DISK_UNITS_MIN = 12       # ancho del disco más pequeño
    DISK_UNITS_MAX = 56       # ancho del disco más grande



    def __init__(self, num_disks=3):
        pygame.init()
        pygame.display.set_caption("Torre de Hanói")
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.game = HanoiGame(num_disks)
        self.font = pygame.font.SysFont("consolas", 28)

      # Imágenes estáticas (si falta alguna, se dibuja una versión simple)
        self.img_background = load_image("background.png")
        self.img_base = load_image("base.png")
        self.img_pole_wood = load_image("pole_wood.png")
        self.img_pole_steel = load_image("pole_steel.png")  # torre 3 (meta)
 
        self._disk_cache = {}

    # ------------------------------------------------------------------
    # Medidas del dibujo (también las usará el Punto 2.3 para los clics)
    # ------------------------------------------------------------------
    def tower_center_x(self, index):
        """Coordenada x del centro de la torre `index` (0, 1 o 2)."""
        section = self.WIDTH // self.NUM_TOWERS
        return section * index + section // 2
 
    def tower_rect(self, index):
        """Rectángulo de la columna de la torre (útil para detectar clics)."""
        section = self.WIDTH // self.NUM_TOWERS
        top = self.BASE_Y - self.POLE_HEIGHT
        bottom = self.PLATFORM_Y + self.PLATFORM_TOP_H
        return pygame.Rect(section * index, top, section, bottom - top)
 
    def disk_color(self, size):
        return self.DISK_COLORS[(size - 1) % len(self.DISK_COLORS)]
 
    def disk_units(self, size):
        """Ancho del disco en pixeles de arte: proporcional a su tamaño (siempre par)."""
        biggest = self.game.num_disks
        if biggest <= 1:
            return self.DISK_UNITS_MAX
        step = (self.DISK_UNITS_MAX - self.DISK_UNITS_MIN) / (biggest - 1)
        units = self.DISK_UNITS_MIN + (size - 1) * step
        return int(round(units / 2) * 2)
 
    def disk_surface(self, size):
        """Imagen pixel-art de un disco (se crea una vez y se reutiliza)."""
        key = (size, self.game.num_disks)
        if key not in self._disk_cache:
            self._disk_cache[key] = self._build_disk(size)
        return self._disk_cache[key]
 
    def _build_disk(self, size):
        units = self.disk_units(size)
        h = self.DISK_UNITS_H
        base = self.disk_color(size)
        light = tuple(min(255, c + 55) for c in base)
        dark = tuple(int(c * 0.62) for c in base)
 
        small = pygame.Surface((units, h), pygame.SRCALPHA)
        for y in range(h):
            for x in range(units):
                edge_x = x in (0, units - 1)
                edge_y = y in (0, h - 1)
                if edge_x and edge_y:
                    continue  # esquina transparente: da el borde redondeado
                if edge_x or edge_y:
                    color = self.COLOR_DISK_BORDER
                elif y == 1:
                    color = light      # brillo superior
                elif y >= h - 2:
                    color = dark       # sombra inferior
                else:
                    color = base
                small.set_at((x, y), color)
        return pygame.transform.scale(
            small, (units * self.PIXEL, h * self.PIXEL))


    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self):
        pass

    # ------------------------------------------------------------------
    # Dibujado (de atrás hacia adelante: fondo, base, palos, discos)
    # ------------------------------------------------------------------
    def draw_background(self):
        if self.img_background:
            self.screen.blit(self.img_background, (0, 0))
        else:
            self.screen.fill(self.COLOR_BG)
 
    def draw_base(self):
        """Base de madera sobre la que están las 3 torres."""
        if self.img_base:
            self.screen.blit(self.img_base, (self.PLATFORM_X, self.PLATFORM_Y))
            return
        for i in range(self.NUM_TOWERS):  # versión simple si falta la imagen
            x = self.tower_center_x(i) - 140
            pygame.draw.rect(self.screen, self.COLOR_BASE,
                             pygame.Rect(x, self.BASE_Y, 280, 24))
 
    def draw_poles(self):
        """Los 3 palos; el de la torre 3 (meta) es de metal."""
        for i in range(self.NUM_TOWERS):
            image = self.img_pole_steel if i == self.NUM_TOWERS - 1 else self.img_pole_wood
            if image:
                x = self.tower_center_x(i) - image.get_width() // 2
                y = self.BASE_Y - image.get_height()
                self.screen.blit(image, (x, y))
            else:
                x = self.tower_center_x(i) - self.POLE_WIDTH // 2
                pole = pygame.Rect(x, self.BASE_Y - self.POLE_HEIGHT,
                                   self.POLE_WIDTH, self.POLE_HEIGHT)
                pygame.draw.rect(self.screen, self.COLOR_POLE, pole)
 
    def draw_disks(self):
        """Dibuja los discos según el estado actual de HanoiGame.
 
        get_state() devuelve 3 listas, de la base a la cima. Cada disco se
        solapa 1 pixel de arte con el de abajo para compartir el borde negro.
        """
        disk_h = self.DISK_UNITS_H * self.PIXEL
        step = (self.DISK_UNITS_H - 1) * self.PIXEL
        for tower_index, tower in enumerate(self.game.get_state()):
            center_x = self.tower_center_x(tower_index)
            for level, size in enumerate(tower):
                surface = self.disk_surface(size)
                x = center_x - surface.get_width() // 2
                y = self.BASE_Y - disk_h - level * step
                self.screen.blit(surface, (x, y))
 
    def draw(self):
        self.draw_background()
        self.draw_base()
        self.draw_poles()
        self.draw_disks()
        pygame.display.flip()
 
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.FPS)
        pygame.quit()


def main():
    gui = HanoiGUI(num_disks=3)
    gui.run()


if __name__ == "__main__":
    main()
