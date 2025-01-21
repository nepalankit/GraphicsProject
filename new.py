import random
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import cos, sin

# Ripple properties: [x, y, radius, opacity]
ripples = []
base_radius = 5
expansion_speed = 0.8  # Speed of ripple expansion
fade_speed = 0.02  # Speed of opacity reduction
paused = False
wind_direction = 0  # Wind direction: negative for left, positive for right

# Raindrops properties: [x, y, speed, dx, size]
raindrops = []

# Cloud properties
cloud_x = 400
cloud_y = 550
cloud_width = 200
cloud_height = 60


def drawCloud():
    glColor3f(0.8, 0.8, 0.8)
    glBegin(GL_POLYGON)
    for angle in range(0, 361, 10):
        x = cloud_x + cos(angle * 3.14159 / 180) * cloud_width // 2
        y = cloud_y + sin(angle * 3.14159 / 180) * cloud_height // 2
        glVertex2f(x, y)
    glEnd()


def drawOceanSurface():
    glColor3f(0.1, 0.3, 0.6)  # Ocean-like blue
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(800, 0)
    glVertex2f(800, 600)
    glVertex2f(0, 600)
    glEnd()


def updateRainAndRipples(value):
    global ripples, raindrops, expansion_speed, fade_speed, paused, wind_direction

    if not paused:
        # Update ripples
        updated_ripples = []
        for ripple in ripples:
            ripple[2] += expansion_speed  # Expand ripple
            ripple[3] -= fade_speed  # Fade ripple
            if ripple[3] > 0:  # Keep visible ripples
                updated_ripples.append(ripple)
        ripples = updated_ripples

        # Update raindrops
        updated_raindrops = []
        for drop in raindrops:
            drop[0] += drop[3] + wind_direction  # Apply horizontal motion
            drop[1] -= drop[2]  # Apply vertical motion

            if drop[1] <= 0:  # If raindrop hits the water
                ripples.append([drop[0], 0, base_radius + drop[4], 1.0])  # Generate larger ripple
            else:
                updated_raindrops.append(drop)
        raindrops = updated_raindrops

        # Generate new raindrops
        for _ in range(random.randint(3, 5)):  # Increase raindrop count
            size = random.uniform(8.0, 20.0)  # Larger drop size
            raindrops.append([
                random.randint(cloud_x - cloud_width // 2, cloud_x + cloud_width // 2),
                cloud_y - cloud_height // 2,
                random.uniform(2.0, 5.0),  # Falling speed
                random.uniform(-1.0, 1.0),  # Horizontal motion variation
                size  # Raindrop size
            ])

    glutPostRedisplay()
    glutTimerFunc(16, updateRainAndRipples, 0)  # Approx. 60 FPS


def display():
    global ripples, raindrops

    glClear(GL_COLOR_BUFFER_BIT)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Draw ocean surface
    drawOceanSurface()

    # Draw the cloud
    drawCloud()

    # Draw raindrops (larger)
    glColor3f(0.5, 0.5, 1.0)
    glBegin(GL_LINES)
    for drop in raindrops:
        # Draw raindrops as circles
        glVertex2f(drop[0], drop[1])
        glVertex2f(drop[0], drop[1] - drop[4])  # Make drop larger

    glEnd()

    # Draw ripples
    for ripple in ripples:
        glColor4f(0.5, 0.8, 1.0, ripple[3])  # Ripple color with opacity
        glBegin(GL_LINE_LOOP)
        for angle in range(0, 361, 5):
            x = ripple[0] + ripple[2] * cos(angle * 3.14159 / 180)
            y = ripple[1] + ripple[2] * sin(angle * 3.14159 / 180)
            glVertex2f(x, y)
        glEnd()

    glutSwapBuffers()


def mouseClick(button, state, x, y):
    global ripples, base_radius
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        ripples.append([x, 600 - y, base_radius, 1.0])  # Add new ripple
        glutPostRedisplay()


def keyboardListener(key, x, y):
    global paused, wind_direction
    if key == b" ":
        paused = not paused  # Toggle pause
    elif key == b"w":
        wind_direction += 0.5  # Increase wind to the right
    elif key == b"a":
        wind_direction -= 0.5  # Increase wind to the left
    elif key == b"s":
        wind_direction = 0  # Stop the wind


def specialKey(key, x, y):
    global expansion_speed
    if key == GLUT_KEY_UP:
        expansion_speed += 0.2  # Increase ripple speed
    elif key == GLUT_KEY_DOWN:
        expansion_speed = max(0.2, expansion_speed - 0.2)  # Decrease ripple speed


# Initialization
glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(800, 600)
glutCreateWindow(b"Interactive Rain, Wind, and Ripples Simulation")

glClearColor(0.0, 0.0, 0.0, 0.0)
gluOrtho2D(0, 800, 0, 600)

glutDisplayFunc(display)
glutMouseFunc(mouseClick)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKey)
glutTimerFunc(0, updateRainAndRipples, 0)

glutMainLoop()
