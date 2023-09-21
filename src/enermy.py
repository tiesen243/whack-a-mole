from pygame import image, sprite
from random import choice, randint


imgs = [
    "../assets/imgs/enermy1.png",
    "../assets/imgs/enermy2.png",
    "../assets/imgs/enermy3.png",
    "../assets/imgs/enermy4.png",
]
die_img = "../assets/imgs/enermy_die.png"


class Enermy(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image.load(choice(imgs)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.midbottom = (randint(0, 1000), randint(0, 1000))

    def die(self):
        self.image = image.load(die_img).convert_alpha()

    def update(self, pos_list):
        self.rect.center = choice(pos_list).center
