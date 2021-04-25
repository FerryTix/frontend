from typing import Union, List
from queue import Queue
from abc import ABC, abstractmethod
from enum import Enum
import pygame
from .colors import Colors


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
    def draw(self, delta_t: float) -> None:
        return

    @abstractmethod
    def process_events(self, events) -> NavigationEvent:
        return NoAction()


class Overlay(Drawable):
    def __init__(self, context):
        self.context = context

    def draw(self, delta_t: float) -> None:
        return

    def process_events(self, events) -> NavigationEvent:
        return NoAction()


class Screen(Drawable):
    """
    Base class for a complete screen, that is drawn by calling its `tick` method.
    A screen can have custom configuration settings, therefore it has a configuration class.
    On a screen, there can be overlays, rendered in the order present.
    """

    def __init__(self, context, overlays: List[Overlay]):
        self.overlays = overlays
        self.context = context

    def draw_overlays(self, delta_t: float) -> None:
        for overlay in self.overlays:
            overlay.draw(delta_t)

    def process_events(self, events) -> NavigationEvent:
        overlay_events = [x for x in [ovl.process_events(events) for ovl in self.overlays] if x]
        if overlay_events:
            return self.process_overlay_events(overlay_events)
        return NoAction()

    @abstractmethod
    def draw(self, delta_t: float) -> None:
        pass

    @abstractmethod
    def process_overlay_events(self, overlay_events: List[NavigationEvent]) -> NavigationEvent:
        return NoAction()


class Menu(Drawable):
    """A menu is a collection of screens"""

    def __init__(self, context, entry_point: Screen = None, screens: List[Screen] = None):
        self.entry_point: Union[None, Screen] = entry_point
        self.current_screen = self.entry_point
        self.screens: Union[None, List[Screen]] = screens
        self.context = context

    def draw(self, delta_t: float) -> None:
        self.context.screen.fill(color=Colors.BACKGROUND)
        self.current_screen.draw(delta_t)
        pygame.display.flip()

    def process_events(self, events) -> NavigationEvent:
        return NoAction()

    def tick(self, redraw: bool, delta_t: float, events: List[Event]) -> NavigationEvent:
        if redraw:
            self.draw(delta_t)
        screen_event = self.current_screen.process_events(events)
        if screen_event:
            return self.process_screen_events(events=[screen_event])
        return NoAction()

    @abstractmethod
    def process_screen_events(self, events) -> NavigationEvent:
        pass

    def enter(self):
        pass

    def exit(self):
        pass


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
