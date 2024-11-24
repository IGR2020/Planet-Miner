import pygame as pg

class Game:
    def __init__(
            self,
            resolution: tuple[int, int],
            name: str,
            fps: int = 60,
            background: tuple[int, int, int] = (255, 255, 255),
    ):
        self.width, self.height = resolution
        self.name = name
        self.window = pg.display.set_mode(resolution, flags=pg.RESIZABLE)
        self.fps = fps
        self.clock = pg.time.Clock()
        self.run = True
        self.background = background
        pg.display.set_caption(name)
        self.deltaTime = 0

    def tick(self) -> None: ...

    def display(self) -> None: ...

    def event(self, event: pg.event.Event) -> None: ...

    def debug(self): ...

    def videoResize(self): ...

    def quit(self):
        """Use this function if you want to return something from the [game].start() function"""

    def start(self):
        while self.run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.run = False
                if event.type == pg.KEYDOWN and event.key == pg.K_F3:
                    print(f"[Graphics] delta time {self.deltaTime}")
                    self.debug()

                if event.type == pg.VIDEORESIZE:
                    self.width, self.height = event.dict["size"]
                    self.videoResize()

                self.event(event)

            self.deltaTime = self.clock.tick(self.fps) / 16
            if self.deltaTime > 1.2:
                print("[Graphics] Low FPS")
            self.tick()
            self.window.fill(self.background)
            self.display()
            pg.display.update()

        return self.quit()