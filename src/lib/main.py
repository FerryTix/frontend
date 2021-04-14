import pygame
from colors import Colors

pygame.init()

HEIGHT = 800
WIDTH = 1280


pygame.font.init()
oxygen96 = pygame.font.Font("src/resources/Oxygen-Sans-Book.otf", 96)
oxygen72 = pygame.font.Font("src/resources/Oxygen-Sans-Book.otf", 72)
oxygen64 = pygame.font.Font("src/resources/Oxygen-Sans-Book.otf", 64)
oxygen54 = pygame.font.Font("src/resources/Oxygen-Sans-Book.otf", 54)  # Bold font has sizing problems
oxygen48 = pygame.font.Font("src/resources/Oxygen-Sans-Book.otf", 48)
oxygen36 = pygame.font.Font("src/resources/Oxygen-Sans-Book.otf", 36)
oxygen24 = pygame.font.Font("src/resources/Oxygen-Sans-Book.otf", 24)


class Hitbox:
    def __init__(self, x, y, width, height, f):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.f = f

    def collides_with(self, x, y):
        if((self.x <= x <= self.x + self.width) and (self.y <= y <= self.y + self.height)):
            return True
        return False


class Screen:
    def __init__(self, screen):
        self.screen = screen
        self.hitboxes = []

    def draw_secondary_header(self, heading, back_f, show_time):
        pygame.draw.rect(self.screen, Colors.GRAY.value, pygame.Rect(0, 0, WIDTH, 90))
        rendered_heading = oxygen54.render(heading, True, Colors.BLACK.value)
        self.screen.blit(rendered_heading, ((WIDTH - rendered_heading.get_width()) / 2, 13 + 77 / 2 - rendered_heading.get_height() / 2))
        if show_time is True:
            rendered_time = oxygen48.render("15:06 Uhr", True, Colors.BLACK.value)
            self.screen.blit(rendered_time, (1001 + (300 - rendered_time.get_width()) / 2, 13 + 77 / 2 - rendered_time.get_height() / 2))
        if back_f is not None:
            rendered_back = oxygen36.render("Zurück", True, Colors.WHITE.value)
            pygame.draw.rect(self.screen, Colors.RED2.value, pygame.Rect(19, 11, 250, 70), border_radius=25)
            self.hitboxes.append(Hitbox(19, 11, 250, 70, back_f))
            self.screen.blit(rendered_back, (86 + (183 - rendered_back.get_width()) / 2, 5 + 82 / 2 - rendered_back.get_height() / 2))
            back_arrow = pygame.image.load("src/resources/back_arrow.png")
            pygame.draw.rect(self.screen, Colors.WHITE.value, pygame.Rect(24, 16, 63.5, 60), border_radius=30)
            self.screen.blit(back_arrow, pygame.Rect(24, 16, 63.5, 60))

    def draw_add_balance_button(self, x, y, text, text_color):
        pygame.draw.rect(self.screen, Colors.GRAY2.value, pygame.Rect(x, y, 379, 100), border_radius=60)
        pygame.draw.rect(self.screen, Colors.GREEN2.value, pygame.Rect(x + 11, y + 10, 80, 80), border_radius=60)
        tmp_r_txt = oxygen72.render("+", True, Colors.WHITE.value)
        self.screen.blit(tmp_r_txt, (x + 11 + (80 - tmp_r_txt.get_width()) / 2, y + 10 + (80 - tmp_r_txt.get_height()) / 2))
        tmp_r_txt = oxygen64.render(text, True, text_color)
        self.screen.blit(tmp_r_txt, (x + 97 + (279 - tmp_r_txt.get_width()) / 2, y + 8 + (101 - tmp_r_txt.get_height()) / 2))

    def draw_bonus_display(self, x, y, text, text_color):
        pygame.draw.rect(self.screen, Colors.GRAY2.value, pygame.Rect(x, y, 158, 80), border_radius=60)
        tmp_r_txt = oxygen36.render(text, True, text_color)
        self.screen.blit(tmp_r_txt, (x + (158 - tmp_r_txt.get_width()) / 2, y + (80 - tmp_r_txt.get_height()) / 2))

    def draw_small_info_box(self, x, y, primary_text, secondary_text):
        pygame.draw.rect(self.screen, Colors.GRAY2.value, pygame.Rect(x, y, 550, 200), border_radius=15)
        tmp_r_txt = oxygen48.render(primary_text, True, Colors.BLACK.value)
        self.screen.blit(tmp_r_txt, (x + (550 - tmp_r_txt.get_width()) / 2, y + 18))
        pygame.draw.rect(self.screen, Colors.BLACK.value, pygame.Rect(x, y + 92, 550, 1))
        tmp_r_txt = oxygen48.render(secondary_text, True, Colors.BLACK.value)
        self.screen.blit(tmp_r_txt, (x + 550 - tmp_r_txt.get_width() - 43, y + 116))

    def draw_ticket_printing_controls(self):
        pygame.draw.rect(self.screen, Colors.BLACK.value, pygame.Rect(0, 654, WIDTH, 1))

        pygame.draw.rect(self.screen, Colors.GREEN.value, pygame.Rect((WIDTH - 708) / 2, 672, 708, 100), border_radius=25)
        self.hitboxes.append(Hitbox((WIDTH - 708) / 2, 672, 708, 100, lambda: self.draw_screen(0)))
        tmp_r_txt = oxygen48.render("Ticket ausdrucken", True, Colors.WHITE.value)
        self.screen.blit(tmp_r_txt, ((WIDTH - 708) / 2 + (709 - tmp_r_txt.get_width()) / 2, 672 + (100 - tmp_r_txt.get_height()) / 2))

    def draw_booking_widget(self, x, y, heading, bicycle_strikethrough, text_count, text_price_per_unit, text_result):
        pygame.draw.rect(self.screen, Colors.GRAY2.value, pygame.Rect(x, y, 550, 250), border_radius=15)
        tmp_image = pygame.image.load("src/resources/small_back_arrow.png")
        self.screen.blit(tmp_image, pygame.Rect(x + 108, y + 25, 36, 36))
        tmp_r_txt = oxygen48.render(heading, True, Colors.BLACK.value)
        self.screen.blit(tmp_r_txt, (x + 290 - tmp_r_txt.get_width() / 2, y + 12))
        tmp_image = pygame.image.load("src/resources/small_forward_arrow.png")
        self.screen.blit(tmp_image, pygame.Rect(x + 550 - 78 - 36, y + 25, 36, 36))
        pygame.draw.rect(self.screen, Colors.BLACK.value, pygame.Rect(x, y + 92, 551, 1))
        tmp_image = pygame.image.load("src/resources/🚲.png")
        self.screen.blit(tmp_image, pygame.Rect(x + 251, y + 109 - 34, 77, 37))
        pygame.draw.rect(self.screen, Colors.BLACK.value, pygame.Rect(x, y + 182, 551, 1))
        if bicycle_strikethrough is True:
            tmp_image = pygame.image.load("src/resources/bicycle_strikethrough.png")
            self.screen.blit(tmp_image, pygame.Rect(x + 250, y + 131 - 34, 88, 88))
        tmp_r_txt = oxygen64.render("-", True, Colors.BLACK.value)
        self.screen.blit(tmp_r_txt, (x + 26 + (69 - tmp_r_txt.get_width()) / 2, y + 165 + (93 - tmp_r_txt.get_height()) / 2))
        pygame.draw.rect(self.screen, Colors.WHITE.value, pygame.Rect(x + 84, y + 186, 66, 51), border_radius=25)
        tmp_r_txt = oxygen48.render(text_count, True, Colors.BLACK.value)
        self.screen.blit(tmp_r_txt, (x + 84 + (66 - tmp_r_txt.get_width()) / 2, y + 186 + (51 - tmp_r_txt.get_height()) / 2))
        tmp_r_txt = oxygen64.render("+", True, Colors.BLACK.value)
        self.screen.blit(tmp_r_txt, (x + 141 + (69 - tmp_r_txt.get_width()) / 2, y + 169 + (86 - tmp_r_txt.get_height()) / 2))
        tmp_r_txt = oxygen36.render(text_price_per_unit, True, Colors.BLACK.value)
        self.screen.blit(tmp_r_txt, (x + 293 - tmp_r_txt.get_width() / 2, y + 186))
        tmp_r_txt = oxygen36.render(text_result, True, Colors.BLACK.value)
        self.screen.blit(tmp_r_txt, (x + 454 - tmp_r_txt.get_width() / 2, y + 186))

    def draw_payment_button(self, x, y):
        pygame.draw.rect(self.screen, Colors.GREEN.value, pygame.Rect(x, y, 200, 90), border_radius=25)
        self.hitboxes.append(Hitbox(x, y, 200, 90, lambda: self.draw_screen(8)))  # TODO: Different behaviour for recharging of FährCard
        tmp_r_txt = oxygen48.render("Zahlen", True, Colors.WHITE.value)
        self.screen.blit(tmp_r_txt, (x + (200 - tmp_r_txt.get_width()) / 2, y + (90 - tmp_r_txt.get_height()) / 2))

    def draw_payment_method_widget(self, x, y, text, img, img_width, img_height):
        pygame.draw.rect(self.screen, Colors.GRAY2.value, pygame.Rect(x, y, 375, 418), border_radius=15)
        tmp_r_txt = oxygen64.render(text, True, Colors.BLACK.value)
        self.screen.blit(tmp_r_txt, (x + 188 - tmp_r_txt.get_width() / 2, y + 32))
        tmp_img = pygame.image.load(img)
        self.screen.blit(tmp_img, pygame.Rect(x + 188 - img_width / 2, y + 251 - img_height / 2, img_width, img_height))

    def draw_screen(self, i):
        self.hitboxes = []
        self.screen.fill(color=Colors.BACKGROUND.value)
        if i == 0:
            title_rect = pygame.Rect(0, 0, WIDTH, 200)
            pygame.draw.rect(self.screen, Colors.GRAY.value, title_rect)

            title = oxygen54.render("Ticketautomat Personenfähre Keer Tröch II", True, Colors.BLACK.value)
            subtitle = oxygen48.render("Bislich -> Xanten", True, Colors.BLACK.value)

            self.screen.blit(title, ((WIDTH - title.get_width()) / 2, 42))
            self.screen.blit(subtitle, ((WIDTH - subtitle.get_width()) / 2, 119))

            info_rect = pygame.Rect(50, 250, 550, 400)
            pygame.draw.rect(self.screen, Colors.GRAY2.value, info_rect, border_radius=15, )
            tmp_rendered_text = oxygen48.render("Fährzeiten", True, Colors.BLACK.value)
            self.screen.blit(tmp_rendered_text, (50 + 10, 250 + 1))

            info_rect = pygame.Rect(680, 250, 550, 400)
            pygame.draw.rect(self.screen, Colors.GRAY2.value, info_rect, border_radius=15, )
            tmp_rendered_text = oxygen48.render("Information", True, Colors.BLACK.value)
            self.screen.blit(tmp_rendered_text, (680 + 114, 250 + 1))
            tmp_rendered_text = oxygen36.render("Uhrzeit:", True, Colors.BLACK.value)
            self.screen.blit(tmp_rendered_text, (680 + (250 - tmp_rendered_text.get_width()) / 2, 250 + 86 + (77 - tmp_rendered_text.get_height()) / 2))
            tmp_rendered_text = oxygen48.render("15:06 Uhr", True, Colors.BLACK.value)
            self.screen.blit(tmp_rendered_text, (680 + 250 + (300 - tmp_rendered_text.get_width()) / 2, 250 + 86 + (77 - tmp_rendered_text.get_height()) / 2))
            tmp_rendered_text = oxygen36.render("Letzte Fahrt:", True, Colors.GRAY3.value)
            self.screen.blit(tmp_rendered_text, (680 + (250 - tmp_rendered_text.get_width()) / 2, 250 + 165 + (77 - tmp_rendered_text.get_height()) / 2))
            tmp_rendered_text = oxygen48.render("19:00 Uhr", True, Colors.GRAY3.value)
            self.screen.blit(tmp_rendered_text, (680 + 250 + (300 - tmp_rendered_text.get_width()) / 2, 250 + 165 + (77 - tmp_rendered_text.get_height()) / 2))
            tmp_rendered_text = oxygen36.render("Aktuell im Wartebereich:", True, Colors.BLACK.value)
            self.screen.blit(tmp_rendered_text, (680 + (550 - tmp_rendered_text.get_width()) / 2, 250 + 242 + (77 - tmp_rendered_text.get_height()) / 2))
            tmp_rendered_text = oxygen36.render("⬛ 17", True, Colors.BLACK.value)
            self.screen.blit(tmp_rendered_text, (680 + 142 + (152 - tmp_rendered_text.get_width()) / 2, 250 + 309 + (91 - tmp_rendered_text.get_height()) / 2))
            tmp_rendered_text = oxygen36.render("⬛ 11", True, Colors.BLACK.value)
            self.screen.blit(tmp_rendered_text, (680 + 291 + (152 - tmp_rendered_text.get_width()) / 2, 250 + 309 + (91 - tmp_rendered_text.get_height()) / 2))

            buy_ticket_rect = pygame.Rect(440, 676, 400, 90)
            self.hitboxes.append(Hitbox(440, 676, 400, 90, lambda: self.draw_screen(7)))
            pygame.draw.rect(self.screen, Colors.GREEN.value, buy_ticket_rect, border_radius=25, )
            subtitle = oxygen36.render("Ticket kaufen", True, Colors.BACKGROUND.value)
            self.screen.blit(subtitle, ((WIDTH - subtitle.get_width()) / 2, 676 + (90 - subtitle.get_height()) // 2))

            faehrcard_rect = pygame.Rect(895, 690, 340, 70)
            self.hitboxes.append(Hitbox(895, 690, 340, 70, lambda: self.draw_screen(1)))
            pygame.draw.rect(self.screen, Colors.BLUE.value, faehrcard_rect, border_radius=25, )
            subtitle = oxygen36.render("FährCard aufladen", True, Colors.BACKGROUND.value)
            self.screen.blit(subtitle, (895 + (340 - subtitle.get_width()) / 2, 690 + (70 - subtitle.get_height()) // 2))

            return_rect = pygame.Rect(45, 690, 340, 70)
            self.hitboxes.append(Hitbox(45, 690, 340, 70, lambda: self.draw_screen(3)))
            pygame.draw.rect(self.screen, Colors.TEAL.value, return_rect, border_radius=25, )
            subtitle = oxygen36.render("Rückfahrt einlösen", True, Colors.BACKGROUND.value)
            self.screen.blit(subtitle, (45 + (340 - subtitle.get_width()) / 2, 690 + (70 - subtitle.get_height()) // 2))
        elif i == 1:
            self.draw_secondary_header("FährCard™", lambda: self.draw_screen(0), True)

            pygame.draw.rect(self.screen, Colors.GRAY2.value, pygame.Rect(50, 130, 1180, 621), border_radius=15)
            self.hitboxes.append(Hitbox(50, 130, 1180, 621, lambda: self.draw_screen(2)))

            info = oxygen48.render("Bitte halten Sie Ihre FährCard an den NFC-Leser.", True, Colors.BLACK.value)
            self.screen.blit(info, (50 + (1180 - info.get_width()) / 2, 171))

            contactless_payment = pygame.image.load("src/resources/contactless_payment.png")
            self.screen.blit(contactless_payment, pygame.Rect(257, 273, 766, 375))

            text = oxygen36.render("NFC-Leser aktiv… ⌛", True, Colors.BLACK.value)
            self.screen.blit(text, (50 + (1180 - text.get_width()) / 2, 649))
        elif i == 2:
            self.draw_secondary_header("FährCard™", lambda: self.draw_screen(1), True)

            pygame.draw.rect(self.screen, Colors.GRAY2.value, pygame.Rect(50, 130, 590, 500), border_radius=15)
            tmp_rendered_text = oxygen36.render("Informationen zu Ihrer FährCard", True, Colors.BLACK.value)
            self.screen.blit(tmp_rendered_text, (50 + (590 - tmp_rendered_text.get_width()) / 2, 130 + 26))
            pygame.draw.rect(self.screen, Colors.BLACK.value, pygame.Rect(50, 217, 590, 1))
            tmp_rendered_text = oxygen24.render("Kartennummer", True, Colors.BLACK.value)
            self.screen.blit(tmp_rendered_text, (50 + 37, 130 + 105))
            tmp_rendered_text = oxygen24.render("3e8d***************f81c", True, Colors.BLACK.value)
            self.screen.blit(tmp_rendered_text, (50 + 590 - 41 - tmp_rendered_text.get_width(), 130 + 105))
            tmp_rendered_text = oxygen36.render("Ausgabedatum", True, Colors.BLACK.value)
            self.screen.blit(tmp_rendered_text, (50 + 34, 130 + 151))
            tmp_rendered_text = oxygen36.render("12.07.2021", True, Colors.BLACK.value)
            self.screen.blit(tmp_rendered_text, (50 + 590 - 41 - tmp_rendered_text.get_width(), 130 + 151))
            tmp_rendered_text = oxygen36.render("Letzte Aufladung", True, Colors.BLACK.value)
            self.screen.blit(tmp_rendered_text, (50 + 34, 130 + 215))
            tmp_rendered_text = oxygen36.render("24.07.2021", True, Colors.BLACK.value)
            self.screen.blit(tmp_rendered_text, (50 + 590 - 41 - tmp_rendered_text.get_width(), 130 + 215))
            tmp_rendered_text = oxygen36.render("Inhaber", True, Colors.BLACK.value)
            self.screen.blit(tmp_rendered_text, (50 + 34, 130 + 276))
            tmp_rendered_text = oxygen36.render("Leon Pascal", True, Colors.BLACK.value)
            self.screen.blit(tmp_rendered_text, (50 + 590 - 41 - tmp_rendered_text.get_width(), 130 + 276))
            tmp_rendered_text = oxygen36.render("Thierschmidt", True, Colors.BLACK.value)
            self.screen.blit(tmp_rendered_text, (50 + 590 - 41 - tmp_rendered_text.get_width(), 130 + 276 + oxygen36.get_linesize()))
            tmp_image = pygame.image.load("src/resources/tilted_heart.png")
            self.screen.blit(tmp_image, pygame.Rect(146, 337, 347, 314))
            tmp_image = pygame.image.load("src/resources/tilted_employee_text.png")
            self.screen.blit(tmp_image, pygame.Rect(259, 437, 119, 105))
            tmp_rendered_text = oxygen36.render("Guthaben:", True, Colors.BLACK.value)
            self.screen.blit(tmp_rendered_text, (50 + 35, 130 + 411))
            tmp_rendered_text = oxygen64.render("5,00 €", True, Colors.BLACK.value)
            self.screen.blit(tmp_rendered_text, (50 + 590 - 41 - tmp_rendered_text.get_width(), 130 + 393))

            tmp_rendered_text = oxygen36.render("Auflade-Optionen", True, Colors.BLACK.value)
            self.screen.blit(tmp_rendered_text, (682, 130))
            self.draw_add_balance_button(671, 197, "5,00 €", Colors.BLACK.value)
            self.draw_add_balance_button(671, 310, "10,00 €", Colors.BLACK.value)
            self.draw_add_balance_button(671, 423, "20,00 €", Colors.GREEN2.value)
            self.draw_add_balance_button(671, 536, "50,00 €", Colors.GREEN.value)

            tmp_rendered_text = oxygen36.render("Bonus", True, Colors.BLACK.value)
            self.screen.blit(tmp_rendered_text, (1102, 132))
            self.draw_bonus_display(1075, 207, "0,00 €", Colors.GRAY3.value)
            self.draw_bonus_display(1075, 320, "0,50 €", Colors.BLACK.value)
            self.draw_bonus_display(1075, 433, "2,00 €", Colors.GREEN2.value)
            self.draw_bonus_display(1075, 546, "10,00 €", Colors.GREEN.value)

            pygame.draw.rect(self.screen, Colors.BLACK.value, pygame.Rect(0, 675, WIDTH, 1))
            tmp_rendered_text = oxygen36.render("Gesamtpreis:", True, Colors.BLACK.value)
            self.screen.blit(tmp_rendered_text, (373 + (255 - tmp_rendered_text.get_width()) / 2, 709 + (58 - tmp_rendered_text.get_height()) / 2))
            tmp_rendered_text = oxygen64.render("50,00 €", True, Colors.BLACK.value)
            self.screen.blit(tmp_rendered_text, (628 + (279 - tmp_rendered_text.get_width()) / 2, 709 + (58 - tmp_rendered_text.get_height()) / 2))
            self.draw_payment_button(966, 693)
        elif i == 3:
            self.draw_secondary_header("Rückfahrt einlösen", lambda: self.draw_screen(0), True)

            tmp_image = pygame.image.load("src/resources/barcode_scanner.png")
            self.screen.blit(tmp_image, pygame.Rect(0, 277, 706, 372))
            self.hitboxes.append(Hitbox(0, 277, 706, 372, lambda: self.draw_screen(4)))

            tmp_rendered_text = oxygen48.render("Bitte halten Sie Ihr Ticket mit QR-Code", True, Colors.BLACK.value)
            self.screen.blit(tmp_rendered_text, ((WIDTH - tmp_rendered_text.get_width()) / 2, 121))
            tmp_rendered_text = oxygen48.render("vor die Kamera, mit einem Abstand von", True, Colors.BLACK.value)
            self.screen.blit(tmp_rendered_text, ((WIDTH - tmp_rendered_text.get_width()) / 2, 121 + oxygen48.get_linesize()))
            tmp_rendered_text = oxygen48.render("circa 20 cm.", True, Colors.BLACK.value)
            self.screen.blit(tmp_rendered_text, ((WIDTH - tmp_rendered_text.get_width()) / 2, 121 + 2 * oxygen48.get_linesize()))

            pygame.draw.rect(self.screen, Colors.GRAY2.value, pygame.Rect(758, 313, 423, 301), border_radius=25)
            tmp_rendered_text = oxygen54.render("bild von der", True, Colors.BLACK.value)
            self.screen.blit(tmp_rendered_text, (758 + (423 - tmp_rendered_text.get_width()) / 2, 313 + 95))
            tmp_rendered_text = oxygen54.render("kamera", True, Colors.BLACK.value)
            self.screen.blit(tmp_rendered_text, (758 + (423 - tmp_rendered_text.get_width()) / 2, 313 + 95 + oxygen54.get_linesize()))

            tmp_rendered_text = oxygen36.render("QR-Code-Scanner aktiv… ⌛", True, Colors.BLACK.value)
            self.screen.blit(tmp_rendered_text, ((WIDTH - tmp_rendered_text.get_width()) / 2, 649))
        elif i == 4:
            self.draw_secondary_header("Rückfahrt eingelöst", lambda: self.draw_screen(3), True)

            tmp_rendered_text = oxygen48.render("Folgende Rückfahrten wurden eingelöst:", True, Colors.BLACK.value)
            self.screen.blit(tmp_rendered_text, ((WIDTH - tmp_rendered_text.get_width()) / 2, 110))

            self.draw_small_info_box(52, 207, "Erwachsener + Fahrrad", "2")  # 🚲 is a not supported unicode character
            self.draw_small_info_box(678, 207, "Kind + Fahrrad", "4")
            self.draw_small_info_box(51, 443, "Ermäßigt + Fahrrad", "1")

            pygame.draw.rect(self.screen, Colors.GREEN.value, pygame.Rect(440, 676, 400, 90), border_radius=25)
            self.hitboxes.append(Hitbox(440, 676, 400, 90, lambda: self.draw_screen(0)))
            tmp_rendered_text = oxygen48.render("Hauptmenü", True, Colors.WHITE.value)
            self.screen.blit(tmp_rendered_text, (440 + (400 - tmp_rendered_text.get_width()) / 2, 676 + 4 + (82 - tmp_rendered_text.get_height()) / 2))
        elif i == 5:
            self.draw_secondary_header("Vielen Dank für Ihre Buchung.", None, False)

            pygame.draw.rect(self.screen, Colors.GRAY2.value, pygame.Rect(286, 127, 708, 442), border_radius=50)
            tmp_rendered_text = oxygen48.render("Erinnerungsfoto", True, Colors.GRAY3.value)
            self.screen.blit(tmp_rendered_text, (286 + (708 - tmp_rendered_text.get_width()) / 2, 127 + 88))
            tmp_rendered_text = oxygen48.render("Hier drücken, um ein", True, Colors.GRAY3.value)
            self.screen.blit(tmp_rendered_text, (286 + (708 - tmp_rendered_text.get_width()) / 2, 127 + 224))
            tmp_rendered_text = oxygen48.render("Foto zu machen", True, Colors.GRAY3.value)
            self.screen.blit(tmp_rendered_text, (286 + (708 - tmp_rendered_text.get_width()) / 2, 127 + 224 + oxygen48.get_linesize()))

            # TODO: Replace with real logic
            self.hitboxes.append(Hitbox(286, 127, 708, 442, lambda: self.draw_screen(6)))

            self.draw_ticket_printing_controls()
        elif i == 6:
            self.draw_secondary_header("Vielen Dank für Ihre Buchung.", None, False)

            tmp_image = pygame.image.load("src/resources/linus_sex_tips.png")
            self.screen.blit(tmp_image, pygame.Rect(286, 127, 708, 442))

            pygame.draw.rect(self.screen, Colors.BLUE.value, pygame.Rect(286, 127 + 442, 355, 62), border_bottom_left_radius=50)
            self.hitboxes.append(Hitbox(286, 127 + 442, 355, 62, lambda: self.draw_screen(6)))
            tmp_rendered_text = oxygen48.render("neues Foto", True, Colors.WHITE.value)
            self.screen.blit(tmp_rendered_text, (286 + (354 - tmp_rendered_text.get_width()) / 2, 127 + 442 + (62 - tmp_rendered_text.get_height()) / 2))

            pygame.draw.rect(self.screen, Colors.RED.value, pygame.Rect(639, 127 + 442, 355, 62), border_bottom_right_radius=50)
            self.hitboxes.append(Hitbox(639, 127 + 442, 355, 62, lambda: self.draw_screen(5)))
            tmp_rendered_text = oxygen48.render("Foto löschen", True, Colors.WHITE.value)
            self.screen.blit(tmp_rendered_text, (639 + (354 - tmp_rendered_text.get_width()) / 2, 127 + 442 + (62 - tmp_rendered_text.get_height()) / 2))

            self.draw_ticket_printing_controls()
        elif i == 7:
            self.draw_secondary_header("Buchung", lambda: self.draw_screen(0), True)

            self.draw_booking_widget(50, 130, "Erwachsener", False, "2", "x 3,00 € =", "6,00 €")
            self.draw_booking_widget(680, 130, "Erwachsener", False, "4", "x 1,50 € =", "6,00 €")
            self.draw_booking_widget(49, 403, "Ermäßigt", True, "1", "x 0,70 € =", "0,70 €")

            pygame.draw.rect(self.screen, Colors.BLACK.value, pygame.Rect(0, 675, WIDTH, 1))

            pygame.draw.rect(self.screen, Colors.BLUE.value, pygame.Rect(19, 703, 324, 70), border_radius=25)
            tmp_rendered_text = oxygen36.render("Rückfahrt:", True, Colors.WHITE.value)
            self.screen.blit(tmp_rendered_text, (19 + (250 - tmp_rendered_text.get_width()) / 2, 703 + (70 - tmp_rendered_text.get_height()) / 2))
            tmp_image = pygame.image.load("src/resources/checkmark_solid.png")
            self.screen.blit(tmp_image, pygame.Rect(19 + 260, 703 + 5, 60, 60))

            tmp_rendered_text = oxygen36.render("Gesamtpreis:", True, Colors.BLACK.value)
            self.screen.blit(tmp_rendered_text, (373 + (255 - tmp_rendered_text.get_width()) / 2, 709 + (58 - tmp_rendered_text.get_height()) / 2))

            tmp_rendered_text = oxygen64.render("12,70 €", True, Colors.BLACK.value)
            self.screen.blit(tmp_rendered_text, (628 + (279 - tmp_rendered_text.get_width()) / 2, 695))

            pygame.draw.rect(self.screen, Colors.GREEN2.value, pygame.Rect(900, 475, 110, 110), border_radius=60)
            tmp_rendered_text = oxygen96.render("+", True, Colors.WHITE.value)
            self.screen.blit(tmp_rendered_text, (900 + (110 - tmp_rendered_text.get_width()) / 2, 475 + (110 - tmp_rendered_text.get_height()) / 2))

            self.draw_payment_button(966, 693)
        elif i == 8:
            self.draw_secondary_header("Zahlungsmittel wählen", lambda: self.draw_screen(7), True)

            self.draw_payment_method_widget(50, 191, "FährCard", "src/resources/contactless_card.png", 194, 194)
            self.draw_payment_method_widget(452, 191, "Bar-Geld", "src/resources/jesus_holding_cash.png", 240, 240)
            self.draw_payment_method_widget(854, 191, "EC-Karte", "src/resources/electronic_cash_logo.png", 188, 188)

            # TODO: Replace with real logic
            self.hitboxes.append(Hitbox(50, 191, 1179, 418, lambda: self.draw_screen(5)))

            pygame.draw.rect(self.screen, Colors.BLACK.value, pygame.Rect(0, 675, WIDTH, 1))

            tmp_rendered_text = oxygen36.render("Betrag:", True, Colors.BLACK.value)
            self.screen.blit(tmp_rendered_text, (373 + (255 - tmp_rendered_text.get_width()) / 2, 709 + (58 - tmp_rendered_text.get_height()) / 2))

            tmp_rendered_text = oxygen64.render("12,70 €", True, Colors.BLACK.value)
            self.screen.blit(tmp_rendered_text, (628 + (279 - tmp_rendered_text.get_width()) / 2, 695))
        pygame.display.flip()


ui = Screen(pygame.display.set_mode((WIDTH, HEIGHT)))
ui.draw_screen(0)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONUP:
            for hitbox in ui.hitboxes:
                epx, epy = event.pos
                if hitbox.collides_with(epx, epy):
                    hitbox.f()
