"""
Enhanced Water Ripple Simulation

Keyboard Controls:
- Space (' '): Toggle pause/play
- 'r': Toggle rain mode
- 'c': Clear/reset the simulation

Special Key Controls:
- UP Arrow: Increase wave speed
- DOWN Arrow: Decrease wave speed
- RIGHT Arrow: Increase rain intensity
- LEFT Arrow: Decrease rain intensity

Mouse Controls:
- Left Click: Add ripple at cursor position
"""

import numpy as np  # Numerical library for efficient array computations.
import random  # For generating random numbers for the rain effect.
from OpenGL.GL import *  # OpenGL core functionalities.
from OpenGL.GLU import *  # OpenGL Utility Library for higher-level functions.
from OpenGL.GLUT import *  # OpenGL Utility Toolkit for windowing and input handling.

# WaterSimulation class handles wave mechanics and parameters.
class WaterSimulation:
    def __init__(self, width=800, height=600):
        self.width = width  # Width of the simulation window.
        self.height = height  # Height of the simulation window.
        self.resolution = 200  # Grid resolution for simulating the water surface.
        self.current_wave = np.zeros((self.resolution, self.resolution))  # Current wave heights.
        self.previous_wave = np.zeros((self.resolution, self.resolution))  # Previous wave heights.
        self.damping = 0.015  # Damping factor to dissipate wave energy.
        self.wave_speed = 0.3  # Speed of wave propagation.
        self.paused = False  # Paused state of the simulation.
        self.rain_mode = False  # Rain mode toggle.
        self.rain_intensity = 3  # Number of raindrops per frame in rain mode.

    def add_drop(self, x, y):
        grid_x = int(x / self.width * (self.resolution - 1))
        grid_y = int(y / self.height * (self.resolution - 1))
        if 0 <= grid_x < self.resolution and 0 <= grid_y < self.resolution:
            self.current_wave[grid_y, grid_x] += 3.0  # Adds energy to the grid point.

    def simulate_rain(self):
        if not self.rain_mode or self.paused:
            return
        for _ in range(self.rain_intensity):
            x = random.uniform(0, self.width)
            y = random.uniform(0, self.height)
            self.add_drop(x, y)

    def update_waves(self):
        if self.paused:
            return
        next_wave = np.zeros_like(self.current_wave)
        for y in range(1, self.resolution - 1):
            for x in range(1, self.resolution - 1):
                neighbors = (
                    self.current_wave[y - 1, x] +
                    self.current_wave[y + 1, x] +
                    self.current_wave[y, x - 1] +
                    self.current_wave[y, x + 1]
                ) * 0.25
                next_wave[y, x] = (
                    2 * self.current_wave[y, x] -
                    self.previous_wave[y, x] +
                    self.wave_speed * (neighbors - self.current_wave[y, x])
                )
        self.previous_wave = self.current_wave
        self.current_wave = next_wave * (1 - self.damping)

    def reset(self):
        self.current_wave.fill(0)
        self.previous_wave.fill(0)
        self.rain_mode = False

# Display function to render the simulation.
def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0.1, 0.2, 0.4)
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(water_sim.width, 0)
    glVertex2f(water_sim.width, water_sim.height)
    glVertex2f(0, water_sim.height)
    glEnd()

    glPointSize(3)
    glBegin(GL_POINTS)
    for y in range(water_sim.resolution):
        for x in range(water_sim.resolution):
            screen_x = x / (water_sim.resolution - 1) * water_sim.width
            screen_y = y / (water_sim.resolution - 1) * water_sim.height
            wave_height = abs(water_sim.current_wave[y, x])
            intensity = min(wave_height * 4, 1.0)
            glColor3f(0.2 + 0.8 * intensity, 0.5 + 0.5 * intensity, 0.7 + 0.3 * intensity)
            glVertex2f(screen_x, screen_y)
    glEnd()

    water_sim.update_waves()
    water_sim.simulate_rain()
    glutSwapBuffers()

# Handles mouse clicks for adding ripples.
def mouse_click(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        water_sim.add_drop(x, water_sim.height - y)

# Handles keyboard inputs for toggling features.
def keyboard(key, x, y):
    global water_sim
    if key == b' ':
        water_sim.paused = not water_sim.paused
    elif key == b'r':
        water_sim.rain_mode = not water_sim.rain_mode
    elif key == b'c':
        water_sim.reset()

# Handles special keys for adjusting parameters.
def special_keys(key, x, y):
    global water_sim
    if key == GLUT_KEY_UP:
        water_sim.wave_speed = min(water_sim.wave_speed + 0.05, 1.0)
    elif key == GLUT_KEY_DOWN:
        water_sim.wave_speed = max(water_sim.wave_speed - 0.05, 0.05)
    elif key == GLUT_KEY_RIGHT:
        water_sim.rain_intensity = min(water_sim.rain_intensity + 1, 10)
    elif key == GLUT_KEY_LEFT:
        water_sim.rain_intensity = max(water_sim.rain_intensity - 1, 1)

# Main function to initialize the simulation.
def main():
    global water_sim

    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"Enhanced Water Ripple Simulation")

    glClearColor(0.0, 0.0, 0.0, 0.0)
    gluOrtho2D(0, 800, 0, 600)

    water_sim = WaterSimulation()

    glutDisplayFunc(display)
    glutIdleFunc(display)
    glutMouseFunc(mouse_click)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special_keys)

    glutMainLoop()

if __name__ == "__main__":
    main()
