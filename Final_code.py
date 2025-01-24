# Enhanced Water Ripple Simulation
# Controls:
# - Mouse Left-Click: Add a water ripple at the clicked position.
# - Spacebar (' '): Pause or resume the simulation.
# - 'r': Toggle rain mode on/off.
# - Up Arrow: Increase wave speed.
# - Down Arrow: Decrease wave speed.
# - Right Arrow: Increase rain intensity.
# - Left Arrow: Decrease rain intensity.

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
        self.rain_intensity = 5  # Number of raindrops per frame in rain mode.

    def add_drop(self, x, y):
        # Converts screen coordinates to grid indices and adds a ripple.
        grid_x = int(x / self.width * (self.resolution - 1))
        grid_y = int(y / self.height * (self.resolution - 1))
        if 0 <= grid_x < self.resolution and 0 <= grid_y < self.resolution:
            self.current_wave[grid_y, grid_x] += 3.0  # Adds energy to the grid point.

    def simulate_rain(self):
        # Simulates random raindrops when rain mode is active.
        if not self.rain_mode:
            return
        for _ in range(self.rain_intensity):
            x = random.uniform(0, self.width)  # Random x-coordinate.
            y = random.uniform(0, self.height)  # Random y-coordinate.
            self.add_drop(x, y)  # Adds a drop at the random location.

    def update_waves(self):
        # Updates the wave grid using a numerical ripple algorithm.
        if self.paused:  # Skip updates if paused.
            return
        next_wave = np.zeros_like(self.current_wave)  # New wave grid.
        for y in range(1, self.resolution - 1):
            for x in range(1, self.resolution - 1):
                # Compute the average height of neighboring points.
                neighbors = (
                    self.current_wave[y - 1, x] +
                    self.current_wave[y + 1, x] +
                    self.current_wave[y, x - 1] +
                    self.current_wave[y, x + 1]
                ) * 0.25
                # Update the wave height based on the wave equation.
                next_wave[y, x] = (
                    2 * self.current_wave[y, x] -
                    self.previous_wave[y, x] +
                    self.wave_speed * (neighbors - self.current_wave[y, x])
                )
        self.previous_wave = self.current_wave  # Store the current wave as the previous.
        self.current_wave = next_wave * (1 - self.damping)  # Apply damping.

# Display function to render the simulation.
def display():
    glClear(GL_COLOR_BUFFER_BIT)  # Clear the screen.

    # Draw the background.
    glColor3f(0.1, 0.2, 0.4)  # Dark blue color.
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(water_sim.width, 0)
    glVertex2f(water_sim.width, water_sim.height)
    glVertex2f(0, water_sim.height)
    glEnd()

    # Draw the waves as points with color gradients.
    glPointSize(3)
    glBegin(GL_POINTS)
    for y in range(water_sim.resolution):
        for x in range(water_sim.resolution):
            # Convert grid indices to screen coordinates.
            screen_x = x / (water_sim.resolution - 1) * water_sim.width
            screen_y = y / (water_sim.resolution - 1) * water_sim.height
            wave_height = abs(water_sim.current_wave[y, x])  # Get the wave height.
            intensity = min(wave_height * 4, 1.0)  # Normalize intensity for color scaling.
            glColor3f(
                0.2 + 0.8 * intensity,  # Light blue gradient.
                0.5 + 0.5 * intensity,  # Aqua tones.
                0.7 + 0.3 * intensity   # Depth effect.
            )
            glVertex2f(screen_x, screen_y)  # Render the point.
    glEnd()

    water_sim.update_waves()  # Update the wave simulation.
    water_sim.simulate_rain()  # Add raindrops if rain mode is active.
    glutSwapBuffers()  # Swap the front and back buffers.

# Handles mouse clicks for adding ripples.
def mouse_click(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        water_sim.add_drop(x, water_sim.height - y)  # Add drop at the clicked position.

# Handles keyboard inputs for toggling features.
def keyboard(key, x, y):
    global water_sim
    if key == b' ':
        water_sim.paused = not water_sim.paused  # Toggle pause.
    elif key == b'r':
        water_sim.rain_mode = not water_sim.rain_mode  # Toggle rain mode.

# Handles special keys for adjusting parameters.
def special_keys(key, x, y):
    global water_sim
    if key == GLUT_KEY_UP:
        water_sim.wave_speed = min(water_sim.wave_speed + 0.05, 1.0)  # Increase wave speed.
    elif key == GLUT_KEY_DOWN:
        water_sim.wave_speed = max(water_sim.wave_speed - 0.05, 0.05)  # Decrease wave speed.
    elif key == GLUT_KEY_RIGHT:
        water_sim.rain_intensity = min(water_sim.rain_intensity + 1, 20)  # Increase rain intensity.
    elif key == GLUT_KEY_LEFT:
        water_sim.rain_intensity = max(water_sim.rain_intensity - 1, 1)  # Decrease rain intensity.

# Main function to initialize the simulation.
def main():
    global water_sim

    glutInit()  # Initialize GLUT.
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)  # Set up a double-buffered RGB window.
    glutInitWindowSize(800, 600)  # Set the window size.
    glutCreateWindow(b"Enhanced Water Ripple Simulation")  # Create the window with a title.

    glClearColor(0.0, 0.0, 0.0, 0.0)  # Set the background clear color.
    gluOrtho2D(0, 800, 0, 600)  # Set up a 2D orthographic projection.

    water_sim = WaterSimulation()  # Create the water simulation instance.

    # Register GLUT callback functions.
    glutDisplayFunc(display)
    glutIdleFunc(display)
    glutMouseFunc(mouse_click)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special_keys)

    glutMainLoop()  # Enter the GLUT main loop.

# Run the program.
if __name__ == "__main__":
    main()
