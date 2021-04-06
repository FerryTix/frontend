import pygame
from colors import Colors
from time import sleep

HEIGHT = 800
WIDTH = 1280
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(color=Colors.BACKGROUND.value)

# username_rect = pg.rect.Rect(screenwidth/2 - 1/8*screenwidth, screenheight*1/5, 1/4*screenwidth, username_title_render.get_height() + 10)
# pg.draw.rect(screen, (0,0,0), username_rect,border_radius = 15)


pygame.font.init()
oxygen54 = pygame.font.SysFont(name='oxygensans', size=54, bold=True)
oxygen48 = pygame.font.SysFont(name='oxygensans', size=48)
oxygen36 = pygame.font.SysFont(name='oxygensans', size=36, bold=True)

title_rect = pygame.rect.Rect(0, 0, WIDTH, 200)
pygame.draw.rect(screen, Colors.GRAY.value, title_rect)

title = oxygen54.render(
    "Ticketautomat Personenfähre Keer Tröch II",
    True, Colors.BLACK.value
)
subtitle = oxygen48.render(
    "Bislich -> Xanten",
    True, Colors.BLACK.value
)

screen.blit(title, ((WIDTH - title.get_width()) / 2, 42))
screen.blit(subtitle, ((WIDTH - subtitle.get_width()) / 2, 119))

x, y = 50, 250
info_rect = pygame.rect.Rect(x, y, 550, 400)
pygame.draw.rect(screen, Colors.GRAY2.value, info_rect, border_radius=15, )

x, y = 680, 250
info_rect = pygame.rect.Rect(x, y, 550, 400)
pygame.draw.rect(screen, Colors.GRAY2.value, info_rect, border_radius=15, )

x, y = 440, 676
buy_ticket_rect = pygame.rect.Rect(x, y, 400, 90)
pygame.draw.rect(screen, Colors.GREEN.value, buy_ticket_rect, border_radius=25, )
subtitle = oxygen36.render(
    "Ticket kaufen",
    True, Colors.BACKGROUND.value
)
screen.blit(subtitle, ((WIDTH - subtitle.get_width()) / 2, 676 + (90 - subtitle.get_height()) // 2))

x, y = 895, 690
faehrcard_rect = pygame.rect.Rect(x, y, 340, 70)
pygame.draw.rect(screen, Colors.BLUE.value, faehrcard_rect, border_radius=25, )
subtitle = oxygen36.render(
    "FährCard aufladen",
    True, Colors.BACKGROUND.value
)
screen.blit(subtitle, (x + (340 - subtitle.get_width()) / 2, y + (70 - subtitle.get_height()) // 2))

x, y = 45, 690
return_rect = pygame.rect.Rect(x, y, 340, 70)
pygame.draw.rect(screen, Colors.TEAL.value, return_rect, border_radius=25, )
subtitle = oxygen36.render(
    "Rückfahrt einlösen",
    True, Colors.BACKGROUND.value
)
screen.blit(subtitle, (x + (340 - subtitle.get_width()) / 2, y + (70 - subtitle.get_height()) // 2))

pygame.display.flip()

sleep(2)
quit()

while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            print("Button Up!")
            print(event)
