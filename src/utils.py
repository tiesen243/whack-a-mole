import pygame


# Mode
mode = {
    "NORMAL": {
        "Col": 3,
        "Row": 3,
    },
    "HARD": {
        "Col": 6,
        "Row": 6,
    },
}


# Utils function
def drawMatrix(current_mode: dict, screen: pygame.Surface, matrixRect: list) -> None:
    hole = pygame.image.load("../assets/imgs/hole.png").convert_alpha()
    x, y = 0, 0

    if current_mode == mode["HARD"]:
        multi = 150
        coe = 80

    elif current_mode == mode["NORMAL"]:
        multi = 300
        coe = 150

    else:
        multi = 0
        coe = 0

    for _ in range(current_mode["Row"]):
        x = 0
        for _ in range(current_mode["Col"]):
            screen.blit(hole, (x * multi + coe, y * multi + coe))
            r = pygame.rect.Rect(x * multi + coe, y * multi + coe, 100, 100)
            matrixRect.append(r)
            x += 1
        y += 1


def draw_text(text: str, size: int, x: int, y: int, screen) -> None:
    font = pygame.font.Font("../assets/fonts/ComicNeue-Bold.ttf", size)
    text_surface = font.render(text, True, (0, 0, 0))
    screen.blit(text_surface, (x, y))
