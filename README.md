# Enhanced Water Ripple Simulation

This project simulates water ripples using OpenGL and Python. It was developed as a mini-project for a Computer Graphics course.  The simulation allows for interactive manipulation of wave properties and includes features like rain simulation and user-created ripples.

## Features

* **Realistic Ripple Propagation:** Simulates wave propagation based on a grid-based approach.
* **Damping:**  Wave energy dissipates over time, creating a more natural effect.
* **Interactive Controls:**
    * **Mouse Click:** Creates a ripple at the cursor's position.
    * **Spacebar:** Pauses and resumes the simulation.
    * **'r' Key:** Toggles rain mode on/off.
    * **'c' Key:** Clears the simulation and resets to initial state.
    * **Up Arrow:** Increases wave propagation speed.
    * **Down Arrow:** Decreases wave propagation speed.
    * **Right Arrow:** Increases rain intensity.
    * **Left Arrow:** Decreases rain intensity.
* **Rain Simulation:**  Simulates raindrops impacting the water surface.
* **Adjustable Parameters:** Wave speed, damping factor, and rain intensity can be modified.

## Requirements

* Python 3.x
* PyOpenGL
* NumPy
* FreeGLUT (or equivalent OpenGL Utility Toolkit)

## Installation

1. Install required libraries using pip:
```bash
pip install pyopengl numpy
