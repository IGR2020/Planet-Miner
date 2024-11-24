import pygame as pg
from time import time
import math
from game import Game

assets = {"Space Station": pg.image.load("assets/Space Station.png")}


class Ship:
    vel = 0
    angle = 0
    sink_speed = 0.1
    hrt_vel, vrt_vel = 0, 0
    disabled = False
    disabled_time = 0.5
    time_since_disabled = 0
    pressure_limit = 2_000
    health = 200
    max_health = health
    selectedSlot = 0
    totalHotBarSlots = 9  # 8 if indexing
    damage = 0
    speed = 10
    acceleration = 1
    rotationSpeed = 5

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

        angle = math.degrees(math.atan2(dy, dx)) - self.correctionAngle - 90
        if angle > self.angle + self.rotationSpeed:
            self.angle += self.rotationSpeed
            self.reload()
        elif angle < self.angle - self.rotationSpeed:
            self.angle -= self.rotationSpeed
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

class SpaceEnvironment(Game):
    ship = Ship(100, 100, "Space Station", 0)

    def display(self) -> None:
        self.ship.display(self.window, 0, 0)

    def tick(self) -> None:
        self.ship.script()

SpaceEnvironment((900, 500), "Space").start()