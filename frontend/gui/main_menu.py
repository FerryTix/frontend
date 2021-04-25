from typing import List
from datetime import datetime
from .base import Screen, Menu, NavigationEvent, Event, HitBox, ClickEvent, Overlay, SwitchMenu, NoAction
from queue import Queue
from .constants import *
from .colors import Colors


class TitleOverlay(Overlay):
    def __init__(self, context):
        super().__init__(context=context)

    def tick(self, redraw, delta_t: float, events: List[Event], tasks: Queue, report_to: Queue,
             **kwargs) -> NavigationEvent:
        screen = self.context.screen
        screen_config = self.context.screen_config

        title_rect = pygame.Rect(0, 0, screen_config.WIDTH, 200)
        pygame.draw.rect(screen, Colors.GRAY, title_rect)

        title = oxygen54.render("Ticketautomat Personenfähre Keer Tröch II", True, Colors.BLACK)
        subtitle = oxygen48.render("Bislich -> Xanten", True, Colors.BLACK)

        screen.blit(title, ((screen_config.WIDTH - title.get_width()) / 2, 42))
        screen.blit(subtitle, ((screen_config.WIDTH - subtitle.get_width()) / 2, 119))

        return NoAction()


class WelcomeScreen(Screen):
    def __init__(self, context, vending_status: bool = True):
        super().__init__(context=context, overlays=[TitleOverlay(
            context=context
        )])
        self.vending_status = vending_status
        self.buttons = MainMenu.Buttons()
        self.last_journey = "19:00 Uhr"
        self.num_bikes = 0
        self.num_passengers = 0

    def draw(self, delta_t: float, events: List[Event], tasks: Queue, report_to: Queue, **kwargs) -> None:
        screen = self.context.screen
        screen.fill(color=Colors.BACKGROUND)
        screen_config = self.context.screen_config

        info_rect = pygame.Rect(50, 250, 550, 400)
        pygame.draw.rect(screen, Colors.GRAY2, info_rect, border_radius=15, )
        tmp_rendered_text = oxygen48.render("Fährzeiten", True, Colors.BLACK)
        screen.blit(tmp_rendered_text, (50 + 10, 250 + 1))

        info_rect = pygame.Rect(680, 250, 550, 400)
        pygame.draw.rect(screen, Colors.GRAY2, info_rect, border_radius=15, )
        tmp_rendered_text = oxygen48.render("Information", True, Colors.BLACK)
        screen.blit(tmp_rendered_text, (680 + 114, 250 + 1))
        tmp_rendered_text = oxygen36.render("Uhrzeit:", True, Colors.BLACK)
        screen.blit(tmp_rendered_text, (
            680 + (250 - tmp_rendered_text.get_width()) / 2, 250 + 86 + (77 - tmp_rendered_text.get_height()) / 2))
        tmp_rendered_text = oxygen48.render(f"{datetime.now().time().strftime('%H:%M')} Uhr", True, Colors.BLACK)
        screen.blit(tmp_rendered_text, (680 + 250 + (300 - tmp_rendered_text.get_width()) / 2,
                                        250 + 86 + (77 - tmp_rendered_text.get_height()) / 2))
        tmp_rendered_text = oxygen36.render("Letzte Fahrt:", True, Colors.GRAY3)
        screen.blit(tmp_rendered_text, (
            680 + (250 - tmp_rendered_text.get_width()) / 2, 250 + 165 + (77 - tmp_rendered_text.get_height()) / 2))
        tmp_rendered_text = oxygen48.render(self.last_journey, True, Colors.GRAY3)
        screen.blit(tmp_rendered_text, (680 + 250 + (300 - tmp_rendered_text.get_width()) / 2,
                                        250 + 165 + (77 - tmp_rendered_text.get_height()) / 2))
        tmp_rendered_text = oxygen36.render("Aktuell im Wartebereich:", True, Colors.BLACK)
        screen.blit(tmp_rendered_text, (
            680 + (550 - tmp_rendered_text.get_width()) / 2, 250 + 242 + (77 - tmp_rendered_text.get_height()) / 2))
        tmp_rendered_text = oxygen36.render(f"P: {self.num_passengers}", True, Colors.BLACK)
        screen.blit(tmp_rendered_text, (680 + 142 + (152 - tmp_rendered_text.get_width()) / 2,
                                        250 + 309 + (91 - tmp_rendered_text.get_height()) / 2))
        tmp_rendered_text = oxygen36.render(f"F: {self.num_bikes}", True, Colors.BLACK)
        screen.blit(tmp_rendered_text, (680 + 291 + (152 - tmp_rendered_text.get_width()) / 2,
                                        250 + 309 + (91 - tmp_rendered_text.get_height()) / 2))

        buy_ticket_rect = pygame.Rect(440, 676, 400, 90)
        pygame.draw.rect(screen, Colors.GREEN, buy_ticket_rect, border_radius=25, )
        subtitle = oxygen36.render("Ticket kaufen", True, Colors.BACKGROUND)
        screen.blit(subtitle,
                    ((screen_config.WIDTH - subtitle.get_width()) / 2, 676 + (90 - subtitle.get_height()) // 2))

        faehrcard_rect = pygame.Rect(895, 690, 340, 70)
        pygame.draw.rect(screen, Colors.BLUE, faehrcard_rect, border_radius=25, )
        subtitle = oxygen36.render("FährCard aufladen", True, Colors.BACKGROUND)
        screen.blit(subtitle,
                    (895 + (340 - subtitle.get_width()) / 2, 690 + (70 - subtitle.get_height()) // 2))

        return_rect = pygame.Rect(45, 690, 340, 70)
        pygame.draw.rect(screen, Colors.TEAL, return_rect, border_radius=25, )
        subtitle = oxygen36.render("Rückfahrt einlösen", True, Colors.BACKGROUND)
        screen.blit(subtitle, (45 + (340 - subtitle.get_width()) / 2, 690 + (70 - subtitle.get_height()) // 2))

        actions = []
        for overlay in self.overlays:
            res = overlay.tick(True, delta_t, events, tasks, report_to, **kwargs)
            if res:
                actions.append(res)

        pygame.display.flip()

    def process_events(self, events) -> NavigationEvent:
        for event in events:
            if isinstance(event, ClickEvent):
                for btn in self.buttons.all:
                    if btn.collides_with(x=event.x, y=event.y):
                        if btn is self.buttons.BuyTicket:
                            return SwitchMenu(target=self.context.BUY_TICKET_MENU)
                        elif btn is self.buttons.UseReturnTicket:
                            return SwitchMenu(target=self.context.USE_RETURN_TICKET_MENU)
                        elif btn is self.buttons.TopUpFaehrCard:
                            return SwitchMenu(target=self.context.TOP_UP_MENU)
                        raise RuntimeError("Where my button??")
        return NoAction()


class MainMenu(Menu):
    class Buttons:
        def __init__(self):
            self.BuyTicket = HitBox(x=440, y=676, width=400, height=90)  # 7
            self.TopUpFaehrCard = HitBox(x=895, y=690, width=340, height=70)  # 1
            self.UseReturnTicket = HitBox(x=45, y=690, width=340, height=70)  # 3
            self.all = self.BuyTicket, self.TopUpFaehrCard, self.UseReturnTicket

    def __init__(self, context):
        self.vending_status = True
        self.welcome_screen = WelcomeScreen(context=context, vending_status=self.vending_status)
        super(MainMenu, self).__init__(
            entry_point=self.welcome_screen,
            screens=[self.welcome_screen],
            context=context,
        )
