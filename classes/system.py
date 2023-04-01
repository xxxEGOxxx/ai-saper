import pygame


class Window:
    window: None
    width: int
    height: int
    title: str
    icon_path: str
    paused: bool
    pause_menu: None

    search: pygame.Surface

    def __init__(self, width: int = 640, height: int = 480, title="", icon_path=""):
        self.set_resolution(width, height)
        self.set_title(title)
        self.set_icon(icon_path)
        self.mount()
        self.paused = False

        self.pause_menu = pygame.Surface((width, height))
        self.pause_menu.set_alpha(128)
        self.pause_menu.fill((0, 0, 0))
        self.search = pygame.Surface((width, height), flags=pygame.SRCALPHA)

    def set_resolution(self, width: int, height: int):
        self.width = width
        self.height = height

    def set_title(self, title: str):
        self.title = title

    def set_icon(self, icon_path: str):
        self.icon_path = icon_path

    def mount(self):
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        if self.icon_path != "":
            icon = pygame.image.load(self.icon_path)
            pygame.display.set_icon(icon)

    def pause(self, paused: bool):
        self.paused = paused
        if self.paused:
            self.window.blit(self.pause_menu, (0, 0))
            pygame.display.update()

    def draw_search(self, pos1: list = [0, 0], pos2: list = [0, 0], tile_size: int = 64, map=None, saper=None):
        map.draw_tiles()
        map.draw_objects()
        saper.draw(self.window, 0.1)
        self.window.blit(self.pause_menu, (0, 0))
        self.search = pygame.Surface((self.width, self.height), flags=pygame.SRCALPHA)
        pos1 = [pos1[0] * tile_size + (tile_size / 2), pos1[1] * tile_size + (tile_size / 2)]
        pos2 = [pos2[0] * tile_size + (tile_size / 2), pos2[1] * tile_size + (tile_size / 2)]
        pygame.draw.line(self.search, pygame.Color(255, 0, 0), pos1, pos2, 5)

        n = 10
        p1 = 0
        p2 = 0
        p3 = 0
        if (pos2[0] - pos1[0]) != 0:
            a1 = (pos2[1] - pos1[1]) / (pos2[0] - pos1[0])
            b1 = (pos1[1] - a1 * pos1[0])
            if a1 != 0:
                a2 = -(1 / a1)
                b2 = pos2[1] - a2 * pos2[0]
                y = a2 * (pos2[0] + n) + b2
                p1 = (pos2[0] + n, y)
                y = a2 * (pos2[0] - n) + b2
                p2 = (pos2[0] - n, y)
                if pos1[0] > pos2[0]:
                    y = a1 * (pos2[0] - n) + b1
                    p3 = (pos2[0] - n, y)
                else:
                    y = a1 * (pos2[0] + n) + b1
                    p3 = (pos2[0] + n, y)
            else:
                p1 = (pos2[0], pos2[1] + n)
                p2 = (pos2[0], pos2[1] - n)
                if pos1[0] > pos2[0]:
                    p3 = (pos2[0] - n, pos2[1])
                else:
                    p3 = (pos2[0] + n, pos2[1])
        else:
            p1 = (pos2[0] - n, pos2[1])
            p2 = (pos2[0] + n, pos2[1])
            if pos1[1] > pos2[1]:
                p3 = (pos2[0], pos2[1] - n)
            else:
                p3 = (pos2[0], pos2[1] + n)

        pygame.draw.polygon(self.search, pygame.Color(255, 0, 0), (p1, p2, p3))
        self.window.blit(self.search, (0, 0))
        pygame.display.update()
