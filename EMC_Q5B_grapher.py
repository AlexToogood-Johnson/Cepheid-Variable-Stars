#EMC_Q5B_grapher.py
"""Creates a graphical calculator that plots the radius, velocity and pressure of a Cepheid variable star
based on how the initial starting values change"""

import sys
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QSlider,
    QLabel,
    QPushButton,
    QHBoxLayout,
)
from PyQt5.QtCore import Qt

# Constants
DEFAULT_INITIAL_MASS = 1e31
DEFAULT_INITIAL_SURFACE_MASS = 1e26
DEFAULT_INITIAL_RADIUS = 1.7e10
DEFAULT_INITIAL_VELOCITY = 0
DEFAULT_INITIAL_PRESSURE = 56000
TIME_INTERVAL = 1e4
GRAVITY_CONSTANT = 6.67430e-11

# Function to perform the simulation
def simulate_properties(initial_mass, initial_surface_mass, initial_radius, initial_velocity, initial_pressure):
    data = {"velocity": [], "radius": [], "pressure": []}
    time = [TIME_INTERVAL * i for i in range(1, 151)]

    vi, ri, Pi = initial_velocity, initial_radius, initial_pressure

    for _ in range(1, 151):
        vf = vi + (
            ((4 * math.pi * (ri ** 2) * Pi) / initial_surface_mass)
            - ((GRAVITY_CONSTANT * initial_mass) / ri ** 2)
        ) * TIME_INTERVAL
        rf = ri + (vf * TIME_INTERVAL)
        Pf = Pi * ((ri / rf) ** 5)

        data["velocity"].append(vf)
        data["radius"].append(rf)
        data["pressure"].append(Pf)

        vi, ri, Pi = vf, rf, Pf

    return time, data

# PyQt5 Application
class CepheidApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Cepheid Variable Star Simulation")
        self.setGeometry(100, 100, 1600, 800)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        sliders = {
            "Initial Mass (kg)": DEFAULT_INITIAL_MASS,
            "Initial Surface Mass (kg)": DEFAULT_INITIAL_SURFACE_MASS,
            "Initial Radius (m)": DEFAULT_INITIAL_RADIUS,
            "Initial Velocity (m/s)": DEFAULT_INITIAL_VELOCITY,
            "Initial Pressure (N/m²)": DEFAULT_INITIAL_PRESSURE,
        }

        self.slider_widgets = {}

        slider_layout = QVBoxLayout()

        for label, default_value in sliders.items():
            slider, label_widget = self.create_slider(label, 0.5, 1.5, 1.0)
            slider.setValue(100)
            self.slider_widgets[label] = slider
            slider.valueChanged.connect(self.refresh_graphs)
            slider_layout.addWidget(label_widget)
            slider_layout.addWidget(slider)

        self.reset_button = QPushButton("Reset", self)
        self.reset_button.clicked.connect(self.reset_values)
        
        slider_layout.addWidget(self.reset_button)
        self.layout.addLayout(slider_layout)

        self.figure, self.ax = plt.subplots(1, 3, figsize=(20, 6))
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        for ax in self.ax:
            ax.yaxis.set_major_formatter(plt.ScalarFormatter(useMathText=True))

        self.figure.subplots_adjust(wspace=0.3)

        self.time, self.data = simulate_properties(
            DEFAULT_INITIAL_MASS,
            DEFAULT_INITIAL_SURFACE_MASS,
            DEFAULT_INITIAL_RADIUS,
            DEFAULT_INITIAL_VELOCITY,
            DEFAULT_INITIAL_PRESSURE,
        )

        self.update_graphs()

    def create_slider(self, label_text, min_value, max_value, initial_value):
        slider = QSlider(Qt.Horizontal)
        slider.setRange(int(min_value * 100), int(max_value * 100))
        slider.setValue(int(initial_value * 100))
        slider.setTickInterval(1)
        slider.setTickPosition(QSlider.TicksBelow)

        def update_label(value):
            multiplier = value / 100.0
            label_widget.setText(f"{label_text}: {multiplier:.2f}")

        slider.valueChanged.connect(update_label)

        label_widget = QLabel(f"{label_text}: {initial_value:.2f}")

        return slider, label_widget

    def refresh_graphs(self):
        # Extract values from sliders
        initial_mass = self.slider_widgets["Initial Mass (kg)"].value() / 100.0 * DEFAULT_INITIAL_MASS
        initial_surface_mass = self.slider_widgets["Initial Surface Mass (kg)"].value() / 100.0 * DEFAULT_INITIAL_SURFACE_MASS
        initial_radius = self.slider_widgets["Initial Radius (m)"].value() / 100.0 * DEFAULT_INITIAL_RADIUS
        initial_velocity = self.slider_widgets["Initial Velocity (m/s)"].value() / 100.0 * DEFAULT_INITIAL_VELOCITY
        initial_pressure = self.slider_widgets["Initial Pressure (N/m²)"].value() / 100.0 * DEFAULT_INITIAL_PRESSURE

        # Update simulation data
        self.time, self.data = simulate_properties(initial_mass, initial_surface_mass, initial_radius, initial_velocity, initial_pressure)

        # Update graphs
        self.update_graphs()

    def update_graphs(self):
        self.figure.clf()

        colors = ['blue', 'green', 'red']

        for i, var_name in enumerate(["radius", "velocity", "pressure"]):
            ax = self.figure.add_subplot(1, 3, i + 1)
            ax.plot(self.time, self.data[var_name], color=colors[i])
            ax.set_xlabel("Time (s)")
            ax.set_title(var_name.capitalize())

        self.canvas.draw()

    def reset_values(self):
        # Reset sliders to default values
        for label, slider in self.slider_widgets.items():
            slider.setValue(100)

        # Reset simulation data to default values
        self.time, self.data = simulate_properties(
            DEFAULT_INITIAL_MASS,
            DEFAULT_INITIAL_SURFACE_MASS,
            DEFAULT_INITIAL_RADIUS,
            DEFAULT_INITIAL_VELOCITY,
            DEFAULT_INITIAL_PRESSURE,
        )

        # Update graphs
        self.update_graphs()

def main():
    app = QApplication(sys.argv)
    ex = CepheidApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
