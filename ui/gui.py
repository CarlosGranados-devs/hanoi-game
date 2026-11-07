import pygame
from game.hanoi_game import HanoiGame


class HanoiGUI:
    WIDTH = 960
    HEIGHT = 640
    FPS = 60

    # Colores tomados de la imagen de referencia (estilo pixel)
    COLOR_BG = (45, 25, 95)
    COLOR_BASE = (139, 90, 43)
    COLOR_POLE = (160, 110, 60)
    COLOR_TEXT = (255, 255, 255)

    def __init__(self, num_disks=3):
        pygame.init()
        pygame.display.set_caption("Torre de Hanói")
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.game = HanoiGame(num_disks)
        self.font = pygame.font.SysFont("consolas", 28)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self):
        pass

    def draw(self):
        self.screen.fill(self.COLOR_BG)

        # Placeholder de texto para verificar que la ventana funciona
        text = self.font.render(
            "Torre de Hanói - GUI base (Punto 1)", True, self.COLOR_TEXT)
        rect = text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
        self.screen.blit(text, rect)

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
