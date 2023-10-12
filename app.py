#app.py
"""A graphical calculator that plots the radius, velocity and pressure of a Cepheid variable star"""

########## Imports ##########

import math
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from itertools import cycle
import numpy as np
import locale

########## Constants ##########

DEFAULT_MASS = 1e31
DEFAULT_SURFACE_MASS = 1e26
DEFAULT_RADIUS = 1.7e10
DEFAULT_VELOCITY = 0
DEFAULT_PRESSURE = 56000
DEFAULT_GAMMA = 5/3
TIME_INTERVAL = 1e4
GRAVITY_CONSTANT = 6.67430e-11

########## Functions ##########

def add_char(number):
    """Inserts a comma every 3 digits in a number"""

    locale.setlocale(locale.LC_ALL, '')
    return locale.format_string("%d", number, grouping=True)

def simulate_properties(initial_mass, initial_surface_mass, initial_radius, initial_pressure, gamma):
    """Calculates the properties of the star based on how the initial starting values change"""

    data = {"velocity": [], "radius": [], "pressure": []}
    time = [TIME_INTERVAL * i for i in range(1, 151)]

    vi, ri, Pi = DEFAULT_VELOCITY, initial_radius, initial_pressure

    for _ in range(1, 151):
        vf = vi + ((4 * math.pi * ri * ri * Pi / initial_surface_mass) - ((GRAVITY_CONSTANT * initial_mass) / ri ** 2)) * TIME_INTERVAL
        rf = ri + (vf * TIME_INTERVAL)
        Pf = Pi * ((ri / rf) ** (3 * gamma))

        data["velocity"].append(vf)
        data["radius"].append(rf)
        data["pressure"].append(Pf)

        vi, ri, Pi = vf, rf, Pf

    return time, data

def show_help():
    tk.messagebox.showinfo("Help", "This is a Cepheid Variable Star Simulation. Adjust the sliders to change the star's properties and click 'Update' to see the changes in the graphs. The graph may break if the values entered are not realistic. Click 'Reset' to reset the sliders to their default values. Click 'Stats' to see the period, average radius and average pressure of the star.")

def show_about():
    tk.messagebox.showinfo("About", "Cepheid Star Simulator\nVersion 1.0\n\nCopyright © 2023 Alex Toogood-Johnson")

class CustomButton(tk.Button):
    """This class is a custom button that changes colour when the mouse hovers over it"""

    def __init__(self, master=None, **kwargs):
        tk.Button.__init__(self, master, **kwargs)
        self.default_bg = self.cget("background")
        self.hover_bg = "light blue"
        self.config(width=30, height=2, relief=tk.GROOVE)
        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)

    def on_hover(self, event):
        self.config(background=self.hover_bg)

    def on_leave(self, event):
        self.config(background=self.default_bg)

class App(tk.Tk):
    """This class is the main application window"""

    def __init__(self) -> None:

        tk.Tk.__init__(self)
        self.title("Cepheid Variable Star Simulater - Made by Alex Toogood-Johnson")
        self.configure(bg="white")
        self.resizable(False, False)

        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)
        self.menu_bar.add_command(label="   ")
        self.menu_bar.add_command(label="Exit", command=self.destroy)
        self.menu_bar.add_command(label="Help", command=show_help)
        self.menu_bar.add_command(label="About", command=show_about)
        self.menu_bar.add_command(label="Stats", command=self.show_stats)


        self.slider_frame = tk.Frame(self, bg="white", relief=tk.GROOVE, borderwidth=2, highlightthickness=1)
        self.slider_frame.pack(side=tk.LEFT, padx=30, pady=30, ipadx=30, ipady=30)
        self.slider_styles = {'sliderrelief': 'groove', 'sliderlength': 50, 'length': 300, 'bg': "white", 'borderwidth': 0, 'highlightthickness': 0, 'orient': "horizontal"}

        self.mass_slider = tk.Scale(self.slider_frame, label="Mass (kg)", from_=0.5*DEFAULT_MASS, to=1.5*DEFAULT_MASS, resolution=DEFAULT_MASS/100, **self.slider_styles)
        self.surface_mass_slider = tk.Scale(self.slider_frame, label="Surface Mass (kg)", from_=0.5*DEFAULT_SURFACE_MASS, to=1.5*DEFAULT_SURFACE_MASS, resolution=DEFAULT_SURFACE_MASS/100, **self.slider_styles)
        self.radius_slider = tk.Scale(self.slider_frame, label="Radius (m)", from_=0.5*DEFAULT_RADIUS, to=1.5*DEFAULT_RADIUS, resolution=DEFAULT_RADIUS/100, **self.slider_styles)
        self.gamma_slider = tk.Scale(self.slider_frame, label="Gamma (ᵞ) Constant", from_=0.5*DEFAULT_GAMMA, to=1.5*DEFAULT_GAMMA, resolution=DEFAULT_GAMMA/100, **self.slider_styles)
        self.pressure_slider = tk.Scale(self.slider_frame, label="Pressure (N)", from_=0.5*DEFAULT_PRESSURE, to=1.5*DEFAULT_PRESSURE, resolution=DEFAULT_PRESSURE/100, **self.slider_styles)

        self.mass_slider.set(DEFAULT_MASS)
        self.surface_mass_slider.set(DEFAULT_SURFACE_MASS)
        self.radius_slider.set(DEFAULT_RADIUS)
        self.gamma_slider.set(DEFAULT_GAMMA)
        self.pressure_slider.set(DEFAULT_PRESSURE)

        self.mass_slider.pack(pady=5)
        self.surface_mass_slider.pack(pady=5)
        self.radius_slider.pack(pady=5)
        self.gamma_slider.pack(pady=5)
        self.pressure_slider.pack(pady=5)

        self.update_button = CustomButton(self.slider_frame, text="Update", command=self.update_graphs)
        self.reset_button = CustomButton(self.slider_frame, text="Reset", command=self.reset_values)

        self.update_button.pack(padx=10, pady=30, side=tk.BOTTOM)
        self.reset_button.pack(padx=10, side=tk.BOTTOM)

        self.graph_frame = tk.Frame(self, bg="white", relief=tk.GROOVE, borderwidth=2)
        self.graph_frame.pack(side=tk.RIGHT, padx=30, ipady=2)


        self.figure, self.ax = plt.subplots(1, 3, figsize=(15, 5))

        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(in_=self.graph_frame)


        self.line_colors = cycle(['b', 'g', 'r'])

        self.update_graphs()

    def update_graphs(self):
        """This function is called when the 'Update' button is pressed. It updates the graphs based on the slider values"""

        initial_mass = self.mass_slider.get()
        initial_surface_mass = self.surface_mass_slider.get()
        initial_radius = self.radius_slider.get()
        initial_gamma = self.gamma_slider.get()
        initial_pressure = self.pressure_slider.get()

        time, data = simulate_properties(initial_mass, initial_surface_mass, initial_radius, initial_pressure, initial_gamma)

        for i, var_name in enumerate(["radius", "velocity", "pressure"]):
            self.ax[i].clear()
            self.ax[i].plot(time, data[var_name], label=var_name.capitalize(), color=next(self.line_colors))
            self.ax[i].set_xlabel("Time (s)")
            self.ax[i].set_title(var_name.capitalize())
            self.ax[i].legend()

        self.canvas.draw()

    def reset_values(self):
        """This function is called when the 'Reset' button is pressed. It resets the sliders to their default values and updates the graphs"""

        self.mass_slider.set(DEFAULT_MASS)
        self.surface_mass_slider.set(DEFAULT_SURFACE_MASS)
        self.radius_slider.set(DEFAULT_RADIUS)
        self.gamma_slider.set(DEFAULT_GAMMA)
        self.pressure_slider.set(DEFAULT_PRESSURE)
        self.update_graphs()

    def show_stats(self):
        initial_mass = self.mass_slider.get()
        initial_surface_mass = self.surface_mass_slider.get()
        initial_radius = self.radius_slider.get()
        initial_gamma = self.gamma_slider.get()
        initial_pressure = self.pressure_slider.get()
        
        time, data = simulate_properties(initial_mass, initial_surface_mass, initial_radius, initial_pressure, initial_gamma)

        period = add_char(self.find_period(time, data["radius"]))
        average_radius = add_char(np.mean(data["radius"]))
        average_pressure = add_char(np.mean(data["pressure"]))

        stats_message = f"Period: {period} s\nAverage Radius: {average_radius} m\nAverage Pressure: {average_pressure} N/m²"
        tk.messagebox.showinfo("Statistics", stats_message)

    def find_period(self, time_data, radius_data):
        """Finds out the period of the star"""

        threshold = self.radius_slider.get()

        crossings = []
        prev_radius = radius_data[0]

        for t, radius in zip(time_data, radius_data):
            if radius > threshold and prev_radius <= threshold:
                crossings.append(t)
            prev_radius = radius

        if len(crossings) < 2:
            return "Unable to calculate period"

        time_intervals = [crossings[i] - crossings[i - 1] for i in range(1, len(crossings))]
        period = np.mean(time_intervals)

        return period

if __name__ == "__main__":
    app = App()
    app.mainloop()
