from .base import Overlay, NavigationEvent, Event, HitBox, ClickEvent, NoAction, ReturnHome
from datetime import datetime
from .constants import *
from .colors import Colors
import pygame


class NavigationOverlay(Overlay):
    def __init__(
            self, context, title: str,
            on_back_button_press: NavigationEvent = ReturnHome(),
            show_time: bool = True,
    ):
        self.back_button = HitBox(19, 11, 250, 70)
        self.title = title
        self.on_back_button_press = on_back_button_press
        self.show_time = show_time
        super(NavigationOverlay, self).__init__(context=context)

    def draw(self, delta_t: float) -> None:
        heading = self.title
        screen = self.context.screen

        pygame.draw.rect(screen, Colors.GRAY, pygame.Rect(0, 0, self.context.screen_config.WIDTH, 90))
        rendered_heading = oxygen54.render(heading, True, Colors.BLACK)
        screen.blit(
            rendered_heading,
            ((self.context.screen_config.WIDTH - rendered_heading.get_width()) / 2,
             13 + 77 / 2 - rendered_heading.get_height() / 2)
        )

        if self.show_time:
            rendered_time = oxygen48.render(f"{datetime.now().time().strftime('%H:%M')} Uhr", True, Colors.BLACK)
            screen.blit(rendered_time, (
                1001 + (300 - rendered_time.get_width()) / 2, 13 + 77 / 2 - rendered_time.get_height() / 2))

        if self.on_back_button_press:
            rendered_back = oxygen36.render("Zurück", True, Colors.WHITE)
            pygame.draw.rect(screen, Colors.RED2, pygame.Rect(19, 11, 250, 70), border_radius=25)
            screen.blit(rendered_back,
                        (86 + (183 - rendered_back.get_width()) / 2, 5 + 82 / 2 - rendered_back.get_height() / 2))
            back_arrow = pygame.image.load(base_path / "back_arrow.png")
            pygame.draw.rect(screen, Colors.WHITE, pygame.Rect(24, 16, 63.5, 60), border_radius=30)
            screen.blit(back_arrow, pygame.Rect(24, 16, 63.5, 60))

    def process_events(self, events) -> NavigationEvent:
        if self.on_back_button_press:
            for event in events:
                if isinstance(event, ClickEvent):
                    if self.back_button.collides_with(event.x, event.y):
                        print("On Back Button Press!")
                        return self.on_back_button_press
        return NoAction()


class PayOverlay(Overlay):
    def __init__(
            self, context,
            on_pay_button_pressed: NavigationEvent,
            price_title: str = "Gesamtpreis", amount: int = 0,
    ):
        self.back_button = HitBox(19, 11, 250, 70)
        self.title = price_title
        self.amount = amount
        self.on_back_button_press = on_pay_button_pressed
        super(PayOverlay, self).__init__(context)

    def draw(self, delta_t: float) -> None:
        tmp_rendered_text = oxygen36.render("Gesamtpreis:", True, Colors.BLACK)
        self.context.screen.blit(tmp_rendered_text, (
            373 + (255 - tmp_rendered_text.get_width()) / 2, 709 + (58 - tmp_rendered_text.get_height()) / 2))

        tmp_rendered_text = oxygen64.render(f"{str(self.amount).zfill(3)[:-2]},{str(self.amount).zfill(3)[-2:]} €",
                                            True, Colors.BLACK)
        self.context.screen.blit(tmp_rendered_text, (628 + (279 - tmp_rendered_text.get_width()) / 2, 695))

        pygame.draw.rect(self.context.screen, Colors.GREEN2, pygame.Rect(900, 475, 110, 110), border_radius=60)
        tmp_rendered_text = oxygen96.render("+", True, Colors.WHITE)
        self.context.screen.blit(tmp_rendered_text, (
            900 + (110 - tmp_rendered_text.get_width()) / 2, 475 + (110 - tmp_rendered_text.get_height()) / 2))

        x, y = 966, 693
        pygame.draw.rect(self.context.screen, Colors.GREEN, pygame.Rect(x, y, 200, 90), border_radius=25)
        # self.hitboxes.append(
        #    Hitbox(x, y, 200, 90, lambda: self.draw_screen(8)))  # TODO: Different behaviour for recharging of FährCard
        tmp_r_txt = oxygen48.render("Zahlen", True, Colors.WHITE)
        self.context.screen.blit(tmp_r_txt,
                                 (x + (200 - tmp_r_txt.get_width()) / 2, y + (90 - tmp_r_txt.get_height()) / 2))

    def process_events(self, events) -> NavigationEvent:
        if self.on_back_button_press:
            for event in events:
                if isinstance(event, ClickEvent):
                    if self.back_button.collides_with(event.x, event.y):
                        return self.on_back_button_press
        return NoAction()
