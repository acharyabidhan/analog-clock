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
minute_hand_angle = -minutes * 6
hour_hand_angle = -hours * 30

while running:
    keys = pygame.key.get_pressed()
    mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            running = False
        if event.type == pygame.MOUSEWHEEL:
            lines_no -= (event.y + event.y)
            step_x = WIDTH / lines_no
            step_y = HEIGHT / lines_no
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                pos_x = 0
                pos_y = 0
        if event.type == timer_event:
            if seconds == 60:
                minute_hand_angle -= 6
                minutes += 1
                seconds = 0
            if minutes == 60:
                hour_hand_angle -= 6
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
    screen.fill((20,30,40))
    for i in range(lines_no):
        start_pos_x = step_x * i
        start_pos_y = (HEIGHT / 2) - LINE_LENGTH
        end_pos_x = step_x * i
        end_pos_y = (HEIGHT / 2) + LINE_LENGTH
        # pygame.draw.line(screen, (100,100,100), (start_pos_x+pos_x, start_pos_y+pos_y), (end_pos_x+pos_x, end_pos_y+pos_y))
        label = i - (lines_no / 2)
        # screen.blit(LABEL_FONT.render(str(int(label)), True, (100,100,100)),(end_pos_x+pos_x, end_pos_y+pos_y))
        start_pos_x = (WIDTH / 2) - LINE_LENGTH
        start_pos_y = step_y * i
        end_pos_x = (WIDTH / 2) + LINE_LENGTH
        end_pos_y = step_y * i
        # pygame.draw.line(screen, (100,100,100), (start_pos_x+pos_x, start_pos_y+pos_y), (end_pos_x+pos_x, end_pos_y+pos_y))
        label = (lines_no / 2) - i
        if label:
            # screen.blit(LABEL_FONT.render(str(int(label)), True, (100,100,100)),(end_pos_x+pos_x, end_pos_y+pos_y))
            ...
    # pygame.draw.line(screen, (100,100,100), (0+pos_x, HEIGHT/2+pos_y), (WIDTH+pos_x, HEIGHT/2+pos_y))
    # pygame.draw.line(screen, (100,100,100), (WIDTH/2+pos_x, 0+pos_y), (WIDTH/2+pos_x, HEIGHT+pos_y))
    # pygame.draw.line(screen, (100,100,100), (0, mouse_pos_y), (WIDTH, mouse_pos_y))
    # pygame.draw.line(screen, (100,100,100), (mouse_pos_x, 0), (mouse_pos_x, HEIGHT))

    pygame.draw.circle(screen, (255,255,0), get_position(0,0), get_size(2400), 1)

    hr_ax, hr_ay = 0, 0
    hr_bx, hr_by = 0, 15
    hr_cx, hr_cy = 0, 0
    hr_nax, hr_nay = hr_ax - hr_cx, hr_ay - hr_cy
    hr_nbx, hr_nby = hr_bx - hr_cx, hr_by - hr_cy
    hr_nax_ = hr_nax * math.cos(math.radians(hour_hand_angle)) - hr_nay * math.sin(math.radians(hour_hand_angle))
    hr_nay_ = hr_nax * math.sin(math.radians(hour_hand_angle)) + hr_nay * math.cos(math.radians(hour_hand_angle))
    hr_nbx_ = hr_nbx * math.cos(math.radians(hour_hand_angle)) - hr_nby * math.sin(math.radians(hour_hand_angle))
    hr_nby_ = hr_nbx * math.sin(math.radians(hour_hand_angle)) + hr_nby * math.cos(math.radians(hour_hand_angle))
    hr_fax, hr_fay = hr_nax_ + hr_cx, hr_nay_ + hr_cy
    hr_fbx, hr_fby = hr_nbx_ + hr_cx, hr_nby_ + hr_cy
    pygame.draw.line(screen, (0,0,255), get_position(hr_fax, hr_fay), get_position(hr_fbx, hr_fby), 7)
    pygame.draw.circle(screen, (0,0,255), get_position(hr_cx, hr_cy), get_size(100))

    min_ax, min_ay = 0, 0
    min_bx, min_by = 0, 20
    min_cx, min_cy = 0, 0
    min_nax, min_nay = min_ax - min_cx, min_ay - min_cy
    min_nbx, min_nby = min_bx - min_cx, min_by - min_cy
    min_nax_ = min_nax * math.cos(math.radians(minute_hand_angle)) - min_nay * math.sin(math.radians(minute_hand_angle))
    min_nay_ = min_nax * math.sin(math.radians(minute_hand_angle)) + min_nay * math.cos(math.radians(minute_hand_angle))
    min_nbx_ = min_nbx * math.cos(math.radians(minute_hand_angle)) - min_nby * math.sin(math.radians(minute_hand_angle))
    min_nby_ = min_nbx * math.sin(math.radians(minute_hand_angle)) + min_nby * math.cos(math.radians(minute_hand_angle))
    min_fax, min_fay = min_nax_ + min_cx, min_nay_ + min_cy
    min_fbx, min_fby = min_nbx_ + min_cx, min_nby_ + min_cy
    pygame.draw.line(screen, (0,255,0), get_position(min_fax, min_fay), get_position(min_fbx, min_fby), 3)
    pygame.draw.circle(screen, (0,255,0), get_position(min_cx, min_cy), get_size(75))

    sec_ax, sec_ay = 0, -3
    sec_bx, sec_by = 0, 20
    sec_cx, sec_cy = 0, 0
    sec_nax, sec_nay = sec_ax - sec_cx, sec_ay - sec_cy
    sec_nbx, sec_nby = sec_bx - sec_cx, sec_by - sec_cy
    sec_nax_ = sec_nax * math.cos(math.radians(second_hand_angle)) - sec_nay * math.sin(math.radians(second_hand_angle))
    sec_nay_ = sec_nax * math.sin(math.radians(second_hand_angle)) + sec_nay * math.cos(math.radians(second_hand_angle))
    sec_nbx_ = sec_nbx * math.cos(math.radians(second_hand_angle)) - sec_nby * math.sin(math.radians(second_hand_angle))
    sec_nby_ = sec_nbx * math.sin(math.radians(second_hand_angle)) + sec_nby * math.cos(math.radians(second_hand_angle))
    sec_fax, sec_fay = sec_nax_ + sec_cx, sec_nay_ + sec_cy
    sec_fbx, sec_fby = sec_nbx_ + sec_cx, sec_nby_ + sec_cy
    pygame.draw.line(screen, (255,0,0), get_position(sec_fax, sec_fay), get_position(sec_fbx, sec_fby), 1)
    pygame.draw.circle(screen, (255,0,0), get_position(sec_cx, sec_cy), get_size(50))

    indicator_angle = 0
    for i in range(60):
        x1, y1 = 0, 0
        x2, y2 = 0, 22
        x3 = math.cos(math.radians(indicator_angle)) * (x2 - x1) - math.sin(math.radians(indicator_angle)) * (y2 - y1) + x1
        y3 = math.sin(math.radians(indicator_angle)) * (x2 - x1) + math.cos(math.radians(indicator_angle)) * (y2 - y1) + y1
        circle_size = 20
        if (indicator_angle / 6) % 5 == 0:
            draw_text(CLOCK_FONT, screen, get_position(x3, y3), str(abs(int((indicator_angle / 6)/5))), (200,200,200))
        else:
            pygame.draw.circle(screen, (0,255,0), get_position(x3, y3), get_size(circle_size))
        indicator_angle -= 6

    pygame.display.flip()
    clock.tick(30)

pygame.quit()

# Made by Bidhan Acharya