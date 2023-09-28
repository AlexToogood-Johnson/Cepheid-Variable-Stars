# Cepheid Variable Star Simulation

This project simulates the behavior of a Cepheid variable star by allowing users to adjust various initial parameters and visualize the star's properties over time.

## Project Description

Cepheid variable stars are important astronomical objects used to measure cosmic distances. This simulation allows users to explore how changing the initial conditions of a Cepheid star affects its behavior. The simulation covers three main properties:

1. **Radius**: The radius of the star over time.
2. **Velocity**: The velocity of the star's surface over time.
3. **Pressure**: The pressure at the star's surface over time.

Users can adjust the following initial parameters via sliders:

- **Initial Mass (kg)**: The mass of the star.
- **Initial Surface Mass (kg)**: The mass of the star's surface.
- **Initial Radius (m)**: The initial radius of the star.
- **Gamma (ᵞ)**: The initial velocity of the gamma constant.
- **Initial Pressure (N/m²)**: The initial pressure at the star's surface.

## How to Use

1. Run the simulation by executing the Python script.
2. Adjust the sliders to change the initial parameters of the Cepheid star.
3. Click the "Update" button to refresh the graph after changing parameters.
4. Observe how changing the parameters affects the star's behavior on the graphs.
5. Click the "Reset" button to revert all parameters to their default values.

## Dependencies

This project uses the following libraries and tools:

- Python 3
- Tkinter: Used for creating the GUI interface.
- NumPy: Used for numerical operations.
- Matplotlib: Used for plotting graphs.

## Project Structure

- `app.py`: The main Python script that runs the Cepheid star simulation.
- `README.md`: This documentation file.
- `LICENSE`: The project's open-source license.
- `requirements.txt`: A list of project dependencies.

## Installation and Usage

1. Install the required libraries using pip:

   ```bash
   pip install -r requirements.txt
