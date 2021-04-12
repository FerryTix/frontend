from time import sleep
import pygame
from colors import Colors

pygame.init()

HEIGHT = 800
WIDTH = 1280
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(color=Colors.BACKGROUND.value)

pygame.font.init()
oxygen72 = pygame.font.Font("src/resources/Oxygen-Sans-Book.otf", 72)
oxygen64 = pygame.font.Font("src/resources/Oxygen-Sans-Book.otf", 64)
oxygen54 = pygame.font.Font("src/resources/Oxygen-Sans-Book.otf", 54)  # Bold font has sizing problems
oxygen48 = pygame.font.Font("src/resources/Oxygen-Sans-Book.otf", 48)
oxygen36 = pygame.font.Font("src/resources/Oxygen-Sans-Book.otf", 36)
oxygen24 = pygame.font.Font("src/resources/Oxygen-Sans-Book.otf", 24)

navigation = 0


def draw_secondary_header(heading, show_back, show_time):
    pygame.draw.rect(screen, Colors.GRAY.value, pygame.Rect(0, 0, WIDTH, 90))
    rendered_heading = oxygen54.render(heading, True, Colors.BLACK.value)
    screen.blit(rendered_heading, ((WIDTH - rendered_heading.get_width()) / 2, 13 + 77 / 2 - rendered_heading.get_height() / 2))
    if show_time is True:
        rendered_time = oxygen48.render("15:06 Uhr", True, Colors.BLACK.value)
        screen.blit(rendered_time, (1001 + (300 - rendered_time.get_width()) / 2, 13 + 77 / 2 - rendered_time.get_height() / 2))
    if show_back is True:
        rendered_back = oxygen36.render("Zurück", True, Colors.WHITE.value)
        pygame.draw.rect(screen, Colors.RED.value, pygame.Rect(19, 11, 250, 70), border_radius=25, )
        screen.blit(rendered_back, (86 + (183 - rendered_back.get_width()) / 2, 5 + 82 / 2 - rendered_back.get_height() / 2))
        back_arrow = pygame.image.load("src/resources/back_arrow.png")
        pygame.draw.rect(screen, Colors.WHITE.value, pygame.Rect(24, 16, 63.5, 60), border_radius=30)
        screen.blit(back_arrow, pygame.Rect(24, 16, 63.5, 60))


def draw_add_balance_button(x, y, text, text_color):
    pygame.draw.rect(screen, Colors.GRAY2.value, pygame.Rect(x, y, 379, 100), border_radius=60)
    pygame.draw.rect(screen, Colors.GREEN2.value, pygame.Rect(x + 11, y + 10, 80, 80), border_radius=60)
    tmp_r_txt = oxygen72.render("+", True, Colors.WHITE.value)
    screen.blit(tmp_r_txt, (x + 11 + (80 - tmp_r_txt.get_width()) / 2, y + 10 + (80 - tmp_r_txt.get_height()) / 2))
    tmp_r_txt = oxygen64.render(text, True, text_color)
    screen.blit(tmp_r_txt, (x + 97 + (279 - tmp_r_txt.get_width()) / 2, y + 8 + (101 - tmp_r_txt.get_height()) / 2))


def draw_bonus_display(x, y, text, text_color):
    pygame.draw.rect(screen, Colors.GRAY2.value, pygame.Rect(x, y, 158, 80), border_radius=60)
    tmp_r_txt = oxygen36.render(text, True, text_color)
    screen.blit(tmp_r_txt, (x + (158 - tmp_r_txt.get_width()) / 2, y + (80 - tmp_r_txt.get_height()) / 2))


if navigation == 0:
    title_rect = pygame.Rect(0, 0, WIDTH, 200)
    pygame.draw.rect(screen, Colors.GRAY.value, title_rect)

    title = oxygen54.render("Ticketautomat Personenfähre Keer Tröch II", True, Colors.BLACK.value)
    subtitle = oxygen48.render("Bislich -> Xanten", True, Colors.BLACK.value)

    screen.blit(title, ((WIDTH - title.get_width()) / 2, 42))
    screen.blit(subtitle, ((WIDTH - subtitle.get_width()) / 2, 119))

    x, y = 50, 250
    info_rect = pygame.Rect(x, y, 550, 400)
    pygame.draw.rect(screen, Colors.GRAY2.value, info_rect, border_radius=15, )

    x, y = 680, 250
    info_rect = pygame.Rect(x, y, 550, 400)
    pygame.draw.rect(screen, Colors.GRAY2.value, info_rect, border_radius=15, )

    x, y = 440, 676
    buy_ticket_rect = pygame.Rect(x, y, 400, 90)
    pygame.draw.rect(screen, Colors.GREEN.value, buy_ticket_rect, border_radius=25, )
    subtitle = oxygen36.render("Ticket kaufen", True, Colors.BACKGROUND.value)
    screen.blit(subtitle, ((WIDTH - subtitle.get_width()) / 2, 676 + (90 - subtitle.get_height()) // 2))

    x, y = 895, 690
    faehrcard_rect = pygame.Rect(x, y, 340, 70)
    pygame.draw.rect(screen, Colors.BLUE.value, faehrcard_rect, border_radius=25, )
    subtitle = oxygen36.render("FährCard aufladen", True, Colors.BACKGROUND.value)
    screen.blit(subtitle, (x + (340 - subtitle.get_width()) / 2, y + (70 - subtitle.get_height()) // 2))

    x, y = 45, 690
    return_rect = pygame.Rect(x, y, 340, 70)
    pygame.draw.rect(screen, Colors.TEAL.value, return_rect, border_radius=25, )
    subtitle = oxygen36.render("Rückfahrt einlösen", True, Colors.BACKGROUND.value)
    screen.blit(subtitle, (x + (340 - subtitle.get_width()) / 2, y + (70 - subtitle.get_height()) // 2))
elif navigation == 1:
    draw_secondary_header("FährCard™", True, True)

    pygame.draw.rect(screen, Colors.GRAY2.value, pygame.Rect(50, 130, 1180, 621), border_radius=15)

    info = oxygen48.render("Bitte halten Sie Ihre FährCard an den NFC-Leser.", True, Colors.BLACK.value)
    screen.blit(info, (50 + (1180 - info.get_width()) / 2, 171))

    contactless_payment = pygame.image.load("src/resources/contactless_payment.png")
    screen.blit(contactless_payment, pygame.Rect(257, 273, 766, 375))

    text = oxygen36.render("NFC-Leser aktiv… ⌛", True, Colors.BLACK.value)
    screen.blit(text, (50 + (1180 - text.get_width()) / 2, 649))
elif navigation == 2:
    draw_secondary_header("FährCard™", True, True)

    pygame.draw.rect(screen, Colors.GRAY2.value, pygame.Rect(50, 130, 590, 500), border_radius=15)
    tmp_rendered_text = oxygen36.render("Informationen zu Ihrer FährCard", True, Colors.BLACK.value)
    screen.blit(tmp_rendered_text, (50 + (590 - tmp_rendered_text.get_width()) / 2, 130 + 26))
    pygame.draw.rect(screen, Colors.BLACK.value, pygame.Rect(50, 217, 590, 1))
    tmp_rendered_text = oxygen24.render("Kartennummer", True, Colors.BLACK.value)
    screen.blit(tmp_rendered_text, (50 + 37, 130 + 105))
    tmp_rendered_text = oxygen24.render("3e8d***************f81c", True, Colors.BLACK.value)
    screen.blit(tmp_rendered_text, (50 + 590 - 41 - tmp_rendered_text.get_width(), 130 + 105))
    tmp_rendered_text = oxygen36.render("Ausgabedatum", True, Colors.BLACK.value)
    screen.blit(tmp_rendered_text, (50 + 34, 130 + 151))
    tmp_rendered_text = oxygen36.render("12.07.2021", True, Colors.BLACK.value)
    screen.blit(tmp_rendered_text, (50 + 590 - 41 - tmp_rendered_text.get_width(), 130 + 151))
    tmp_rendered_text = oxygen36.render("Letzte Aufladung", True, Colors.BLACK.value)
    screen.blit(tmp_rendered_text, (50 + 34, 130 + 215))
    tmp_rendered_text = oxygen36.render("24.07.2021", True, Colors.BLACK.value)
    screen.blit(tmp_rendered_text, (50 + 590 - 41 - tmp_rendered_text.get_width(), 130 + 215))
    tmp_rendered_text = oxygen36.render("Inhaber", True, Colors.BLACK.value)
    screen.blit(tmp_rendered_text, (50 + 34, 130 + 276))
    tmp_rendered_text = oxygen36.render("Leon Pascal", True, Colors.BLACK.value)
    screen.blit(tmp_rendered_text, (50 + 590 - 41 - tmp_rendered_text.get_width(), 130 + 276))
    tmp_rendered_text = oxygen36.render("Thierschmidt", True, Colors.BLACK.value)
    screen.blit(tmp_rendered_text, (50 + 590 - 41 - tmp_rendered_text.get_width(), 130 + 276 + oxygen36.get_linesize()))
    tmp_image = pygame.image.load("src/resources/tilted_heart.png")
    screen.blit(tmp_image, pygame.Rect(146, 337, 347, 314))
    tmp_image = pygame.image.load("src/resources/tilted_employee_text.png")
    screen.blit(tmp_image, pygame.Rect(259, 437, 119, 105))
    tmp_rendered_text = oxygen36.render("Guthaben:", True, Colors.BLACK.value)
    screen.blit(tmp_rendered_text, (50 + 35, 130 + 411))
    tmp_rendered_text = oxygen64.render("5,00 €", True, Colors.BLACK.value)
    screen.blit(tmp_rendered_text, (50 + 590 - 41 - tmp_rendered_text.get_width(), 130 + 393))

    tmp_rendered_text = oxygen36.render("Auflade-Optionen", True, Colors.BLACK.value)
    screen.blit(tmp_rendered_text, (682, 130))
    draw_add_balance_button(671, 197, "5,00 €", Colors.BLACK.value)
    draw_add_balance_button(671, 310, "10,00 €", Colors.BLACK.value)
    draw_add_balance_button(671, 423, "20,00 €", Colors.GREEN2.value)
    draw_add_balance_button(671, 536, "50,00 €", Colors.GREEN.value)

    tmp_rendered_text = oxygen36.render("Bonus", True, Colors.BLACK.value)
    screen.blit(tmp_rendered_text, (1102, 132))
    draw_bonus_display(1075, 207, "0,00 €", Colors.GRAY3.value)
    draw_bonus_display(1075, 320, "0,50 €", Colors.BLACK.value)
    draw_bonus_display(1075, 433, "2,00 €", Colors.GREEN2.value)
    draw_bonus_display(1075, 546, "10,00 €", Colors.GREEN.value)

    pygame.draw.rect(screen, Colors.BLACK.value, pygame.Rect(0, 675, WIDTH, 1))
    tmp_rendered_text = oxygen36.render("Gesamtpreis:", True, Colors.BLACK.value)
    screen.blit(tmp_rendered_text, (373 + (255 - tmp_rendered_text.get_width()) / 2, 709 + (58 - tmp_rendered_text.get_height()) / 2))
    tmp_rendered_text = oxygen64.render("50,00 €", True, Colors.BLACK.value)
    screen.blit(tmp_rendered_text, (628 + (279 - tmp_rendered_text.get_width()) / 2, 709 + (58 - tmp_rendered_text.get_height()) / 2))
    pygame.draw.rect(screen, Colors.GREEN.value, pygame.Rect(966, 693, 200, 90), border_radius=25)
    tmp_rendered_text = oxygen48.render("Zahlen", True, Colors.WHITE.value)
    screen.blit(tmp_rendered_text, (966 + (200 - tmp_rendered_text.get_width()) / 2, 693 + (90 - tmp_rendered_text.get_height()) / 2))
elif navigation == 3:
    draw_secondary_header("Rückfahrt einlösen", True, True)
elif navigation == 4:
    draw_secondary_header("Rückfahrt eingelöst", True, True)
elif navigation == 5:
    draw_secondary_header("Vielen Dank für Ihre Buchung.", False, False)
elif navigation == 6:
    draw_secondary_header("Vielen Dank für Ihre Buchung.", False, False)
elif navigation == 7:
    draw_secondary_header("Buchung", True, True)
elif navigation == 8:
    draw_secondary_header("Zahlungsmittel wählen", True, True)
pygame.display.flip()

sleep(5)
quit()

while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            print("Button Up!")
            print(event)
