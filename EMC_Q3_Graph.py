# EMC_Q3_Graph.py
"""
Creates a list of 150 iterative formula results for the radius, velocity, and pressure acting on the shell of a Cepheid variable star.
"""

import math
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import numpy as np

# Constants
INITIAL_MASS = 1e31  # Initial mass of a typical Cepheid variable star (kg)
INITIAL_SURFACE_MASS = 1e26  # Initial mass of the surface layer of the star (kg)
INITIAL_RADIUS = 1.7e10  # Initial radius of the star (m)
INITIAL_VELOCITY = 0  # Initial velocity of the surface layer (m/s)
INITIAL_PRESSURE = 56000  # Initial pressure acting on the surface layer (N/m²)
TIME_INTERVAL = 1e4  # Time interval of iteration (s)
GRAVITY_CONSTANT = 6.67430e-11  # Gravitational constant on Earth

# Functions
def calculate_properties():
    data = {"velocity": [], "radius": [], "pressure": []}
    time = [TIME_INTERVAL * i for i in range(1, 151)]

    vi, ri, Pi = INITIAL_VELOCITY, INITIAL_RADIUS, INITIAL_PRESSURE

    for i in range(1, 151):
        vf = vi + (((4 * math.pi * (ri**2) * Pi) / INITIAL_SURFACE_MASS) - ((GRAVITY_CONSTANT * INITIAL_MASS) / ri**2)) * TIME_INTERVAL
        rf = ri + (vf * TIME_INTERVAL)
        Pf = Pi * ((ri / rf)**(5))

        data["velocity"].append(vf)
        data["radius"].append(rf)
        data["pressure"].append(Pf)

        vi, ri, Pi = vf, rf, Pf

    return time, data

def plot_properties(time, data):
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))

    # Plot 1: Pressure vs. Time
    axs[0].plot(time, data["pressure"], label="Pressure (N/m²)", color="blue")
    axs[0].set_xlabel("Time (s)")
    axs[0].set_ylabel("Pressure (N/m²)")
    axs[0].set_title("Pressure")
    axs[0].legend()
    axs[0].yaxis.set_major_formatter(ScalarFormatter(useMathText=True))

    # Plot 2: Radius vs. Time
    axs[1].plot(time, data["radius"], label="Radius (m)", color="green")
    axs[1].set_xlabel("Time (s)")
    axs[1].set_ylabel("Radius (m)")
    axs[1].set_title("Radius")
    axs[1].legend()
    axs[1].yaxis.set_major_formatter(ScalarFormatter(useMathText=True))

    # Plot 3: Velocity vs. Time
    axs[2].plot(time, data["velocity"], label="Velocity (m/s)", color="red")
    axs[2].set_xlabel("Time (s)")
    axs[2].set_ylabel("Velocity (m/s)")
    axs[2].set_title("Velocity")
    axs[2].legend()
    axs[2].yaxis.set_major_formatter(ScalarFormatter(useMathText=True))

    plt.tight_layout()
    plt.show()

def find_period(time, data):
    radius_data = data["radius"]
    threshold = INITIAL_RADIUS  # The threshold value is the initial radius

    crossings = []  # Store the times when the radius crosses the threshold in a positive direction
    prev_radius = radius_data[0]

    for t, radius in zip(time, radius_data):
        if radius > threshold and prev_radius <= threshold:
            crossings.append(t)
        prev_radius = radius

    if len(crossings) < 2:
        return None  # Insufficient data points to calculate the period

    time_intervals = [crossings[i] - crossings[i - 1] for i in range(1, len(crossings))]
    period = np.mean(time_intervals)

    return period

if __name__ == "__main__":
    time, data = calculate_properties()
    plot_properties(time, data)

    average_radius = np.mean(data["radius"])
    print(f'Average radius: {average_radius} m.')

    period = find_period(time, data)
    if period is not None:
        print(f'Period (T) of the radius oscillation: {period} seconds, or {period/86400} days')
    else:
        print('Unable to calculate the period with the available data points.')
