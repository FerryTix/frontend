from .base import Overlay, Screen, NavigationEvent, Event, Menu
from typing import List, Union
from abc import ABC


class NavigationOverlay(Overlay):
    class Config:
        def __init__(self, title: str, on_back_button_press: Screen, on_success: Screen):
            self.title = title
            self.on_back_button_press = on_back_button_press
            self.on_success = on_success

    def __init__(self, config):
        super(NavigationOverlay, self).__init__(config=config)

    def tick(self, delta_t: float, events: List[Event], **kwargs) -> Union[None, NavigationEvent]:
        return None


class RootNavigationEvent(NavigationEvent):
    class EventData(ABC):
        pass

    class SwitchMenu(EventData):
        def __init__(self, target: Menu):
            self.target = target

    class ReturnHome(EventData):
        pass

    def __init__(self, event_data: EventData):
        super(RootNavigationEvent, self).__init__(event_data)


class MenuNavigationEvent(NavigationEvent):
    class EventData(ABC):
        pass

    class PreviousScreen(EventData):
        pass

    class SwitchScreen(EventData):
        def __init__(self, target: Screen):
            pass

    def __init__(self, event_data: EventData):
        super(MenuNavigationEvent, self).__init__(event_data)
