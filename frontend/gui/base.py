from typing import Union, List
import pygame
from queue import Queue
from abc import ABC, abstractmethod
from enum import Enum


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

    class EventData(ABC):
        pass

    class NoAction(EventData):
        pass

    def __init__(self, event_data: EventData):
        self.event_data = event_data

    def __bool__(self):
        return type(self.event_data) != self.NoAction


class Drawable(ABC):
    @abstractmethod
    def tick(
            self, delta_t: float, events: List[Event], tasks: Queue, report_to: Queue,
            screen_config: ScreenConfig, screen: pygame.Surface, **kwargs
    ) -> NavigationEvent:
        pass


class DrawableConfig(ABC):
    """Base class for the configuration of a drawable object."""
    pass


class Overlay(Drawable):
    class Config(DrawableConfig):
        pass

    def tick(
            self, delta_t: float, events: List[Event], tasks: Queue, report_to: Queue,
            screen_config: ScreenConfig, screen: pygame.Surface, **kwargs
    ) -> NavigationEvent:
        pass


class Screen(Drawable):
    """Base class for a complete screen, that is drawn by calling its `tick` method.
    A screen can have custom configuration settings, therefore it has a configuration class.
    On a screen, there can be overlays, rendered in the order present.
    """

    class Config(DrawableConfig):
        pass

    def __init__(self, config: Config, overlays: List[Overlay], ):
        self.config = config
        self.overlays = overlays

    def tick(
            self, delta_t: float, events: List[Event], tasks: Queue, report_to: Queue,
            screen_config: ScreenConfig, screen: pygame.Surface, **kwargs
    ) -> NavigationEvent:
        pass


class Menu(Drawable):
    """A menu is a collection of screens"""

    class Config(DrawableConfig):
        pass

    def __init__(self, context, entry_point: Screen = None, screens: List[Screen] = None):
        super(Menu, self).__init__()
        self.entry_point: Union[None, Screen] = entry_point
        self.screens: Union[None, List[Screen]] = screens
        self.context = context

    def tick(
            self, delta_t: float, events: List[Event], tasks: Queue, report_to: Queue,
            screen_config: ScreenConfig, screen: pygame.Surface, **kwargs
    ) -> NavigationEvent:
        pass


class HitBox:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def collides_with(self, x, y):
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height
