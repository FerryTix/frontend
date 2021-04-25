from typing import Union, List
from queue import Queue
from abc import ABC, abstractmethod
from enum import Enum
import pygame


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
    def __init__(
            self, width: int = 1280, height: int = 800,
            display_rotation: Rotation = Rotation.R0,
            touchscreen_rotation: Rotation = Rotation.R0,
            fullscreen: bool = True
    ):
        self.WIDTH = width
        self.HEIGHT = height
        self.DISPLAY_ROTATION = display_rotation
        self.TOUCHSCREEN_ROTATION = touchscreen_rotation
        self.FULLSCREEN = fullscreen


class Event(ABC):
    pass


class ClickEvent(Event):
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.pos = x, y


class NavigationEvent(Event):
    """Base class for all events that can change the state of the current menu, or
    introduce a switch to another menu."""

    def __bool__(self):
        return True


class NoAction(NavigationEvent):
    def __bool__(self):
        return False


class Drawable(ABC):
    @abstractmethod
    def draw(self, delta_t: float, events: List[Event], tasks: Queue, report_to: Queue, **kwargs) -> None:
        return

    @abstractmethod
    def process_events(self, events) -> NavigationEvent:
        return NoAction()

    @abstractmethod
    def tick(self, redraw: bool, delta_t: float, events: List[Event], tasks: Queue, report_to: Queue,
             **kwargs) -> NavigationEvent:
        pass


class Overlay(Drawable):
    def __init__(self, context):
        self.context = context

    def draw(self, delta_t: float, events: List[Event], tasks: Queue, report_to: Queue, **kwargs) -> None:
        return

    def process_events(self, events) -> NavigationEvent:
        return NoAction()

    def tick(self, redraw: bool, delta_t: float, events: List[Event], tasks: Queue, report_to: Queue,
             **kwargs) -> NavigationEvent:
        if redraw:
            self.draw(delta_t, events, tasks, report_to, **kwargs)
        return self.process_events(events)


class Screen(Drawable):
    """
    Base class for a complete screen, that is drawn by calling its `tick` method.
    A screen can have custom configuration settings, therefore it has a configuration class.
    On a screen, there can be overlays, rendered in the order present.
    """

    def __init__(self, context, overlays: List[Overlay]):
        self.overlays = overlays
        self.context = context

    def draw_overlays(self, delta_t: float, events: List[Event], tasks: Queue, report_to: Queue,
                      **kwargs) -> NavigationEvent:
        overlay_events = []
        for overlay in self.overlays:
            event = overlay.tick(True, delta_t, events, tasks, report_to, **kwargs)
            if event:
                overlay_events.append(event)
        if overlay_events:
            # return only one event, as to match signature.
            # there is no way to determine which event happened first, so this is a viable approach
            return overlay_events[0]
        return NoAction()

    def draw(self, delta_t: float, events: List[Event], tasks: Queue, report_to: Queue, **kwargs) -> None:
        return

    def process_events(self, events) -> NavigationEvent:
        return NoAction()

    def tick(self, redraw: bool, delta_t: float, events: List[Event], tasks: Queue, report_to: Queue,
             **kwargs) -> NavigationEvent:
        if redraw:
            self.draw(delta_t, events, tasks, report_to, **kwargs)
        screen_event = self.process_events(events=events)
        overlay_event = self.draw_overlays(delta_t, events, tasks, report_to, **kwargs)
        if screen_event:
            return screen_event
        if overlay_event:
            return overlay_event
        return NoAction()


class Menu(Drawable):
    """A menu is a collection of screens"""

    def __init__(self, context, entry_point: Screen = None, screens: List[Screen] = None):
        self.entry_point: Union[None, Screen] = entry_point
        self.current_screen = self.entry_point
        self.screens: Union[None, List[Screen]] = screens
        self.context = context

    def draw(self, delta_t: float, events: List[Event], tasks: Queue, report_to: Queue, **kwargs) -> None:
        pass

    def process_events(self, events) -> NavigationEvent:
        return events

    def tick(self, redraw: bool, delta_t: float, events: List[Event], tasks: Queue, report_to: Queue,
             **kwargs) -> NavigationEvent:
        result = self.current_screen.tick(redraw, delta_t, events, tasks, report_to, **kwargs)
        if redraw:
            pygame.display.flip()
        if result:
            return self.process_events(result)
        return NoAction()


class HitBox:
    """Basis for buttons"""

    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def collides_with(self, x, y):
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height


class RootNavigationEvent(NavigationEvent):
    pass


class SwitchMenu(RootNavigationEvent):
    def __init__(self, target: Menu):
        """
        Event resembling a switch to a target menu.
        """
        self.target = target


class ReturnHome(RootNavigationEvent):
    """Event resembling a return to the home screen, which is the MainMenu."""
    pass


class RequireDraw(RootNavigationEvent):
    """Event to signal, that a redraw of the canvas is necessary."""
    pass


class MenuNavigationEvent(NavigationEvent):
    pass


class PreviousScreen(MenuNavigationEvent):
    pass


class SwitchScreen(MenuNavigationEvent):
    def __init__(self, target: Screen):
        self.target = target
