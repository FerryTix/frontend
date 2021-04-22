from typing import Union, List, Dict
from abc import ABC, abstractmethod


class Drawable(ABC):
    @abstractmethod
    def tick(self, delta_t: float, **kwargs):
        pass


class DrawableConfig(ABC):
    """Base class for the configuration of a drawable object."""
    pass


class NavigationEvent(ABC):
    """Base class for all events that can change the state of the current menu, or
    introduce a switch to another menu."""
    pass


class Overlay(Drawable, ABC):
    class Config(DrawableConfig):
        pass

    def tick(self, delta_t: float, **kwargs):
        pass


class Screen(ABC, Drawable):
    """Base class for a complete screen, that is drawn by calling its `tick` method.
    A screen can have custom configuration settings, therefore it has a configuration class.
    On a screen, there can be overlays, rendered in the order present.
    """

    def __init__(self, overlays=List[Overlay]):
        self.overlays = overlays

    class Config(DrawableConfig):
        pass

    def tick(self, delta_t: float, **kwargs):
        pass


class Menu(Drawable, ABC):
    """A menu is a collection of screens"""

    class Config(DrawableConfig):
        pass

    def __init__(self, entry_point: Screen, screens: List[Screen]):
        super(Menu, self).__init__()
        self.entry_point: Union[None, Screen] = entry_point
        self.screens: Union[None, List[Screen]] = screens

    def tick(self, delta_t: float, event: NavigationEvent, **kwargs):
        pass


class NavigationOverlay(Overlay):
    class Config:
        def __init__(self, title: str, on_back_button_press: Screen, on_success: Screen):
            self.title = title
            self.on_back_button_press = on_back_button_press
            self.on_success = on_success

    def __init__(self, config):
        super(NavigationOverlay, self).__init__(config=config)

    def tick(self, delta_t: float, **kwargs):
        return self, None
