from threading import Thread
import pygame
from datetime import datetime
from time import sleep
from queue import Queue
import gui
from pygame import camera

camera.init()


class FrontendController(Thread):
    FPS = 30
    TICK = 1 / FPS

    def __init__(self, context, report_to: Queue, screen_config: gui.ScreenConfig):
        self.tasks = Queue()
        self.report_to = report_to
        self.context = context
        self.screen_config = screen_config
        self.camera = camera.Camera(camera.list_cameras()[0], (640, 480))

        if screen_config.FULLSCREEN:
            self.screen = pygame.display.set_mode((screen_config.WIDTH, screen_config.HEIGHT), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((screen_config.WIDTH, screen_config.HEIGHT), )

        self.current_menu = self.MAIN_MENU = gui.main_menu.MainMenu(context=self)
        self.TOP_UP_MENU = gui.top_up_menu.TopUpMenu(context=self)
        self.BUY_TICKET_MENU = gui.buy_ticket_menu.BuyTicketMenu(context=self)
        self.USE_RETURN_TICKET_MENU = gui.use_return_ticket_menu.UseReturnTicketMenu(context=self)

        super(FrontendController, self).__init__(target=self.handler)

    def handler(self):
        last_tick = datetime.now()
        last_minute = datetime.now().minute
        redraw = True
        while True:
            sleep(self.TICK)
            delta_t = (datetime.now() - last_tick).total_seconds()
            events = []

            if datetime.now().minute != last_minute:
                redraw = True
                last_minute = datetime.now().minute

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type in (pygame.MOUSEBUTTONUP, pygame.FINGERUP):
                    if event.type == pygame.MOUSEBUTTONUP:
                        x, y = event.pos
                    else:
                        x, y = int(self.screen_config.WIDTH * event.x), int(self.screen_config.HEIGHT * event.y)
                    if self.screen_config.TOUCHSCREEN_ROTATION == gui.Rotation.FLIPPED:
                        x = self.screen_config.WIDTH - x
                        y = self.screen_config.HEIGHT - y
                    events.append(gui.ClickEvent(x, y))

            navigation_event = self.current_menu.tick(
                redraw=redraw,
                delta_t=delta_t,
                events=events,
            )

            redraw = False

            if navigation_event:
                redraw = True
                if isinstance(navigation_event, gui.RequireDraw):
                    pass
                elif isinstance(navigation_event, gui.SwitchMenu):
                    self.current_menu.exit()
                    self.current_menu = navigation_event.target
                    self.current_menu.enter()
                elif isinstance(navigation_event, gui.ReturnHome):
                    self.current_menu.exit()
                    self.current_menu = self.MAIN_MENU
                    self.current_menu.enter()
                else:
                    raise RuntimeError("not expecting Events other than RootEvents at this level.")

            print(f'\rFrame render time: {(datetime.now() - last_tick).total_seconds() - FrontendController.TICK}'
                  f' {redraw}', end='')
            last_tick = datetime.now()


if __name__ == '__main__':
    import os

    print(os.getpid())
    ctrl = FrontendController(
        context=None,
        report_to=Queue(),
        screen_config=gui.ScreenConfig(fullscreen=False)
    )
    ctrl.start()
