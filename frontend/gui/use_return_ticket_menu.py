from typing import List
from . import Screen, Menu, NavigationEvent, NavigationOverlay, HitBox, ReturnHome, NoAction, \
    RequireDraw
from .constants import *
from .colors import Colors
import pygame
import cv2
from pyzbar import pyzbar


class QRCodeRead(NavigationEvent):
    def __init__(self, code):
        self.code = code


class ScanQRCode(Screen):
    def __init__(self, context):
        self.detector = cv2.QRCodeDetector()
        self.capture = None
        super(ScanQRCode, self).__init__(context, overlays=[
            NavigationOverlay(context, title="Rückfahrt einlösen"),
        ])

    def draw(self, delta_t: float) -> None:
        self.context.screen.fill(color=Colors.BACKGROUND)
        tmp_image = pygame.image.load(base_path / "barcode_scanner.png")
        self.context.screen.blit(tmp_image, pygame.Rect(0, 277, 706, 372))
        # self.hitboxes.append(HitBox(0, 277, 706, 372, lambda: self.draw_screen(4)))

        tmp_rendered_text = oxygen48.render("Bitte halten Sie Ihr Ticket mit QR-Code", True, Colors.BLACK)
        self.context.screen.blit(tmp_rendered_text,
                                 ((self.context.screen_config.WIDTH - tmp_rendered_text.get_width()) / 2, 121))

        tmp_rendered_text = oxygen48.render("vor die Kamera, mit einem Abstand von", True, Colors.BLACK)
        self.context.screen.blit(tmp_rendered_text,
                                 ((self.context.screen_config.WIDTH - tmp_rendered_text.get_width()) / 2,
                                  121 + oxygen48.get_linesize()))
        tmp_rendered_text = oxygen48.render("circa 20 cm.", True, Colors.BLACK)
        self.context.screen.blit(tmp_rendered_text,
                                 ((self.context.screen_config.WIDTH - tmp_rendered_text.get_width()) / 2,
                                  121 + 2 * oxygen48.get_linesize()))

        pygame.draw.rect(self.context.screen, Colors.GRAY2, pygame.Rect(758, 313, 423, 301), border_radius=25)

        # tmp_rendered_text = oxygen54.render("bild von der", True, Colors.BLACK)
        # self.context.screen.blit(tmp_rendered_text, (758 + (423 - tmp_rendered_text.get_width()) / 2, 313 + 95))
        # tmp_rendered_text = oxygen54.render("kamera", True, Colors.BLACK)

        capture = pygame.transform.scale(self.capture, (423, 301))
        self.context.screen.blit(capture, (758, 313))

        # self.context.screen.blit(tmp_rendered_text,
        #                         (758 + (423 - tmp_rendered_text.get_width()) / 2, 313 + 95 + oxygen54.get_linesize()))

        tmp_rendered_text = oxygen36.render("QR-Code-Scanner aktiv… ⌛", True, Colors.BLACK)
        self.context.screen.blit(tmp_rendered_text,
                                 ((self.context.screen_config.WIDTH - tmp_rendered_text.get_width()) / 2, 649))

        self.draw_overlays(delta_t)

    def process_overlay_events(self, overlay_events: List[NavigationEvent]) -> NavigationEvent:
        for evt in overlay_events:
            if evt:
                return evt
        return NoAction()

    def process_events(self, events) -> NavigationEvent:
        self.capture: pygame.Surface = self.context.camera.get_image()

        overlay_events = [evt for evt in [ovl.process_events(events) for ovl in self.overlays] if evt]
        if overlay_events:
            return self.process_overlay_events(overlay_events)

        fp = f'/dev/shm/ferrytix_capture.jpg'

        pygame.image.save(self.capture, fp)

        img = cv2.imread(fp)
        bar_codes = pyzbar.decode(img)

        for bc in bar_codes:
            print(bc.data)
            return QRCodeRead(code=bc.data.decode())

        return RequireDraw()


class ReturnTicketOverview(Screen):
    def __init__(self, context):
        super(ReturnTicketOverview, self).__init__(context, overlays=[
            NavigationOverlay(context, title="Rückfahrt eingelöst."),
        ])

    def draw(self, delta_t: float) -> None:
        self.context.screen.fill(color=Colors.BACKGROUND)
        # self.draw_secondary_header("Rückfahrt eingelöst", lambda: self.draw_screen(3), True)

        tmp_rendered_text = oxygen48.render("Folgende Rückfahrten wurden eingelöst:", True, Colors.BLACK)
        self.context.screen.blit(tmp_rendered_text,
                                 ((self.context.screen_config.WIDTH - tmp_rendered_text.get_width()) / 2, 110))

        # self.draw_small_info_box(52, 207, "Erwachsener + Fahrrad", "2")  # 🚲 is a not supported unicode character
        # self.draw_small_info_box(678, 207, "Kind + Fahrrad", "4")
        # self.draw_small_info_box(51, 443, "Ermäßigt + Fahrrad", "1")

        pygame.draw.rect(self.context.screen, Colors.GREEN, pygame.Rect(440, 676, 400, 90), border_radius=25)
        # self.hitboxes.append(HitBox(440, 676, 400, 90, lambda: self.draw_screen(0)))
        tmp_rendered_text = oxygen48.render("Hauptmenü", True, Colors.WHITE)
        self.context.screen.blit(tmp_rendered_text, (
            440 + (400 - tmp_rendered_text.get_width()) / 2, 676 + 4 + (82 - tmp_rendered_text.get_height()) / 2))

        self.draw_overlays(delta_t)

    def process_overlay_events(self, overlay_events: List[NavigationEvent]) -> NavigationEvent:
        for evt in overlay_events:
            if evt:
                return evt
        return NoAction()


class UseReturnTicketMenu(Menu):
    def __init__(self, context):
        entry_point = ScanQRCode(
            context=context,
        )
        self.scan_qr_code_screen = entry_point
        self.return_ticket_overview_screen = ReturnTicketOverview(context=context)
        super(UseReturnTicketMenu, self).__init__(
            context=context,
            entry_point=entry_point,
            screens=[
                self.scan_qr_code_screen,
                self.return_ticket_overview_screen,
            ]
        )

    def process_screen_events(self, events) -> NavigationEvent:
        for evt in events:
            if evt:
                if isinstance(evt, ReturnHome):
                    self.current_screen = self.entry_point
                    return evt
                if isinstance(evt, RequireDraw):
                    return evt
                if isinstance(evt, QRCodeRead):
                    self.current_screen = self.return_ticket_overview_screen
                    return RequireDraw()
                else:
                    # unhandled event
                    raise NotImplementedError()
        return NoAction()

    def enter(self, **kwargs):
        self.context.camera.start()
        # current capture needs to be set to an image
        # without this step, the capture is None
        self.scan_qr_code_screen.capture = self.context.camera.get_image()

    def exit(self, **kwargs):
        self.context.camera.stop()
        # capture needs to be reset, without this step, the last picture from the previous
        # scan is still stored and will be processed
        self.scan_qr_code_screen.capture = None
