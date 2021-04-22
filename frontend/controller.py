from threading import Thread
import pygame
from datetime import datetime
from time import sleep
from queue import Queue
import gui


class FrontendController(Thread):
    FPS = 10
    TICK = 1 / FPS

    def __init__(self, context, report_to: Queue, screen_config: gui.ScreenConfig):
        self.tasks = Queue()
        self.report_to = report_to
        self.context = context
        self.screen_config = screen_config

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
        while True:
            sleep(self.TICK)
            delta_t = (datetime.now() - last_tick).total_seconds()
            events = []

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type in (pygame.MOUSEBUTTONUP, pygame.FINGERUP):
                    if event.type == pygame.MOUSEBUTTONUP:
                        x, y = event.pos
                    else:
                        int(self.screen_config.WIDTH * event.x), int(self.screen_config.HEIGHT * event.y)
                    if self.screen_config.TOUCHSCREEN_ROTATION == gui.Rotation.FLIPPED:
                        x = self.screen_config.WIDTH - x
                        y = self.screen_config.HEIGHT - y
                    events.append(gui.ClickEvent(x, y))

            print('Tick!', delta_t)
            navigation_event = self.current_menu.tick(
                delta_t=delta_t,
                events=events,
                tasks=self.tasks,
                report_to=self.report_to,
                screen_config=self.screen_config,
                screen=self.screen,
            )
            # TODO: Change Menu
            if navigation_event:
                if isinstance(navigation_event, gui.RootNavigationEvent):
                    if isinstance(navigation_event.event_data, gui.RootNavigationEvent.SwitchMenu):
                        self.current_menu = navigation_event.event_data.target
                    elif isinstance(navigation_event.event_data, gui.RootNavigationEvent.ReturnHome):
                        self.current_menu = self.MAIN_MENU
                    elif isinstance(navigation_event.event_data, gui.RootNavigationEvent.NoAction):
                        pass
                else:
                    raise RuntimeError("not expecting Events other than RootEvents at this level.")

            last_tick = datetime.now()


if __name__ == '__main__':
    ctrl = FrontendController(
        context=None,
        report_to=Queue(),
        screen_config=gui.ScreenConfig(fullscreen=False)
    )
    ctrl.start()
