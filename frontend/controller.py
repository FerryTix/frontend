from threading import Thread
from datetime import datetime
from time import sleep
from queue import Queue
from enum import Enum
import gui


class Rotation(Enum):
    NORMAL = 0
    LEFT = 3
    RIGHT = 1
    FLIPPED = 2

    R0 = NORMAL
    R90 = RIGHT
    R180 = FLIPPED
    R270 = LEFT


class ScreenConfig:
    def __init__(self, width: int = 1280, height: int = 800,
                 display_rotation: Rotation = Rotation.R0,
                 touchscreen_rotation: Rotation = Rotation.R0):
        self.WIDTH = width
        self.HEIGHT = height
        self.DISPLAY_ROTATION = display_rotation
        self.TOUCHSCREEN_ROTATION = touchscreen_rotation


class FrontendController(Thread):
    FPS = 30
    TICK = 1 / 30
    MAIN_MENU = gui.main_menu.MainMenu()
    TOP_UP_MENU = gui.top_up_menu.TopUpMenu()
    BUY_TICKET_MENU = gui.buy_ticket_menu.BuyTicketMenu()
    USE_RETURN_TICKET_MENU = gui.use_return_ticket_menu.UseReturnTicketMenu()

    def __init__(self, context, report_to: Queue, screen_config: ScreenConfig):
        super(FrontendController, self).__init__(target=self.handler)
        self.tasks = Queue()
        self.report_to = report_to
        self.context = context
        self.screen_config = screen_config
        self.current_menu: gui.Menu = FrontendController.MAIN_MENU

    def handler(self):
        last_tick = datetime.now()
        while True:
            sleep(self.TICK)
            delta_t = (datetime.now() - last_tick).total_seconds()
            latest_task = None
            if self.tasks.not_empty:
                latest_task = self.tasks.get()
            self.current_menu, result_event = self.current_menu.tick(delta_t=delta_t, event=latest_task)
            if result_event:
                self.report_to.put(result_event)
            last_tick = datetime.now()
