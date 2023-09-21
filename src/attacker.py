from pygame import sprite, mouse, mixer
from pygame.image import load


imgs = [
    "../assets/imgs/bonk-before.gif",
    "../assets/imgs/bonk-after.gif",
    "../assets/imgs/bomb.png",
]


class Attacker(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load(imgs[0]).convert_alpha()
        self.rect = self.image.get_rect()
        self.boom_sfx = mixer.Sound("../assets/sounds/boom.mp3")

    def hit(self, target):
        self.image = load(imgs[1]).convert()
        return sprite.spritecollide(self, target, False)

    def unhit(self):
        self.image = load(imgs[0]).convert_alpha()

    def bomb(self):
        self.image = load(imgs[2]).convert_alpha()

    def boom(self, target_group):
        mouse_pos = mouse.get_pos()
        self.boom_sfx.play()
        count = 0
        for target in target_group:
            dx = target.rect.centerx - mouse_pos[0]
            dy = target.rect.centery - mouse_pos[1]
            dist_sq = dx * dx + dy * dy
            if dist_sq <= 400 * 400:
                count += 1
        return count

    def update(self):
        self.rect.center = mouse.get_pos()
