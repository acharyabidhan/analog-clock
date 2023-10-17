import pygame
pygame.init()

import math
screen_info = pygame.display.Info()
# WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h
WIDTH, HEIGHT = 700,700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
LABEL_FONT = pygame.font.Font(None, 18)
CLOCK_FONT = pygame.font.Font(None, 40)
LINE_LENGTH = 5
running = True

lines_no = 50

step_x = WIDTH / lines_no
step_y = HEIGHT / lines_no

pos_x = 0
pos_y = 0

sensitivity = 5

def get_position(x, y):
    x = (WIDTH / 2) - (step_x * abs(x)) if x < 0 else (WIDTH / 2) + (step_x * x)
    y = (HEIGHT / 2) + (step_y * abs(y)) if y < 0 else (HEIGHT / 2) - (step_y * y)
    x = WIDTH / 2 if x == 0 else x
    y = HEIGHT / 2 if y == 0 else y
    return x+pos_x, y+pos_y

def get_size(size):
    return step_x * (size/100)

def draw_text(font, surface, position, text, color):
    text = font.render(text, True, color)
    text_pos_x = position[0] - (text.get_width() / 2)
    text_pos_y = position[1] - (text.get_height() / 2)
    surface.blit(text, (text_pos_x, text_pos_y))

surface = pygame.Surface((50,50))

timer_event = pygame.USEREVENT
pygame.time.set_timer(timer_event, 1000)

import time

seconds = int(time.strftime("%S"))
minutes = int(time.strftime("%M"))
hours = int(time.strftime("%I"))

second_hand_angle = -seconds * 6
minute_hand_angle = -(minutes * 6 + ((6 * seconds) / 60))
hour_hand_angle = -((hours * 30) + ((30 * minutes) / 60))

def draw_hands(surface, ax, ay, bx, by, hand, color, size, lw):
    cx, cy = 0, 0
    nax, nay = ax - cx, ay - cy
    nbx, nby = bx - cx, by - cy
    hand_angle_in_radians = math.radians(hand)
    nax_ = nax * math.cos(hand_angle_in_radians) - nay * math.sin(hand_angle_in_radians)
    nay_ = nax * math.sin(hand_angle_in_radians) + nay * math.cos(hand_angle_in_radians)
    nbx_ = nbx * math.cos(hand_angle_in_radians) - nby * math.sin(hand_angle_in_radians)
    nby_ = nbx * math.sin(hand_angle_in_radians) + nby * math.cos(hand_angle_in_radians)
    fax, fay = nax_ + cx, nay_ + cy
    fbx, fby = nbx_ + cx, nby_ + cy
    pygame.draw.line(surface, color, get_position(fax, fay), get_position(fbx, fby), lw)
    pygame.draw.circle(surface, color, get_position(cx, cy), size)

def create_coordinate(surface):
    for i in range(lines_no):
        start_pos_x = step_x * i
        start_pos_y = (HEIGHT / 2) - LINE_LENGTH
        end_pos_x = step_x * i
        end_pos_y = (HEIGHT / 2) + LINE_LENGTH
        pygame.draw.line(surface, (100,100,100), (start_pos_x+pos_x, start_pos_y+pos_y), (end_pos_x+pos_x, end_pos_y+pos_y))
        label = i - (lines_no / 2)
        surface.blit(LABEL_FONT.render(str(int(label)), True, (100,100,100)),(end_pos_x+pos_x, end_pos_y+pos_y))
        start_pos_x = (WIDTH / 2) - LINE_LENGTH
        start_pos_y = step_y * i
        end_pos_x = (WIDTH / 2) + LINE_LENGTH
        end_pos_y = step_y * i
        pygame.draw.line(surface, (100,100,100), (start_pos_x+pos_x, start_pos_y+pos_y), (end_pos_x+pos_x, end_pos_y+pos_y))
        label = (lines_no / 2) - i
        if not label:
            continue
        surface.blit(LABEL_FONT.render(str(int(label)), True, (100,100,100)),(end_pos_x+pos_x, end_pos_y+pos_y))
    pygame.draw.line(surface, (100,100,100), (0+pos_x, HEIGHT/2+pos_y), (WIDTH+pos_x, HEIGHT/2+pos_y))
    pygame.draw.line(surface, (100,100,100), (WIDTH/2+pos_x, 0+pos_y), (WIDTH/2+pos_x, HEIGHT+pos_y))
    pygame.draw.line(surface, (100,100,100), (0, mouse_pos_y), (WIDTH, mouse_pos_y))
    pygame.draw.line(surface, (100,100,100), (mouse_pos_x, 0), (mouse_pos_x, HEIGHT))

while running:
    keys = pygame.key.get_pressed()
    mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            running = False
        if event.type == pygame.MOUSEWHEEL:
            lines_no -= (event.y + event.y)
            if lines_no > 1:
                step_x = WIDTH / lines_no
                step_y = HEIGHT / lines_no
            else:
                lines_no = 50
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                pos_x = 0
                pos_y = 0
                lines_no = 50
                step_x = WIDTH / lines_no
                step_y = HEIGHT / lines_no
        if event.type == timer_event:
            minute_hand_angle -= 0.1
            if seconds == 60:
                minutes += 1
                seconds = 0
                hour_hand_angle -= 0.5
            if minutes == 60:
                hours += 1
                minutes = 0
            if hours == 12:
                hours = 0
            second_hand_angle -= 6
            seconds += 1
    if keys[pygame.K_LEFT]:
        pos_x -= sensitivity
    if keys[pygame.K_RIGHT]:
        pos_x += sensitivity
    if keys[pygame.K_UP]:
        pos_y -= sensitivity
    if keys[pygame.K_DOWN]:
        pos_y += sensitivity
    screen.fill((0,0,0))
    create_coordinate(screen)
    pygame.draw.circle(screen, (255,0,0), get_position(0,0), get_size(2400), 1)
    draw_hands(screen, 0, 0, 0, 15, hour_hand_angle, (0,0,255), get_size(100), 7)
    draw_hands(screen, 0, 0, 0, 20, minute_hand_angle, (0,255,0), get_size(75), 3)
    draw_hands(screen, 0, -3, 0, 20, second_hand_angle, (255,0,0), get_size(50), 1)
    indicator_angle = 0
    for i in range(60):
        x1, y1 = 0, 0
        x2, y2 = 0, 22
        angle_in_radians = math.radians(indicator_angle)
        x3 = math.cos(angle_in_radians) * (x2 - x1) - math.sin(angle_in_radians) * (y2 - y1) + x1
        y3 = math.sin(angle_in_radians) * (x2 - x1) + math.cos(angle_in_radians) * (y2 - y1) + y1
        if (indicator_angle / 6) % 5 == 0:
            clock_label_text = (indicator_angle / 6) / 5
            clock_label_text = "12" if clock_label_text == 0 else clock_label_text
            clock_label_text = str(abs(int(clock_label_text)))
            draw_text(CLOCK_FONT, screen, get_position(x3, y3), clock_label_text, (0,0,255))
        else:
            pygame.draw.circle(screen, (0,255,0), get_position(x3, y3), get_size(20))
        indicator_angle -= 6
    pygame.display.flip()
    clock.tick(30)

pygame.quit()

# Made by Bidhan Acharya