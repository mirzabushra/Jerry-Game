from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

move_speed = 30  # jerry
head_center_x = 150
head_radius = 50
head_center_y = 100
bypass = 0

# new
remove_ball_x = 0
remove_ball_y = 0

brick_list = []
time_interval_brick = 0
current_time_brick = 0

cheese_list = []
time_interval_cheese = 0
current_time_cheese = 0
now = 0  # new
now2 = 0  # new

ball_list = []
time_interval_ball = 0
current_time_ball = 0

play_button_visible = True
current_mode = 0
laser = False  # new

score = 0
health = 5
cheese_collect = 0
highest_score = 0

# new
num_shot = 5
shoot_list = []
shoot_speed = 2.0

max_speed = 20
speed = 0.005

mouse_x = 0
mouse_y = 0

mode = "menu"

##Sohayeb
def circle_Points(cx, cy, x, y):
    glVertex2f(x + cx, y + cy)
    glVertex2f(-x + cx, y + cy)
    glVertex2f(x + cx, -y + cy)
    glVertex2f(-x + cx, -y + cy)
    glVertex2f(y + cx, x + cy)
    glVertex2f(-y + cx, x + cy)
    glVertex2f(y + cx, -x + cy)
    glVertex2f(-y + cx, -x + cy)


def mid_circle(cx, cy, radius):
    d = 1 - radius
    x = 0
    y = radius

    while x <= y:
        circle_Points(cx, cy, x, y)
        x += 1

        if d <= 0:
            d = d + 2 * x + 1
        else:
            y -= 1
            d = d + 2 * (x - y) + 1
        circle_Points(cx, cy, x, y)


################################################## mid point line algo######################    start
##Eushra
def draw_line(x1, y1, x2, y2):
    # find the zone
    zone = find_zone(x1, y1, x2, y2)
    # convert the coordinate values to zone 0
    x1, y1 = convert_to_zone0(x1, y1, zone)
    x2, y2 = convert_to_zone0(x2, y2, zone)
    # mid point line with zone 0
    glBegin(GL_POINTS)
    midpoint_line(x1, y1, x2, y2, zone)
    glEnd()


def find_zone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) > abs(dy):
        if dx >= 0 and dy >= 0:  # zone0
            return 0
        elif dx < 0 and dy >= 0:  # zone3 modified EUSRA
            return 3
        elif dx < 0 and dy < 0:  # zone 4
            return 4
        elif dx >= 0 and dy < 0:  # zone7 modified EUSRA
            return 7
    else:
        if dx >= 0 and dy >= 0:
            return 1
        elif dx < 0 and dy >= 0:
            return 2
        elif dx < 0 and dy < 0:
            return 5
        elif dx >= 0 and dy < 0: #modified EUSRA
            return 6


def convert_to_zone0(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y


def midpoint_line(x1, y1, x2, y2, zone):
    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    E = 2 * dy
    NE = 2 * (dy - dx)
    y = y1

    for x in range(int(x1), int(x2) + 1):  # last iteration will be x2
        cx, cy = convert_to_original(x, y, zone)
        glVertex2f(cx, cy)
        if d > 0:
            d += NE
            y += 1
        else:
            d += E


def convert_to_original(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y


################################################# mid point line algo######################   end

##Sohayeb
def draw_jerry():
    global head_center_x, head_radius, head_center_y
    new_body_radius = 30
    if health == 5:

        body_radius = new_body_radius
    elif 0 < health < 5:
        body_radius = new_body_radius - (5 - health) * 3
        if body_radius < 1:
            body_radius = 1
    elif health == 0:
        body_radius = 0

    # Draw Jerry's head
    glColor3f(1.0, 0.75, 0.8)
    glPointSize(2)
    glBegin(GL_POINTS)
    mid_circle(head_center_x, head_center_y, head_radius)
    glEnd()

    # Draw Jerry's eyes
    eye_radius = 5
    eye_offset = 20

    glColor3f(1.0, 0.75, 0.8)
    glPointSize(2)
    glBegin(GL_POINTS)
    mid_circle(head_center_x - eye_offset, head_center_y + eye_offset, eye_radius)
    glEnd()
    glColor3f(1.0, 0.75, 0.8)
    glPointSize(2)
    glBegin(GL_POINTS)
    mid_circle(head_center_x + eye_offset, head_center_y + eye_offset, eye_radius)
    glEnd()

    # Draw Jerry's mouth (triangle)
    mouth_x1 = head_center_x - 10
    mouth_y1 = head_center_y - 25
    mouth_x2 = head_center_x + 10
    mouth_y2 = head_center_y - 25
    mouth_x3 = head_center_x
    mouth_y3 = head_center_y - 35

    glColor3f(1.0, 0.75, 0.8)

    draw_line(mouth_x1, mouth_y1, mouth_x2, mouth_y2)
    draw_line(mouth_x2, mouth_y2, mouth_x3, mouth_y3)
    draw_line(mouth_x1, mouth_y1, mouth_x3, mouth_y3)

    # Draw three straight lines from the mouth (lighter brown color)

    # Jerry's mustache

    glColor3f(1.0, 0.75, 0.8)
    glPointSize(2)
    draw_line(mouth_x1 - 30, mouth_y1, mouth_x1 - 5,
              mouth_y1)  # why it doesnt work if i wanna draw right point to left point
    draw_line(mouth_x1 - 30, mouth_y1 - 4, mouth_x1 - 5, mouth_y1 - 4)
    draw_line(mouth_x2 + 5, mouth_y2, mouth_x2 + 30, mouth_y2)
    draw_line(mouth_x2 + 5, mouth_y2 - 4, mouth_x2 + 30, mouth_y2 - 4)

    # Draw Jerry's ears (circles)
    ear_radius = 8
    ear_offset = 40

    glColor3f(1.0, 0.75, 0.8)  # Brown color (dark)
    glPointSize(2)
    glBegin(GL_POINTS)
    mid_circle(head_center_x - ear_offset, head_center_y + ear_offset, ear_radius)
    mid_circle(head_center_x + ear_offset, head_center_y + ear_offset, ear_radius)
    glEnd()

    # Draw Jerry's body (circle)

    body_center_x = head_center_x
    body_center_y = head_center_y - 70

    glColor3f(1.0, 0.75, 0.8)  # Brown color (medium)
    glPointSize(2)
    glBegin(GL_POINTS)
    mid_circle(body_center_x, body_center_y, body_radius)
    glEnd()


def initialize():
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, WINDOW_WIDTH, 0.0, WINDOW_HEIGHT, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

##Eusra
def cheese_function():
    for cheese in cheese_list:
        draw_cheese(cheese['x'], cheese['y'], cheese['size'], cheese['color'])
    if not cheese_list:
        new_cheese = {'x': random.randint(0, WINDOW_WIDTH - 20), 'y': WINDOW_HEIGHT, 'size': random.randint(30, 50),
                      'color': (1, 1, 0)}
        cheese_list.append(new_cheese)

##Eusra
def draw_cheese(x, y, size, color):
    glColor3f(*color)
    draw_line(x, y, x + (size) / 3, y + (size / 4) * 3)
    draw_line(x + (size) / 3, y + (size / 4) * 3, x + 2 * (size) / 3, y + (size / 4) * 3)
    draw_line(x + (size / 3), y, x + 2 * (size) / 3, y + (size / 4) * 3)
    draw_line(x, y, x + (size / 3), y)
    draw_line(x + size, y, x + 2 * (size) / 3, y + (size / 4) * 3)  # why doesnt work reverse
    draw_line(x + (size / 3), y, x + size, y)

##Eusra
def brick_function():
    for brick in brick_list:
        draw_brick(brick['x'], brick['y'], brick['size'], brick['color'])
    if not brick_list:
        new_brick = {'x': random.randint(0, WINDOW_WIDTH - 40), 'y': WINDOW_HEIGHT, 'size': random.randint(20, 30),
                     'color': (0.8, 0.4, 0.1)}
        brick_list.append(new_brick)

##Eusra
def draw_brick(x, y, size, color):
    glColor3f(*color)

    # horizontal lines
    draw_line(x, y, x + size, y)
    draw_line(x, y + (size / 4) * 3, x + size, y + (size / 4) * 3)
    draw_line(x + (size / 4), y + size, x + (size / 4) * 5, y + size)

    # vertical lines
    draw_line(x + 0.1, y + 0.1, x, y + (size / 4) * 3)
    draw_line(x + size + 0.1, y + 0.1, x + size, y + (size / 4) * 3)
    draw_line(x + 5 * (size / 4), y + (size / 4), x + 0.5 + (size / 4) * 5, y + size)

    # diagonal line
    draw_line(x + size, y + (size / 4) * 3, x + (size / 4) * 5, y + size)
    draw_line(x + size, y, x + 5 * (size) / 4, y + (size / 4))
    draw_line(x, y + (size / 4) * 3, x + (size / 4), y + size)

##Sohayeb
def draw_ball(cx, cy, radius, color):
    glColor3f(*color)
    glPointSize(2)
    glBegin(GL_POINTS)
    mid_circle(cx, cy, radius)
    mid_circle(cx + 3, cy + 2, radius - 4)
    mid_circle(cx + 3, cy + 2, radius - 5)
    glEnd()
##Sohayeb
def ball_fuction():
    for ball in ball_list:
        draw_ball(ball['cx'], ball['cy'], ball['radius'], ball['color'])
    if not ball_list:
        new_ball = {'cx': random.randint(0, WINDOW_WIDTH - 10), 'cy': WINDOW_HEIGHT, 'radius': random.randint(20, 25),
                    'color': (1.0, 0.0, 0.0)}
        ball_list.append(new_ball)


##EUSRA
def draw_easy():
    x = WINDOW_WIDTH - 510
    y = (WINDOW_HEIGHT - 120) / 2
    size = 40

    glColor3f(1.0, 1.0, 1.0)

    # Draw letter 'E'
    draw_line(x, y, x + size, y)  # lowerline
    draw_line(x, y + size / 2, x + size - 10, y + size / 2)  # middleline
    draw_line(x, y + size, x + size, y + size)  # upperline
    draw_line(x, y, x, y + size)

    # Draw letter 'A'
    draw_line(x + size + 5, y, x + size + 25, y + size)  # left
    draw_line((x + size + 15), y + size / 2, x + size + 35, y + size / 2)  # between
    draw_line(x + size + 25, y + size, x + size + 25 + 20, y)  # right

    # Draw letter 'S'
    draw_line(x + size + 50, y + size, x + size + 90, y + size)  # upeer horizontal
    draw_line(x + size + 50, y + size, x + size + 50, y + size / 2)  # left vertical
    draw_line(x + size + 50, y + size / 2, x + size + 90, y + size / 2)  # middle
    draw_line(x + size + 90, y + size / 2, x + size + 90, y)  # right vertical
    draw_line(x + size + 90, y, x + size + 50, y)  # lower horizontal

    # Draw letter 'Y'
    draw_line(x + size + 95, y + size, x + size + 93 + (45 / 2), y + size / 2)  # \
    draw_line(x + size + 93 + (45 / 2), y + size / 2, x + size + 135, y + size)  # /
    draw_line(x + size + 93 + (45 / 2), y + size / 2, x + size + 93 + (45 / 2), y)

    # Draw boundary box around 'easy'
    draw_line(x - 10, y - 10, x + size + 145, y - 10)  # Bottom
    draw_line(x - 10, y + size + 10, x + size + 145, y + size + 10)  # Top
    draw_line(x - 10, y - 10, x - 10, y + size + 10)  # Left
    draw_line(x + size + 145, y - 10, x + size + 145, y + size + 10)  # Right


##EUSRA
def draw_hard():
    x = WINDOW_WIDTH - 250
    y = (WINDOW_HEIGHT - 120) / 2
    size = 40

    glColor3f(1.0, 1.0, 1.0)

    # Draw letter 'H'
    draw_line(x, y, x, y + size)  # left vertical
    draw_line(x, y + size / 2, x + size, y + size / 2)  # middle horizontal
    draw_line(x + size, y, x + size, y + size)  # right vertical

    # Draw letter 'A'
    draw_line(x + size + 5, y, x + size + 25, y + size)  # /
    draw_line((x + size + 15), y + size / 2, x + size + 35, y + size / 2)  # between
    draw_line(x + size + 25, y + size, x + size + 25 + 20, y)  # right

    # Draw letter 'R'
    draw_line(x + size + 50, y, x + size + 50, y + size)  # left vertical
    draw_line(x + size + 50, y + size, x + size + 80, y + size)  # top horizontal
    draw_line(x + size + 50, y + size / 2, x + size + 80, y + size / 2)  # middle
    draw_line(x + size + 80, y + size, x + size + 80, y + size / 2)  # right vertical
    draw_line(x + size + 50, y + size / 2, x + size + 80, y)

    # Draw letter 'D'
    draw_line(x + size + 90, y, x + size + 90, y + size)  # left vertical
    draw_line(x + size + 90, y, x + size + 105, y)  # top horizontal
    draw_line(x + size + 90, y + size, x + size + 105, y + size)  # bottom horizontal
    draw_line(x + size + 115, y + 10, x + size + 115, y + size - 10)  # right vertical (line)
    draw_line(x + size + 105, y, x + size + 115, y + 10)  # lower bent /
    draw_line(x + size + 115, y + size - 10, x + size + 105, y + size)  # upper bent/

    # Draw a box around the word 'hard'
    draw_line(x - 10, y - 10, x + size + 125, y - 10)  # top horizontal
    draw_line(x - 10, y - 10, x - 10, y + size + 10)  # left vertical
    draw_line(x - 10, y + size + 10, x + size + 125, y + size + 10)  # bottom horizontal
    draw_line(x + size + 125, y - 10, x + size + 125, y + size + 10)  # right vertical

##EUSRA
def draw_game():
    x = WINDOW_WIDTH - 480
    y = WINDOW_HEIGHT - 250
    size = 40

    glColor3f(1.0, 0.5, 0.5)
    # Draw letter 'G'
    draw_line(x, y, x + size, y)  # bottom
    draw_line(x, y, x, y + size)  # left
    draw_line(x, y + size, x + size, y + size)  # top
    draw_line(x + size, y + size / 2, x + size, y)  # right bottom line (small line of G)
    draw_line(x + size, y + size / 2, x + size / 2, y + size / 2)  # middle horizontal

    # Draw letter 'A'
    draw_line(x + size + 5, y, x + size + 25, y + size)  # /
    draw_line((x + size + 15), y + size / 2, x + size + 35, y + size / 2)  # between
    draw_line(x + size + 25, y + size, x + size + 25 + 20, y)  # right

    # Draw letter 'M'
    draw_line(x + size + 50, y, x + size + 50, y + size)  # left
    draw_line(x + size + 50, y + size, x + size + 70, y + size / 2)  # left diagonal \
    draw_line(x + size + 70, y + size / 2, x + size + 90, y + size)  # right diagonal /
    draw_line(x + size + 90, y, x + size + 90, y + size)  # right

    # Draw letter 'E'
    draw_line(x + size + 95, y, x + size + 130, y)  # bottom
    draw_line(x + size + 95, y, x + size + 95, y + size)  # left
    draw_line(x + size + 95, y + size / 2, x + size + 120, y + size / 2)  # middle horizontal
    draw_line(x + size + 95, y + size, x + size + 130, y + size)  # bottom horizontal

    # Draw letter 'M'
    draw_line(x + size + 170, y, x + size + 170, y + size)  # left
    draw_line(x + size + 170, y + size, x + size + 190, y + size / 2)  # left diagonal \
    draw_line(x + size + 190, y + size / 2, x + size + 190 + 20, y + size)  # right diagonal /
    draw_line(x + size + 190 + 20, y, x + size + 190 + 20, y + size)  # right

    # Draw letter 'O'
    draw_line(x + size + 218, y, x + size + 240, y)  # bottom
    draw_line(x + size + 218, y, x + size + 218, y + size)  # left
    draw_line(x + size + 218, y + size, x + size + 240, y + size)  # top
    draw_line(x + size + 240, y + size, x + size + 240, y)  # right

    # Draw letter 'D'
    draw_line(x + size + 240 + 8, y,
              x + size + 240 + 8, y + size)  # left vertical
    draw_line(x + size + 240 + 8, y,
              x + size + 240 + 20, y)  # top horizontal
    draw_line(x + size + 240 + 8, y + size,
              x + size + 240 + 20, y + size)  # bottom horizontal
    draw_line(x + size + 240 + 30, y + 10,
              x + size + 240 + 30, y + size - 10)  # right vertical (line)
    draw_line(x + size + 240 + 20, y,
              x + size + 240 + 30, y + 10)  # lower bent /
    draw_line(x + size + 240 + 30, y + size - 10,
              x + size + 240 + 20, y + size)  # upper bent/

    # Draw letter 'E'
    draw_line(x + size + 240 + 30 + 8, y,
              x + size + 240 + 30 + 8 + 35, y)  # bottom horizontal
    draw_line(x + size + 240 + 30 + 8, y,
              x + size + 240 + 30 + 8, y + size)  # left vertical
    draw_line(x + size + 240 + 30 + 8, y + size / 2,
              x + size + 240 + 30 + 8 + 25, y + size / 2)  # middle horizontal
    draw_line(x + size + 240 + 30 + 8, y + size,
              x + size + 240 + 30 + 8 + 35, y + size)  # top horizontal
    


##EUSRA
def click_easy(x, y):
    global mode
    # Define the coordinates of the boundary box around 'EASY'
    easy_box_x1 = WINDOW_WIDTH - 510 - 10
    easy_box_x2 = WINDOW_WIDTH - 510 + 40 + 25 + 20 + 45 + 45 + 10
    easy_box_y1 = (WINDOW_HEIGHT) / 2 + 10
    easy_box_y2 = (WINDOW_HEIGHT) / 2 + 40 + 28
    print(x,y)

    if easy_box_x1 <= x <= easy_box_x2 and easy_box_y1 <= y <= easy_box_y2:
        # print("Easy mode")
        mode = "easy"

##EUSRA
def click_hard(x, y):
    global mode

    # Define the coordinates of the boundary box around 'EASY'
    x1 = WINDOW_WIDTH - 250 - 10
    x2 = WINDOW_WIDTH - 250 + 40 + 25 + 20 + 45 + 45 + 10
    y1 = (WINDOW_HEIGHT) / 2 + 10
    y2 = (WINDOW_HEIGHT) / 2 + 40 + 28

    if x1 <= x <= x2 and y1 <= y <= y2:
        # print("Hard mode")
        mode = "hard"




##Eusra
def keyboard_special_keys(key, x, y):
    global move_speed, health, current_mode
    if health != 0 and current_mode == 0:
        if key == GLUT_KEY_LEFT:

            move_jerry('left')

        elif key == GLUT_KEY_RIGHT:
            # print("keyboard_special_keys working right")
            move_jerry('right')

##Eusra
def move_jerry(direction):
    global head_center_x, head_radius
    if direction == 'left':
        head_center_x = max(head_radius, head_center_x - move_speed)
    elif direction == 'right':
        head_center_x = min(WINDOW_WIDTH - head_radius, head_center_x + move_speed)
    glutPostRedisplay()


######################################
##Bushra
def update_objects():
    global time_interval_brick, current_time_brick
    global time_interval_cheese, current_time_cheese
    global time_interval_ball, current_time_ball
    global current_mode, play_button_visible
    global head_center_y, head_radius, head_center_x, score, health, max_speed, speed, highest_score, cheese_collect

    current_time_brick = glutGet(GLUT_ELAPSED_TIME)
    current_time_cheese = glutGet(GLUT_ELAPSED_TIME)
    current_time_ball = glutGet(GLUT_ELAPSED_TIME)

    if current_mode == 0 and health != 0:
        # For bricks
        if current_time_brick - time_interval_brick > 3500:  # Adjust time interval as needed
            time_interval_brick = current_time_brick
            add_brick()

        for brick in brick_list:
            brick['y'] -= speed
            if brick['y'] <= 0:
                brick_list.remove(brick)
            if jerry_clash_brick(head_center_y, head_radius, head_center_x, brick):
                brick_list.remove(brick)
                health = 0
                if score < highest_score:
                    print('You Ara A loser')
                    print("can't beat the highest score")
                    print("SCORE:", score)
                    print("CHEESE_COLLECT:", cheese_collect)
                else:
                    print("CONGOOOOO YOU BEAT THE HIGHEST SCORE")
                    print('New Highest_Score:', highest_score)
                    print("CHEESE_COLLECT:", cheese_collect)
            for cheese in cheese_list:
                if cheese_clash_brick(cheese, brick):
                    brick_list.remove(brick)

        # For cheese
        if current_time_cheese - time_interval_cheese > 4300:  # Adjust time interval as needed
            time_interval_cheese = current_time_cheese
            add_cheese()

        for cheese in cheese_list:
            cheese['y'] -= speed
            if cheese['y'] <= 0:
                cheese_list.remove(cheese)
            if jerry_clash_cheese(head_center_y, head_radius, head_center_x, cheese):
                cheese_list.remove(cheese)
                speed = min(speed + 0.05, max_speed)
                # print('speed',speed)
                score += 5
                cheese_collect += 1
                highest_score = max(highest_score, score)
                print('score:', score)
                print("CHEESE_COLLECT:", cheese_collect)

        # For balls
        if current_time_ball - time_interval_ball > 3000:  # Adjust time interval as needed
            time_interval_ball = current_time_ball
            add_ball()
        for ball in ball_list:
            ball['cy'] -= speed
            if ball['cy'] <= 0:
                ball_list.remove(ball)
            if jerry_clash_ball(head_center_y, head_radius, head_center_x, ball):
                ball_list.remove(ball)
                # speed = min(speed+0.001,max_speed)
                health -= 1
                print('health:', health)
            ##newly add
            # for ball in ball_list:
            for cheese in cheese_list:
                if cheese_clash_ball(cheese, ball):
                    ball_list.remove(ball)
            for brick in brick_list:
                if brick_clash_ball(brick, ball):
                    brick_list.remove(brick)

##Minhaj
def jerry_clash_cheese(head_center_y, head_radius, head_center_x, cheese):
    return (
            head_center_x - head_radius < cheese['x'] + cheese['size'] and
            head_center_x + head_radius > cheese['x'] and
            head_center_y - head_radius < cheese['y'] + cheese['size'] and
            head_center_y + head_radius > cheese['y']
    )

##Minhaj
def cheese_clash_brick(cheese, brick):
    return (
            brick['x'] < cheese['x'] + cheese['size'] and
            brick['x'] + brick['size'] > cheese['x'] and
            brick['y'] < cheese['y'] + cheese['size'] and
            brick['y'] + brick['size'] > cheese['y']
    )


# -----------------newly add--------------
##Minhaj
def cheese_clash_ball(cheese, ball):
    return (
            ball['cx'] - ball['radius'] < cheese['x'] + cheese['size'] and
            ball['cx'] + ball['radius'] > cheese['x'] and
            ball['cy'] - ball['radius'] < cheese['y'] + cheese['size'] and
            ball['cy'] + ball['radius'] > cheese['y']
    )

##Minhaj
def brick_clash_ball(brick, ball):
    return (
            ball['cx'] - ball['radius'] < brick['x'] + brick['size'] and
            ball['cx'] + ball['radius'] > brick['x'] and
            ball['cy'] - ball['radius'] < brick['y'] + brick['size'] and
            ball['cy'] + ball['radius'] > brick['y']
    )


# -----------------newly add--------------

##Minhaj
def jerry_clash_ball(head_center_y, head_radius, head_center_x, ball):
    return (
            head_center_x - head_radius < ball['cx'] + ball['radius'] and
            head_center_x + head_radius > ball['cx'] - ball['radius'] and
            head_center_y - head_radius < ball['cy'] + ball['radius'] and
            head_center_y + head_radius > ball['cy'] - ball['radius']
    )

##Minhaj
def jerry_clash_brick(head_center_y, head_radius, head_center_x, brick):
    return (
            head_center_x - head_radius < brick['x'] + brick['size'] and
            head_center_x + head_radius > brick['x'] and
            head_center_y - head_radius < brick['y'] + brick['size'] and
            head_center_y + head_radius > brick['y']
    )

##Bushra
def add_ball():
    new_ball = {'cx': random.randint(50, WINDOW_WIDTH - 50), 'cy': WINDOW_HEIGHT, 'radius': 20,
                'color': (1.0, 0.0, 0.0)}
    ball_list.append(new_ball)

##Bushra
def add_brick():
    new_brick = {'x': random.randint(50, WINDOW_WIDTH - 50), 'y': WINDOW_HEIGHT, 'size': random.randint(30, 50),
                 'color': (0.8, 0.4, 0.1)}
    brick_list.append(new_brick)

##Bushra
def add_cheese():
    new_cheese = {'x': random.randint(0, WINDOW_WIDTH - 10), 'y': WINDOW_HEIGHT, 'size': random.randint(30, 50),
                  'color': (1, 1, 0)}
    cheese_list.append(new_cheese)

##Bushra
def initialize_game(msg=False):
    global brick_list, ball_list, cheese_list, score, health, speed, cheese_collect
    brick_list = []
    ball_list = []
    cheese_list = []
    score = 0
    cheese_collect = 0
    health = 5
    speed = 0.5
    if msg:
        print("Starting Over!!")

    # buttons

##Bushra
def back_button():
    glColor3f(0.0, 1.0, 1.0)
    bx1 = 15  # minimum x value
    bx2 = bx1 + 50  # max x value
    bx_mid = int(bx1 + (bx2 - bx1) / 2)
    by1 = WINDOW_HEIGHT - 60  # y min
    by2 = WINDOW_HEIGHT - 20  # y max
    by_mid = int(by1 + (by2 - by1) / 2)
    draw_line(bx1, by_mid, bx_mid, by2)
    draw_line(bx1, by_mid, bx2, by_mid)
    draw_line(bx1, by_mid, bx_mid, by1)

##Bushra
def play_button():  # bypassing print draw_line
    global bypass, play_button_visible  # new

    play_button_visible = True
    glColor3f(0.7, 1.0, 0.7)
    px1 = WINDOW_WIDTH / 2  # minimum x value
    px2 = px1 + 40  # max x value
    py1 = WINDOW_HEIGHT - 60  # y min
    py2 = WINDOW_HEIGHT - 20  # y max
    py_mid = int(py1 + (py2 - py1) / 2)
    draw_line(px1, py2, px2, py_mid)
    draw_line(px1, py1, px1, py2)  # wrote px1 instead of px1 - 0.0000001
    draw_line(px1, py1, px2, py_mid)

##Bushra
def pause_button():
    global play_button_visible
    play_button_visible = False

    glColor3f(0.7, 1.0, 0.7)
    tx1 = WINDOW_WIDTH / 2  # minimum x value
    tx2 = tx1 + 40  # max x value
    ty1 = WINDOW_HEIGHT - 60  # y min
    ty2 = WINDOW_HEIGHT - 20  # y max

    t_part = int((tx2 - tx1) / 3)

    # print("PAUSED")
    draw_line(tx1 + t_part - 0.001, ty1, tx1 + t_part, ty2)
    draw_line(tx1 + 2 * t_part - 0.0001, ty1, tx1 + 2 * t_part, ty2)

##Bushra
def cross_button():
    glColor3f(1.0, 0.0, 0.0)
    cx1 = int((WINDOW_WIDTH) - 60)  # minimum x value
    cx2 = int((WINDOW_WIDTH) - 20)  # max x value
    cx_mid = int(cx1 + (cx2 - cx1) / 2)
    cy1 = int((WINDOW_HEIGHT) - 60)  # y min
    cy2 = int((WINDOW_HEIGHT) - 20)  # y max
    cy_mid = int(cy1 + (cy2 - cy1) / 2)
    draw_line(cx1, cy1, cx2, cy2)
    draw_line(cx1, cy2, cx2, cy1)

##Bushra
def mouse_click(button, state, mouse_x, mouse_y):
    global mode
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if mode == "menu":
            button_click(mouse_x, mouse_y)
        elif mode == "easy":
            button_click(mouse_x, mouse_y)
        elif mode == "hard":
            button_click(mouse_x, mouse_y)
            check_gun_ball_clash(mouse_x, mouse_y)
        elif click_play_again():
            button_click(mouse_x, mouse_y) 
          
        else:
            pass 

    print(mouse_x,mouse_y,'mouse') 


##Bushra
def button_click(x, y):
    click_easy(x, y)     
    click_hard(x, y)      
    back_button_click(x, y)
    play_button_click(x, y)
    cross_button_click(x, y)
    shooted(x, y)  # new
    check_gun_ball_clash(x, y)  # new
    click_play_again(x, y)

##Bushra
def back_button_click(x, y):
    global speed, mode
    x1, x2 = int(15), int(15 + 50)
    y1, y2 = WINDOW_HEIGHT - 60, WINDOW_HEIGHT - 20
    if x1 <= x <= x2 and y1 <= WINDOW_HEIGHT - y <= y2:
        print("reset")
        mode = "menu"     #EUSRA
        # speed=0.005
        initialize_game(msg=True)

##Bushra
def toggle_play_pause_button():
    global play_button_visible, current_mode
    play_button_visible = not play_button_visible
    current_mode = 0 if play_button_visible else 1

##Bushra
def play_button_click(x, y):
    x1, x2 = WINDOW_WIDTH / 2, int((WINDOW_WIDTH / 2) + 40)
    y1, y2 = WINDOW_HEIGHT - 60, WINDOW_HEIGHT - 20

    if x1 <= x <= x2 and y1 <= WINDOW_HEIGHT - y <= y2:
        # print(speed)#########################################
        toggle_play_pause_button()
        glutPostRedisplay()

##Bushra
def cross_button_click(x, y):
    x1, x2 = int((WINDOW_WIDTH) - 60), int((WINDOW_WIDTH) - 20)
    y1, y2 = WINDOW_HEIGHT - 60, WINDOW_HEIGHT - 20
    if x1 <= x <= x2 and y1 <= WINDOW_HEIGHT - y <= y2:
        print("Goodbye! Score:", score)
        print("CHEESE_COLLECT:", cheese_collect)
        glutLeaveMainLoop()


##Minhaj
def initialize_shooting():  # new
    global head_radius, head_center_y
    for _ in range(num_shot):
        x = head_radius + head_center_y

        shoot_list.append([x, shoot_speed])

##Minhaj
def draw_shots():  # new
    glColor3f(1.0, 1.0, 1.0)
    glPointSize(2)
    glBegin(GL_POINTS)
    for x, _ in shoot_list:
        glVertex2f(x, 0)
    glEnd()

##Minhaj
def shoot_laser():  # new
    global laser, now, now2, remove_ball_x, remove_ball_y, head_center_x, head_center_y, head_radius
    now2 = glutGet(GLUT_ELAPSED_TIME)

    glColor3f(0.0, 1.0, 1.0)
    if laser == True:  # new
        draw_line(head_center_x, head_center_y + head_radius, remove_ball_x, remove_ball_y)
    if now2 - now > 300:  # Adjust time interval as needed
        now = now2
        laser = False

##Minhaj
def gun_clash_ball(mx, my, ball):
    bx1, bx2 = ball['cx'] - ball['radius'], ball['cx'] + ball['radius']
    by1, by2 = ball['cy'] + ball['radius'], ball['cy'] - ball['radius']
    return (
            mx <= bx2 and
            mx >= bx1 and
            my <= by1 and
            my >= by2
    )

##Minhaj
def shooted(x, y):
    global score, health, WINDOW_HEIGHT, ball_list, max_speed, highest_score, cheese_collect
    x1, x2 = int(WINDOW_HEIGHT - 60), int(WINDOW_HEIGHT - 90)
    y1, y2 = int(90), int(60)

    if x2 <= x <= x1 and y2 <= WINDOW_HEIGHT - y <= y1:
        for ball in ball_list:
            if gun_clash_ball(x, WINDOW_HEIGHT - y, ball):
                score += 5
                highest_score = max(highest_score, score)
                print('score:', score)
                print("CHEESE_COLLECT:", cheese_collect)
                ball_list.remove(ball)
                return

##Minhaj
def check_gun_ball_clash(x, y):
    global ball, ball_list, score, laser, remove_ball_x, remove_ball_y, max_speed, highest_score, cheese_collect
    for ball in ball_list:
        if gun_clash_ball(x, WINDOW_HEIGHT - y, ball):
            score += 5
            highest_score = max(highest_score, score)
            print('score:', score)
            print("CHEESE_COLLECT:", cheese_collect)
            laser = True
            remove_ball_x = ball['cx']
            remove_ball_y = ball['cy']
            shoot_laser()
            ball_list.remove(ball)




##Sohayeb
def draw_play_again():
    x = WINDOW_WIDTH - 510
    y = (WINDOW_HEIGHT - 120) / 2 - 100
    size = 40

    glColor3f(1.0, 1.0, 1.0)

    # Draw letter 'P'
    draw_line(x, y, x, y + size)  # Left vertical
    draw_line(x, y + size, x + 20, y + size)  # Lower horizontal
    draw_line(x + 20, y + size, x + 20, y + size / 2)  # Right vertical
    draw_line(x + 20, y + size / 2, x, y + size / 2)  # Middle horizontal

    # Draw letter 'L'
    draw_line(x + 30, y, x + 30, y + size)  # Left vertical
    draw_line(x + 30, y, x + 40, y)  # Lower horizontal

    # Draw letter 'A'
    draw_line(x + 50, y, x + 70, y + size)  # Left
    draw_line((x + 60), y + size / 2, x + 80, y + size / 2)  # Between
    draw_line(x + 70, y + size, x + 90, y)  # Right

    # Draw letter 'Y'
    draw_line(x + 95, y + size, x + 93 + (45 / 2), y + size / 2)  # \
    draw_line(x + 93 + (45 / 2), y + size / 2, x + 135, y + size)  # /
    draw_line(x + 93 + (45 / 2), y + size / 2, x + 93 + (45 / 2), y)

    # Draw letter 'A' for 'AGAIN'
    draw_line(x + 170, y, x + 190, y + size)  # Left
    draw_line((x + 180), y + size / 2, x + 200, y + size / 2)  # Between
    draw_line(x + 190, y + size, x + 210, y)  # Right

    # Draw letter 'G' for 'AGAIN'
    draw_line(x + 220, y, x + 220, y + size)
    draw_line(x + 220, y, x + 240, y)
    draw_line(x + 240, y + size, x + 220, y + size)
    draw_line(x + 230, y + size / 2, x + 240, y + size / 2)
    draw_line(x + 240, y, x + 240, y + size/2)


    # Draw letter 'A' for 'AGAIN'
    draw_line(x + 250, y, x + 270, y + size)  # Left
    draw_line((x + 260), y + size / 2, x + 280, y + size / 2)  # Between
    draw_line(x + 270, y + size, x + 290, y)  # Right

    # Draw letter 'I' for 'AGAIN'
    draw_line(x + 300, y, x + 300, y + size)  # Vertical

    # Draw letter 'N' for 'AGAIN'
    draw_line(x + 310, y, x + 310, y + size)  # Left vertical
    draw_line(x + 310, y + size, x + 330, y)  # Right diagonal
    draw_line(x + 330, y, x + 330, y + size)  # Right vertical

    # Draw boundary box around 'Play Again'
    draw_line(x - 10, y - 10, x + 380, y - 10)  # Bottom
    draw_line(x - 10, y + size + 10, x + 380, y + size + 10)  # Top
    draw_line(x - 10, y - 10, x - 10, y + size + 10)  # Left
    draw_line(x + 380, y - 10, x + 380, y + size + 10)  # Right
##Sohayeb
def click_play_again(x, y):
    global speed, mode
    # Define the coordinates of the boundary box around 'Play Again'
    x1, x2 = WINDOW_WIDTH - 510-10 , WINDOW_WIDTH - 510 + 380
    y1, y2 = WINDOW_HEIGHT - 200, WINDOW_HEIGHT - 160
    print(x,y,'uhuh')

    # Check if the mouse click coordinates are within the boundary box
    if x1 <= x <= x2 and y1 <= y <= y2:
        # Call the initializing_game function to start over
        print("reset")
        mode = "menu"
        initialize_game(msg=True)

##Minhaj
def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) #modified this entire showscreen function (EUSRA)
    if mode == "menu":
        draw_easy()
        draw_hard()
        draw_game()

    elif health != 0 and mode == "easy":
        draw_jerry()
        cheese_function()
        brick_function()
        cross_button()
        back_button()
        if play_button_visible:
            play_button()
        else:
            pause_button()

    elif health != 0 and mode == "hard":
        draw_jerry()
        cheese_function()
        brick_function()
        cross_button()
        back_button()
        ball_fuction()
        shoot_laser()
        draw_shots()
        if play_button_visible:
            play_button()
        else:
            pause_button()

    else:                             
        # Display "Game Over!" and the score
        glColor3f(1.0, 0.0, 0.0)
        glRasterPos2f(WINDOW_WIDTH / 2 - 80, WINDOW_HEIGHT / 2)
        gameOverMsg = "Game Over!"
        for character in gameOverMsg:
            glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(character))

        glColor3f(1.0, 1.0, 1.0)
        glRasterPos2f(WINDOW_WIDTH / 2 - 60, WINDOW_HEIGHT / 2 - 50)
        scoreMsg = "Score: " + str(score)
        for character in scoreMsg:
            glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(character))
    
        draw_play_again()
        
        

            
   
    cross_button()
    back_button()

    glutSwapBuffers()
##Minhaj
def animation(value=None):
    if current_mode == 0:
        if mode == "easy" or mode == "hard":  # added this extra line (EUSRA)
            update_objects()
            glutPostRedisplay()


glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Jerry the Cheese Lover")
glutDisplayFunc(showScreen)
glutIdleFunc(animation)
# glutTimerFunc(0, animation, 0)
glClearColor(0.0, 0.0, 0.0, 0.0)
glutSpecialFunc(keyboard_special_keys)
glutMouseFunc(mouse_click)
glEnable(GL_DEPTH_TEST)
initialize()
initialize_game()
glutMainLoop()