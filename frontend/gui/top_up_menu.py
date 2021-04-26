from typing import List
from .constants import *
from .colors import Colors
from . import Screen, Overlay, Menu, HitBox, NavigationOverlay, ReturnHome, NoAction, Event, NavigationEvent
from .payment_menu import PaymentMenu, ECCard, Cash


class ShowFaehrCardInfo(Screen):
    def __init__(self, context):
        super(ShowFaehrCardInfo, self).__init__(context, overlays=[
            NavigationOverlay(context, title="FährCard™")
        ])

    def draw(self, delta_t: float) -> None:
        self.context.screen.fill(color=Colors.BACKGROUND)

        pygame.draw.rect(self.context.screen, Colors.GRAY2, pygame.Rect(50, 130, 590, 500), border_radius=15)
        tmp_rendered_text = oxygen36.render("Informationen zu Ihrer FährCard", True, Colors.BLACK)
        self.context.screen.blit(tmp_rendered_text, (50 + (590 - tmp_rendered_text.get_width()) / 2, 130 + 26))
        pygame.draw.rect(self.context.screen, Colors.BLACK, pygame.Rect(50, 217, 590, 1))
        tmp_rendered_text = oxygen24.render("Kartennummer", True, Colors.BLACK)
        self.context.screen.blit(tmp_rendered_text, (50 + 37, 130 + 105))
        tmp_rendered_text = oxygen24.render("3e8d***************f81c", True, Colors.BLACK)
        self.context.screen.blit(tmp_rendered_text, (50 + 590 - 41 - tmp_rendered_text.get_width(), 130 + 105))
        tmp_rendered_text = oxygen36.render("Ausgabedatum", True, Colors.BLACK)
        self.context.screen.blit(tmp_rendered_text, (50 + 34, 130 + 151))
        tmp_rendered_text = oxygen36.render("12.07.2021", True, Colors.BLACK)
        self.context.screen.blit(tmp_rendered_text, (50 + 590 - 41 - tmp_rendered_text.get_width(), 130 + 151))
        tmp_rendered_text = oxygen36.render("Letzte Aufladung", True, Colors.BLACK)
        self.context.screen.blit(tmp_rendered_text, (50 + 34, 130 + 215))
        tmp_rendered_text = oxygen36.render("24.07.2021", True, Colors.BLACK)
        self.context.screen.blit(tmp_rendered_text, (50 + 590 - 41 - tmp_rendered_text.get_width(), 130 + 215))
        tmp_rendered_text = oxygen36.render("Inhaber", True, Colors.BLACK)
        self.context.screen.blit(tmp_rendered_text, (50 + 34, 130 + 276))
        tmp_rendered_text = oxygen36.render("Leon Pascal", True, Colors.BLACK)
        self.context.screen.blit(tmp_rendered_text, (50 + 590 - 41 - tmp_rendered_text.get_width(), 130 + 276))
        tmp_rendered_text = oxygen36.render("Thierschmidt", True, Colors.BLACK)
        self.context.screen.blit(tmp_rendered_text,
                                 (50 + 590 - 41 - tmp_rendered_text.get_width(), 130 + 276 + oxygen36.get_linesize()))
        tmp_image = pygame.image.load(base_path / "tilted_heart.png")
        self.context.screen.blit(tmp_image, pygame.Rect(146, 337, 347, 314))
        tmp_image = pygame.image.load(base_path / "tilted_employee_text.png")
        self.context.screen.blit(tmp_image, pygame.Rect(259, 437, 119, 105))
        tmp_rendered_text = oxygen36.render("Guthaben:", True, Colors.BLACK)
        self.context.screen.blit(tmp_rendered_text, (50 + 35, 130 + 411))
        tmp_rendered_text = oxygen64.render("5,00 €", True, Colors.BLACK)
        self.context.screen.blit(tmp_rendered_text, (50 + 590 - 41 - tmp_rendered_text.get_width(), 130 + 393))

        tmp_rendered_text = oxygen36.render("Auflade-Optionen", True, Colors.BLACK)
        self.context.screen.blit(tmp_rendered_text, (682, 130))
        # self.draw_add_balance_button(671, 197, "5,00 €", Colors.BLACK)
        # self.draw_add_balance_button(671, 310, "10,00 €", Colors.BLACK)
        # self.draw_add_balance_button(671, 423, "20,00 €", Colors.GREEN2)
        # self.draw_add_balance_button(671, 536, "50,00 €", Colors.GREEN)

        tmp_rendered_text = oxygen36.render("Bonus", True, Colors.BLACK)
        self.context.screen.blit(tmp_rendered_text, (1102, 132))
        # self.draw_bonus_display(1075, 207, "0,00 €", Colors.GRAY3)
        # self.draw_bonus_display(1075, 320, "0,50 €", Colors.BLACK)
        # self.draw_bonus_display(1075, 433, "2,00 €", Colors.GREEN2)
        # self.draw_bonus_display(1075, 546, "10,00 €", Colors.GREEN)

        pygame.draw.rect(self.context.screen, Colors.BLACK,
                         pygame.Rect(0, 675, self.context.screen_config.WIDTH, 1))
        tmp_rendered_text = oxygen36.render("Gesamtpreis:", True, Colors.BLACK)
        self.context.screen.blit(tmp_rendered_text, (
            373 + (255 - tmp_rendered_text.get_width()) / 2, 709 + (58 - tmp_rendered_text.get_height()) / 2))
        tmp_rendered_text = oxygen64.render("50,00 €", True, Colors.BLACK)
        self.context.screen.blit(tmp_rendered_text, (
            628 + (279 - tmp_rendered_text.get_width()) / 2, 709 + (58 - tmp_rendered_text.get_height()) / 2))
        # self.draw_payment_button(966, 693)

        self.draw_overlays(delta_t)

    def process_overlay_events(self, overlay_events: List[NavigationEvent]) -> NavigationEvent:
        for evt in overlay_events:
            if evt:
                return evt
        return NoAction()


class ScanFaehrCard(Screen):
    def __init__(self, context):
        self.contactless_payment = pygame.image.load(base_path / "contactless_payment.png")
        self.info = oxygen48.render("Bitte halten Sie Ihre FährCard an den NFC-Leser.", True, Colors.BLACK)

        super(ScanFaehrCard, self).__init__(context, overlays=[
            NavigationOverlay(context, title="FährCard™")
        ])

    def draw(self, delta_t: float) -> None:
        pygame.draw.rect(self.context.screen, Colors.GRAY2, pygame.Rect(50, 130, 1180, 621), border_radius=15)

        # looks like this was used for debugging purposes
        # self.hitboxes.append(HitBox(50, 130, 1180, 621, lambda: self.draw_screen(2)))

        self.context.screen.blit(self.info, (50 + (1180 - self.info.get_width()) / 2, 171))

        self.context.screen.blit(self.contactless_payment, pygame.Rect(257, 273, 766, 375))

        text = oxygen36.render("NFC-Leser aktiv… ⌛", True, Colors.BLACK)
        self.context.screen.blit(text, (50 + (1180 - text.get_width()) / 2, 649))

        self.draw_overlays(delta_t)

    def process_overlay_events(self, overlay_events: List[NavigationEvent]) -> NavigationEvent:
        for evt in overlay_events:
            if evt:
                return evt
        return NoAction()


class TopUpMenu(Menu):
    def __init__(self, context):
        self.scan_faehr_card_screen = ScanFaehrCard(context)
        self.show_faehr_card_info_screen = ShowFaehrCardInfo(context)
        self.payment_menu = PaymentMenu(
            context, on_exit=self, accepted_payment_methods=[
                ECCard, Cash,
            ],
            cheese=False,
        )
        super(TopUpMenu, self).__init__(
            context,
            entry_point=self.scan_faehr_card_screen,
            screens=[self.scan_faehr_card_screen, self.show_faehr_card_info_screen]
        )

    def process_screen_events(self, events) -> NavigationEvent:
        for evt in events:
            if evt:
                if isinstance(evt, ReturnHome):
                    return evt
                else:
                    # unhandled event
                    raise NotImplementedError()
        return NoAction()
