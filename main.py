import pygame as pg
from time import time
import math
from game import Game

assets = {"Space Station": pg.transform.scale_by(pg.image.load("assets/Space Station.png"), 4), "Planet": pg.transform.scale_by(pg.image.load("assets/Planet.png"), 20)}


class Ship:
    vel = 0
    angle = 0
    sink_speed = 0.1
    hrt_vel, vrt_vel = 0, 0
    disabled = False
    disabled_time = 0.5
    time_since_disabled = 0
    damage = 0
    speed = 10
    acceleration = 1

    def __init__(self, x, y, name, correctionAngle: int):
        """correctionAngle -> should make it so that when the
                object is rotated by that amount it faces up."""
        self.rect = pg.Rect(x, y, assets[name].get_width(), assets[name].get_height())
        self.name = name
        self.rotatedImage = pg.transform.rotate(assets[name], self.angle)
        self.mask = pg.mask.from_surface(self.rotatedImage)

        self.correctionAngle = correctionAngle

    def display(self, window, x_offset, y_offset):
        window.blit(self.rotatedImage, (self.rect.x - x_offset, self.rect.y - y_offset))

    def move(self):
        radians = math.radians(self.angle)
        self.hrt_vel = math.sin(radians) * self.vel
        self.vrt_vel = math.cos(radians) * self.vel
        self.rect.x -= self.hrt_vel
        self.rect.y -= self.vrt_vel

    def reload(self):
        self.rotatedImage = pg.transform.rotate(assets[self.name], self.angle)
        self.rect = self.rotatedImage.get_rect(center=self.rect.center)
        self.mask = pg.mask.from_surface(self.rotatedImage)

    def script(self, x_offset: int = 0, y_offset: int = 0):

        # mouse facing
        mouseX, mouseY = pg.mouse.get_pos()
        mouseX += x_offset
        mouseY += y_offset

        # distance from mouse
        dx, dy = (
            mouseX - self.rect.centerx,
            self.rect.centery - mouseY,
        )

        self.angle = math.degrees(math.atan2(dy, dx)) - self.correctionAngle - 90
        self.reload()

        # getting inputs
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            if self.disabled:
                self.vel += 0.3
            else:
                self.vel += self.acceleration

        # auto removing disabled tag
        if time() - self.time_since_disabled > self.disabled_time:
            self.disabled = False

        # adding the velocities
        self.move()
        if self.vel > 0:
            if self.disabled:
                self.vel -= 0.1
            else:
                self.vel -= 0.5
            self.vel = max(self.vel, 0)
        elif self.vel < 0:
            if self.disabled:
                self.vel += 0.1
            else:
                self.vel += 0.5
            self.vel = min(self.vel, 0)
        self.vel = max(min(self.vel, self.speed), -self.speed)


class CoreObject:
    type = "Object"

    def __init__(
        self, x: int, y: int, name: str, scale: int | float = 1, angle: int = 0, size: tuple[int, int] | list[int, int] = None, data=None
    ) -> None:
        self.name = name
        self.rect: pg.Rect = assets[name].get_rect(topleft=(x, y))
        self.mask = pg.mask.from_surface(assets[name])
        self.scale = scale
        self.angle = angle
        if size is None:
            self.size = self.rect.width, self.rect.height
        else:
            self.size = size
        self.size = [self.size[0], self.size[1]]
        self.reload()
        self.data = data

    def resetSize(self) -> None:
        self.size = [assets[self.name].get_width(), assets[self.name].get_height()]

    def reload(self) -> None:
        self.morphedImage = pg.transform.scale(assets[self.name], self.size)
        self.scaledImage = pg.transform.scale_by(self.morphedImage, self.scale)
        self.rotatedImage = pg.transform.rotate(self.scaledImage, self.angle)
        self.mask = pg.mask.from_surface(self.rotatedImage)
        self.rect = self.rotatedImage.get_rect(center=self.rect.center)

    def rotate(self) -> None:
        self.rotatedImage = pg.transform.rotate(self.scaledImage, self.angle)
        self.mask = pg.mask.from_surface(self.rotatedImage)
        self.rect = self.rotatedImage.get_rect(center=self.rect.center)

    def script(self, *args): ...

    def display(self, window: pg.Surface, x_offset: int = 0, y_offset: int = 0) -> None:
        window.blit(self.rotatedImage, (self.rect.x - x_offset, self.rect.y - y_offset))

    def pack(self):
        self.morphedImage, self.scaledImage, self.rotatedImage, self.mask = None, None, None, None

    def unpack(self):
        self.reload()

    def collide(self, *args): return []

    def resolveXCollision(self, player, *args):
        if pg.sprite.collide_mask(player, self): return True
        return False

    def resolveYCollision(self, player, *args):
        if pg.sprite.collide_mask(player, self): return True
        return False

class SpaceEnvironment(Game):
    def onInit(self):
        self.ship = Ship(100, 100, "Space Station", 0)

        self.x_offset, self.y_offset = 0, 0

        self.spaceObjects = [CoreObject(100, 100, "Planet")]

    def display(self) -> None:
        for obj in self.spaceObjects:
            obj.display(self.window, self.x_offset, self.y_offset)

        self.ship.display(self.window, self.x_offset, self.y_offset)

    def tick(self) -> None:
        self.x_offset, self.y_offset = self.ship.rect.centerx - self.width/2, self.ship.rect.centery - self.height/2
        self.ship.script(self.x_offset, self.y_offset)

        for obj in self.spaceObjects:
            obj.angle += 1
            obj.rotate()


if __name__ == "__main__":
    instance = SpaceEnvironment((900, 500), "Planet Miner (Space)", background=(0, 0, 0))
    instance.start()
