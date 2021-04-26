from typing import List
from .constants import *
from .colors import Colors
from receipt_generator import ReceiptPrinter, Receipt
from . import Screen, Overlay, Menu, NavigationEvent, SwitchMenu, NoAction, RequireDraw, SwitchScreen, HitBox, \
    ClickEvent
from .shared import NavigationOverlay
from .tools import format_amount


class PaymentMethod:
    title = None
    icon = None
    width = None


class ECCard(PaymentMethod):
    title = 'EC-karte'
    icon = base_path / "contactless_card.png"
    width = 194


class Cash(PaymentMethod):
    title = 'Bargeld'
    icon = base_path / "jesus_holding_cash.png"
    width = 240


class FaehrCard(PaymentMethod):
    title = 'FährCard™'
    icon = base_path / "electronic_cash_logo.png"
    width = 188


class BookingConfirmation(Screen):
    def __init__(self, context, cheese):
        self.cheese = cheese
        self.amount = None
        super(BookingConfirmation, self).__init__(context, overlays=[
            NavigationOverlay(context, title="Zahlung erfolgreich", on_back_button_press=NoAction()),
        ])

    def draw(self, delta_t: float) -> None:
        pass

    def process_overlay_events(self, overlay_events: List[NavigationEvent]) -> NavigationEvent:
        return NoAction()

    def process_events(self, events) -> NavigationEvent:
        return RequireDraw()


class PaymentMethodOverlay(Overlay):
    def __init__(self, context, method: PaymentMethod,
                 x, y):
        self.x, self.y = x, y
        self.method = method
        self.img = pygame.image.load(self.method.icon)
        self.button_hb = HitBox(self.x, self.y, 375, 418)
        self.button_action = SwitchScreen(
            target={
                ECCard: ECCardPayment(context, overlays=[]),
                Cash: CashPayment(context, overlays=[]),
                FaehrCard: FaehrCardPayment(context, overlays=[]),
            }[self.method]
        )
        super(PaymentMethodOverlay, self).__init__(context)

    def draw(self, delta_t: float) -> None:
        pygame.draw.rect(self.context.screen, Colors.GRAY2, pygame.Rect(self.x, self.y, 375, 418),
                         border_radius=15)
        tmp_r_txt = oxygen64.render(self.method.title, True, Colors.BLACK)
        self.context.screen.blit(tmp_r_txt, (self.x + 188 - tmp_r_txt.get_width() / 2, self.y + 32))
        tmp_img = self.img
        img_width = img_height = self.method.width
        self.context.screen.blit(
            tmp_img, pygame.Rect(self.x + 188 - img_width / 2, self.y + 251 - img_height / 2, img_width, img_height)
        )

        pygame.display.flip()

    def process_events(self, events) -> NavigationEvent:
        for evt in events:
            if isinstance(evt, ClickEvent):
                if self.button_hb.collides_with(evt.x, evt.y):
                    return self.button_action


class ChoosePaymentMethod(Screen):
    def __init__(self, context, on_exit, offered_payment_methods: List[type]):
        self.offered_payment_methods = offered_payment_methods
        self.on_exit = on_exit
        self.amount = None

        widget_positions = []

        n = len(self.offered_payment_methods)
        d0 = 25
        d = (1280 - 2 * d0 - (n * 375)) / (n + 1)

        for x in range(n):
            widget_positions.append((d0 + d + x * (d + 375), 190))

        super(ChoosePaymentMethod, self).__init__(context, overlays=[
            NavigationOverlay(
                context, title="Zahlungsmittel wählen",
                on_back_button_press=SwitchMenu(target=self.on_exit),
            ),
            *[
                PaymentMethodOverlay(context, pm, x, y) for pm, (x, y) in
                zip(self.offered_payment_methods, widget_positions)
            ],
        ])

    def draw(self, delta_t: float) -> None:
        for ovl in self.overlays:
            ovl.draw(delta_t)

        pygame.draw.rect(self.context.screen, Colors.BLACK, pygame.Rect(0, 675, self.context.screen_config.WIDTH, 1))

        tmp_rendered_text = oxygen36.render("Betrag:", True, Colors.BLACK)
        self.context.screen.blit(tmp_rendered_text, (
            373 + (255 - tmp_rendered_text.get_width()) / 2, 709 + (58 - tmp_rendered_text.get_height()) / 2))

        tmp_rendered_text = oxygen64.render(format_amount(self.amount), True, Colors.BLACK)
        self.context.screen.blit(tmp_rendered_text, (628 + (279 - tmp_rendered_text.get_width()) / 2, 695))

    def process_overlay_events(self, overlay_events: List[NavigationEvent]) -> NavigationEvent:
        for evt in overlay_events:
            if evt:
                return evt
        return NoAction()


class FaehrCardPayment(Screen):
    def draw(self, delta_t: float) -> None:
        # TODO: implement
        raise NotImplementedError()

    def process_overlay_events(self, overlay_events: List[NavigationEvent]) -> NavigationEvent:
        for evt in overlay_events:
            if evt:
                return evt
        return NoAction()


class CashPayment(Screen):
    def draw(self, delta_t: float) -> None:
        # TODO: implement
        raise NotImplementedError()

    def process_overlay_events(self, overlay_events: List[NavigationEvent]) -> NavigationEvent:
        pass


class ECCardPayment(Screen):
    def draw(self, delta_t: float) -> None:
        # TODO: implement
        raise NotImplementedError()

    def process_overlay_events(self, overlay_events: List[NavigationEvent]) -> NavigationEvent:
        pass


class PaymentMenu(Menu):
    def __init__(
            self, context,
            on_exit: Menu,
            accepted_payment_methods: List[type] = (
                    ECCard,
                    Cash,
                    FaehrCard,
            ),
            cheese: bool = True,
    ):
        self.cheese = cheese
        self.accepted_payment_methods = accepted_payment_methods
        self.on_exit = on_exit
        self.amount = None

        self.choose_payment_method_screen = ChoosePaymentMethod(
            context,
            self.on_exit,
            self.accepted_payment_methods,
        )
        self.booking_confirmation_screen = BookingConfirmation(
            context,
            cheese,
        )

        super(PaymentMenu, self).__init__(
            context,
            entry_point=self.choose_payment_method_screen,
            screens=[self.choose_payment_method_screen, self.booking_confirmation_screen],
        )

    def process_screen_events(self, events) -> NavigationEvent:
        for evt in events:
            if isinstance(evt, SwitchMenu):
                return evt
            elif isinstance(evt, SwitchScreen):
                self.current_screen = evt.target
                return RequireDraw()
        return NoAction()

    def enter(self, **kwargs):
        self.booking_confirmation_screen.amount = self.amount
        self.choose_payment_method_screen.amount = self.amount
