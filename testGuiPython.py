import tkinter as tk
from tkinter import ttk, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import threading
from MeasurementSet import MeasurementSet  # Import MeasurementSet class

class DataSeriesGUI:
    def __init__(self, root, measurement_set: MeasurementSet, experiment_name):
        self.root = root
        self.measurement_set = measurement_set
        self.selected_series = []
        self.experiment_name = experiment_name

        self.root.title(f"Data Series Plotter - {self.experiment_name}")
        self.root.geometry("1200x800")

        # Create main layout
        self.left_frame = tk.Frame(root)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.right_frame = tk.Frame(root)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.stats_frame = tk.Frame(self.right_frame)
        self.stats_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        # Create a Scrollable Frame for Variable Selection
        self.canvas = tk.Canvas(self.left_frame)
        self.scrollbar = tk.Scrollbar(self.left_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Headers
        header_frame = tk.Frame(self.scrollable_frame)
        header_frame.grid(row=0, column=0, columnspan=5, padx=10, pady=5)
        headers = ["Variable", "X+", "X-", "Y+", "Y-"]
        for col, header in enumerate(headers):
            tk.Label(header_frame, text=header, width=12, anchor="center").grid(row=0, column=col, padx=5, pady=5)

        self.series_vars = {}
        self.plot_vars = {}

        for row, series in enumerate(self.measurement_set.data_series_list, start=1):
            var = tk.BooleanVar()
            chk = tk.Checkbutton(self.scrollable_frame, text=series.name, variable=var, anchor="w", width=15)
            chk.grid(row=row, column=0, padx=5, pady=2, sticky="w")
            self.series_vars[series.name] = var

            self.plot_vars[series.name] = []
            for col in range(1, 5):  # Columns 1 to 4 for the four plots
                plot_var = tk.BooleanVar()
                chk = tk.Checkbutton(self.scrollable_frame, variable=plot_var)
                chk.grid(row=row, column=col, padx=15, pady=2, sticky="n")  # Center checkboxes
                self.plot_vars[series.name].append(plot_var)


        # Matplotlib figure with 2x2 subplots
        self.figure, self.axs = plt.subplots(2, 2, figsize=(10, 6))
        titles = ["X - Pos", "X - Neg", "Y - Pos", "Y - Neg"]
        for ax, title in zip(self.axs.flatten(), titles):
            ax.set_title(title)
            ax.set_xlabel("Time (s)")  # Set x-axis label to time
            ax.set_ylabel("Magnetic Flux Field (\muT)")  # Set y-axis label to magnetic induction in microtesla

        
        self.canvas_plot = FigureCanvasTkAgg(self.figure, master=self.right_frame)
        self.canvas_plot.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Statistics selection
        self.stats_options = {stat: tk.BooleanVar() for stat in ["Mean", "Standard Deviation", "Min", "Max"]}
        stats_check_frame = tk.Frame(self.stats_frame)
        stats_check_frame.pack()
        
        for stat_name, var in self.stats_options.items():
            chk = tk.Checkbutton(stats_check_frame, text=stat_name, variable=var)
            chk.pack(side=tk.LEFT)

        self.calc_button = tk.Button(self.stats_frame, text="Calculate Statistics", command=self.calculate_statistics)
        self.calc_button.pack(pady=5)
        
        self.plot_button = tk.Button(self.stats_frame, text="Plot Data", command=self.plot_selected_data)
        self.plot_button.pack(pady=5)
        
        self.close_button = tk.Button(self.stats_frame, text="Close", command=self.root.quit)
        self.close_button.pack(pady=5)

        self.stats_label = tk.Label(self.stats_frame, text="Statistics: ")
        self.stats_label.pack()

    def plot_selected_data(self):
        """Plots the selected data series in the chosen subplots."""
        # Clear plots but keep titles
        titles = ["X - Pos", "X - Neg", "Y - Pos", "Y - Neg"]
        for ax, title in zip(self.axs.flatten(), titles):
            ax.set_title(title)
            ax.set_xlabel("Time (s)")  # Set x-axis label to time
            ax.set_ylabel("Magnetic Flux Field ($\mu$ T)")  # Set y-axis label to magnetic induction in microtesla

        for series in self.measurement_set.data_series_list:
            if self.series_vars[series.name].get():  # Check if series is selected
                times, values = list(series.data_series.keys()), list(series.data_series.values())

                for idx, plot_var in enumerate(self.plot_vars[series.name]):
                    if plot_var.get():  # Check which plot position is selected
                        self.axs[idx // 2, idx % 2].plot(times, values, label=series.name)
                        self.axs[idx // 2, idx % 2].legend(loc="upper right", fontsize=8)

        self.canvas_plot.draw()  # Update the plot


    def calculate_statistics(self):
        """Calculates selected statistics for checked DataSeries."""
        # for ax in self.axs.flatten():
        #     ax.clear()
        
        selected_stats = []
        selected_series = [series for series in self.measurement_set.data_series_list if self.series_vars[series.name].get()]
        
        for series in selected_series:
            times = list(series.data_series.keys())
            values = list(series.data_series.values())
            
            # for idx, plot_var in enumerate(self.plot_vars[series.name]):
            #     if plot_var.get():
            #         self.axs[idx // 2, idx % 2].plot(times, values, label=series.name)
            #         self.axs[idx // 2, idx % 2].legend()
            
            # Compute selected statistics
            stats_result = []
            if self.stats_options["Mean"].get():
                stats_result.append(f"Mean={series.mean_value:.2f}")
            if self.stats_options["Standard Deviation"].get():
                stats_result.append(f"Std={series.std:.2f}")
            if self.stats_options["Min"].get():
                stats_result.append(f"Min={min(values):.2f}")
            if self.stats_options["Max"].get():
                stats_result.append(f"Max={max(values):.2f}")
            
            if stats_result:
                selected_stats.append(f"{series.name}: " + ", ".join(stats_result))
        
        # self.canvas_plot.draw()
        
        # Update statistics label
        self.stats_label.config(text="\n".join(selected_stats))


def load_measurement_set(path, filename):
    return MeasurementSet(path, filename)

def open_gui(path, filename, experiment_name):
    root = tk.Tk()
    measurement_set = load_measurement_set(path, filename)
    gui = DataSeriesGUI(root, measurement_set, experiment_name)
    root.mainloop()