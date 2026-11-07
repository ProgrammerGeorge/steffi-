import cv2
import numpy as np
import turtle
import os


image_path = "sap.png"


LOGO_COLOR = (0, 0, 0)

BACKGROUND_COLOR = "white"
PEN_SIZE = 1


TURTLE_SPEED = 5
SCREEN_DELAY = 20


if not os.path.exists(image_path):
    raise FileNotFoundError(
        f"Image '{image_path}' not found. "
        "Place lp.jpeg in the same folder as this Python file."
    )

img = cv2.imread(image_path)

if img is None:
    raise ValueError(f"Could not load image: {image_path}")

HEIGHT, WIDTH = img.shape[:2]

print(f"Image loaded successfully: {WIDTH} x {HEIGHT}")


gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

_, mask = cv2.threshold(
    gray,
    150,
    255,
    cv2.THRESH_BINARY_INV
)

contours, hierarchy = cv2.findContours(
    mask,
    cv2.RETR_CCOMP,
    cv2.CHAIN_APPROX_SIMPLE
)

if hierarchy is None or not contours:
    raise ValueError("No logo contours detected. Check your image.")

hierarchy = hierarchy[0]


contour_pairs = list(zip(contours, hierarchy))

contour_pairs.sort(
    key=lambda item: cv2.boundingRect(item[0])[0]
)


screen = turtle.Screen()

screen.setup(
    width=min(WIDTH + 100, 1800),
    height=min(HEIGHT + 100, 1000)
)

screen.title("Python Turtle Graphics")
screen.bgcolor(BACKGROUND_COLOR)
screen.colormode(255)


screen.tracer(1, SCREEN_DELAY)



t = turtle.Turtle()

t.shape("turtle")
t.speed(TURTLE_SPEED)
t.pensize(PEN_SIZE)
t.hideturtle()


def to_turtle_coords(x, y):
    tx = x - WIDTH / 2
    ty = HEIGHT / 2 - y

    return tx, ty



def draw_contour(cnt, color):
    """Draw and fill one contour using Turtle."""

    if len(cnt) < 3:
        return

    points = cnt[:, 0, :]

    # Move to the starting point
    start_x, start_y = points[0]

    t.penup()
    t.goto(to_turtle_coords(start_x, start_y))

    t.color(color)
    t.pendown()

    t.begin_fill()


    for point in points[1:]:
        x, y = point
        t.goto(to_turtle_coords(x, y))

    t.goto(to_turtle_coords(start_x, start_y))

    t.end_fill()
    t.penup()



print("Drawing STEFFI ...")

for cnt, h in contour_pairs:


    if cv2.contourArea(cnt) < 10:
        continue


    if h[3] == -1:
        draw_contour(cnt, LOGO_COLOR)


for cnt, h in contour_pairs:

    if cv2.contourArea(cnt) < 10:
        continue


    if h[3] != -1:
        draw_contour(cnt, BACKGROUND_COLOR)



t.hideturtle()

screen.update()

print("STEFFI drawing completed!")

turtle.done()
