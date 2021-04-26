from typing import List
from . import Screen, Menu, NavigationEvent, ReturnHome, NavigationOverlay, Overlay, NoAction, \
    MenuNavigationEvent, HitBox, ClickEvent, PayOverlay, SwitchMenu, RequireDraw
from .payment_menu import PaymentMenu, ECCard, Cash, FaehrCard
from .colors import Colors
from .constants import *
from .ticket_classes import ticket_prices, TicketClassNames
from .tools import format_amount


class ReturnTicketCheckBox(Overlay):
    class CheckBoxTrigger(MenuNavigationEvent):
        def __init__(self, checked):
            self.checked = checked

    def __init__(self, context):
        self.screen = context.screen
        self.button_hb = HitBox(x=19, y=700, width=250, height=70)
        self.checked = True
        super(ReturnTicketCheckBox, self).__init__(context)

    def draw(self, delta_t: float) -> None:
        pygame.draw.rect(self.screen, Colors.BLACK, pygame.Rect(0, 675, self.context.screen_config.WIDTH, 1))

        pygame.draw.rect(self.screen, Colors.BLUE, pygame.Rect(19, 703, 324, 70), border_radius=25)
        tmp_rendered_text = oxygen36.render("Rückfahrt:", True, Colors.WHITE)
        self.context.screen.blit(tmp_rendered_text, (
            19 + (250 - tmp_rendered_text.get_width()) / 2, 703 + (70 - tmp_rendered_text.get_height()) / 2))
        tmp_image = pygame.image.load(base_path / "checkmark_solid.png")
        self.context.screen.blit(tmp_image, pygame.Rect(19 + 260, 703 + 5, 60, 60))

    def process_events(self, events) -> NavigationEvent:
        for evt in events:
            if isinstance(evt, ClickEvent):
                if self.button_hb.collides_with(evt.x, evt.y):
                    self.checked = not self.checked
                    return ReturnTicketCheckBox.CheckBoxTrigger(checked=self.checked)
        return NoAction()


class TicketPositionWidget(Overlay):
    widget_coordinates = [(50, 130), (680, 130), (50, 400), (680, 400)]
    all_ticket_classes: List[TicketClassNames] = [
        TicketClassNames.adult_bike,
        TicketClassNames.adult_passenger,
        TicketClassNames.child_bike,
        TicketClassNames.child_passenger,
        TicketClassNames.reduced_bike,
        TicketClassNames.reduced_passenger,
    ]

    class NextTicketClass(MenuNavigationEvent):
        pass

    class PreviousTicketClass(MenuNavigationEvent):
        pass

    def __init__(self, context, index, ticket_class: TicketClassNames, ticket_count: int, return_ticket=False):
        self.x, self.y = TicketPositionWidget.widget_coordinates[index]
        self._index = index
        self.return_ticket = return_ticket
        self.ticket_class = ticket_class
        self.screen = context.screen
        self.ticket_count = ticket_count
        self.previous_item_hb = HitBox(x=self.x + 108, y=self.y + 25, width=36, height=36)
        self.next_item_hb = HitBox(x=self.x + 550 - 78 - 36, y=self.y + 25, width=36, height=36)
        # TODO: self.close_button = HitBox(x=0, y=0, width=0, height=0)
        super(TicketPositionWidget, self).__init__(context)

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, i: int):
        self._index = i
        self.x, self.y = TicketPositionWidget.widget_coordinates[i]
        self.previous_item_hb = HitBox(x=self.x + 108, y=self.y + 25, width=36, height=36)
        self.next_item_hb = HitBox(x=self.x + 550 - 78 - 36, y=self.y + 25, width=36, height=36)
        # TODO: self.close_button = HitBox(x=0, y=0, width=0, height=0)

    def draw(self, delta_t: float) -> None:
        x, y = self.x, self.y
        ticket_price = ticket_prices[self.ticket_class][
            TicketClassNames.return_fare if self.return_ticket else TicketClassNames.single_fare
        ]
        heading = ticket_prices[self.ticket_class][TicketClassNames.title]
        bicycle_strikethrough = not ticket_prices[self.ticket_class][TicketClassNames.bike]
        text_count = str(self.ticket_count)

        text_price_per_unit = format_amount(ticket_price)
        text_result = format_amount(self.ticket_count * ticket_price)

        pygame.draw.rect(self.screen, Colors.GRAY2, pygame.Rect(x, y, 550, 250), border_radius=15)
        tmp_image = pygame.image.load(base_path / "small_back_arrow.png")
        self.screen.blit(tmp_image, pygame.Rect(x + 108, y + 25, 36, 36))
        tmp_r_txt = oxygen48.render(heading, True, Colors.BLACK)
        self.screen.blit(tmp_r_txt, (x + 290 - tmp_r_txt.get_width() / 2, y + 12))
        tmp_image = pygame.image.load(base_path / "small_forward_arrow.png")
        self.screen.blit(tmp_image, pygame.Rect(x + 550 - 78 - 36, y + 25, 36, 36))
        pygame.draw.rect(self.screen, Colors.BLACK, pygame.Rect(x, y + 92, 551, 1))
        tmp_image = pygame.image.load(base_path / "🚲.png")
        self.screen.blit(tmp_image, pygame.Rect(x + 251, y + 109 - 34, 77, 37))
        pygame.draw.rect(self.screen, Colors.BLACK, pygame.Rect(x, y + 182, 551, 1))
        if bicycle_strikethrough is True:
            tmp_image = pygame.image.load(base_path / "bicycle_strikethrough.png")
            self.screen.blit(tmp_image, pygame.Rect(x + 250, y + 131 - 34, 88, 88))
        tmp_r_txt = oxygen64.render("-", True, Colors.BLACK)
        self.screen.blit(tmp_r_txt,
                         (x + 26 + (69 - tmp_r_txt.get_width()) / 2, y + 165 + (93 - tmp_r_txt.get_height()) / 2))
        pygame.draw.rect(self.screen, Colors.WHITE, pygame.Rect(x + 84, y + 186, 66, 51), border_radius=25)
        tmp_r_txt = oxygen48.render(text_count, True, Colors.BLACK)
        self.screen.blit(tmp_r_txt,
                         (x + 84 + (66 - tmp_r_txt.get_width()) / 2, y + 186 + (51 - tmp_r_txt.get_height()) / 2))
        tmp_r_txt = oxygen64.render("+", True, Colors.BLACK)
        self.screen.blit(tmp_r_txt,
                         (x + 141 + (69 - tmp_r_txt.get_width()) / 2, y + 169 + (86 - tmp_r_txt.get_height()) / 2))
        tmp_r_txt = oxygen36.render(text_price_per_unit, True, Colors.BLACK)
        self.screen.blit(tmp_r_txt, (x + 293 - tmp_r_txt.get_width() / 2, y + 186))
        tmp_r_txt = oxygen36.render(text_result, True, Colors.BLACK)
        self.screen.blit(tmp_r_txt, (x + 454 - tmp_r_txt.get_width() / 2, y + 186))

    def process_events(self, events) -> NavigationEvent:
        for evt in events:
            if isinstance(evt, ClickEvent):
                if self.previous_item_hb.collides_with(evt.x, evt.y):
                    return TicketPositionWidget.PreviousTicketClass()
                if self.next_item_hb.collides_with(evt.x, evt.y):
                    return TicketPositionWidget.NextTicketClass()

        return NoAction()


class BuyTicketScreen(Screen):
    def __init__(self, context, payment_menu: PaymentMenu, vending_status: bool = True):
        self.vending_status = vending_status
        self.return_ticket = True
        self.payment_menu = payment_menu
        self.positions = [
            TicketPositionWidget(
                context=context,
                ticket_class=TicketClassNames.adult_bike,
                ticket_count=2,
                return_ticket=True,
                index=0,
            )
        ]
        super(BuyTicketScreen, self).__init__(context=context, overlays=[
            PayOverlay(
                context=context, on_pay_button_pressed=SwitchMenu(target=self.payment_menu),
                amount=self.calculate_sum(),
            ),
            NavigationOverlay(context=context, title="Tickets kaufen"),
            ReturnTicketCheckBox(
                context=context,
            ),
        ])

    def calculate_sum(self):
        return sum(x.ticket_count * ticket_prices[x.ticket_class][
            TicketClassNames.return_fare if self.return_ticket else TicketClassNames.single_fare
        ] for x in self.positions)

    def recalculate_amount(self):
        for ovl in self.overlays:
            if isinstance(ovl, PayOverlay):
                ovl.amount = self.calculate_sum()

    def draw(self, delta_t: float) -> None:
        self.context.screen.fill(color=Colors.BACKGROUND)

        for position in self.positions:
            position.draw(delta_t)
        for ovl in self.overlays:
            ovl.draw(delta_t)

    def process_events(self, events) -> NavigationEvent:
        for ovl in self.overlays:
            evt = ovl.process_events(events)
            if evt:
                return evt

        widget_events = []

        for position in self.positions:
            evt = position.process_events(events)
            if evt:
                widget_events.append((evt, position))

        for evt, position in widget_events:
            if type(evt) in [TicketPositionWidget.NextTicketClass, TicketPositionWidget.PreviousTicketClass]:
                # TODO: make sense
                available_classes = [
                    x for x in TicketPositionWidget.all_ticket_classes
                    if x not in [p.ticket_class for p in self.positions if p is not position]
                ]
                idx = available_classes.index(position.ticket_class)

                if isinstance(evt, TicketPositionWidget.PreviousTicketClass):
                    position.ticket_class = available_classes[(idx - 1)]
                    self.recalculate_amount()
                    return RequireDraw()
                if isinstance(evt, TicketPositionWidget.NextTicketClass):
                    position.ticket_class = available_classes[(idx + 1) % len(available_classes)]
                    self.recalculate_amount()
                    return RequireDraw()

    def process_overlay_events(self, overlay_events: List[NavigationEvent]) -> NavigationEvent:
        for evt in overlay_events:
            if evt:
                return evt
        return NoAction()


class BuyTicketMenu(Menu):
    def __init__(self, context):
        self.payment_menu = PaymentMenu(
            context,
            on_exit=self,
            accepted_payment_methods=[
                FaehrCard,
                # ECCard,
                Cash
            ]
        )

        self.buy_ticket_screen = BuyTicketScreen(context=context, payment_menu=self.payment_menu)

        super(BuyTicketMenu, self).__init__(
            entry_point=self.buy_ticket_screen,
            screens=[self.buy_ticket_screen],
            context=context,
        )

    def process_screen_events(self, events) -> NavigationEvent:
        for evt in events:
            if evt:
                if isinstance(evt, ReturnHome):
                    return evt
                elif isinstance(evt, RequireDraw):
                    return evt
                elif isinstance(evt, SwitchMenu):
                    if evt.target == self.payment_menu:
                        self.payment_menu.amount = self.buy_ticket_screen.calculate_sum()
                        return evt
                    else:
                        raise NotImplementedError()
                else:
                    # unhandled event
                    raise NotImplementedError()
        return NoAction()
