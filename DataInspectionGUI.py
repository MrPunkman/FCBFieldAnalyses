import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import threading
from MeasurementSet import MeasurementSet  # Import MeasurementSet class
from plot_template import create_plot_template  # Import the template
import os

class DataSeriesGUI:
    def __init__(self, root, measurement_set: MeasurementSet, path, experiment_name):
        self.root = root
        self.measurement_set = measurement_set
        self.selected_series = []
        self.experiment_name = experiment_name
        self.path = path

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
        header_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=5)
        headers = ["Variable", "Plot Area"]
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
            # New drop-down menus for plot selection
            plot_options = ['None', "X - Pos", "X - Neg", "Y - Pos", "Y - Neg"]
            plot_menu = ttk.Combobox(self.scrollable_frame, values=plot_options, state="readonly")
            plot_menu.set('None')  # Default option
            plot_menu.grid(row=row, column=1, padx=5, pady=2)

            # Store plot selection in the dictionary
            self.plot_vars[series.name] = plot_menu
            plot_menu.bind("<<ComboboxSelected>>", self.update_plot)

        # Create plot using the template
        self.figure, self.axs = create_plot_template()

        self.canvas_plot = FigureCanvasTkAgg(self.figure, master=self.right_frame)
        self.canvas_plot.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Statistics selection - Place checkboxes above buttons
        self.stats_check_frame = tk.Frame(self.stats_frame)
        self.stats_check_frame.pack(pady=10)

        self.stats_options = {stat: tk.BooleanVar() for stat in ["Mean", "Standard Deviation", "Min", "Max"]}

        # Create the checkboxes for statistics
        for stat_name, var in self.stats_options.items():
            chk = tk.Checkbutton(self.stats_check_frame, text=stat_name, variable=var)
            chk.pack(side=tk.LEFT, padx=10)

        # Button frame (for Calculate Statistics and Delete Outliers)
        button_frame = tk.Frame(self.stats_frame)
        button_frame.pack(pady=5)

        # Place the buttons side by side in the button_frame
        self.calc_button = tk.Button(button_frame, text="Calculate Statistics", command=self.calculate_statistics)
        self.calc_button.pack(side=tk.LEFT, padx=5)

        self.delete_outliers_button = tk.Button(button_frame, text="Delete Outliers", command=self.add_filtered_series_to_measurement_set)
        self.delete_outliers_button.pack(side=tk.LEFT, padx=5)

        # ======================== CROPPING SECTION ========================
        self.crop_frame = tk.Frame(self.stats_frame)
        self.crop_frame.pack(pady=5)

        # Get min and max x values from the dataset
        all_x_values = [x for series in self.measurement_set.data_series_list for x in series.data_series.keys()]
        self.min_x = min(all_x_values)
        self.max_x = max(all_x_values)

        # Display min and max X values
        self.min_x_label = tk.Label(self.crop_frame, text=f"Min X: {self.min_x:.2f}")
        self.min_x_label.pack(side=tk.LEFT, padx=5)

        self.max_x_label = tk.Label(self.crop_frame, text=f"Max X: {self.max_x:.2f}")
        self.max_x_label.pack(side=tk.LEFT, padx=5)

        # Entry fields for cropping
        self.min_x_entry = tk.Entry(self.crop_frame, width=10)
        self.min_x_entry.pack(side=tk.LEFT, padx=5)
        self.min_x_entry.insert(0, f"{self.min_x:.2f}")  # Default value

        self.max_x_entry = tk.Entry(self.crop_frame, width=10)
        self.max_x_entry.pack(side=tk.LEFT, padx=5)
        self.max_x_entry.insert(0, f"{self.max_x:.2f}")  # Default value

        # "Show Crop" button
        self.show_crop_button = tk.Button(self.crop_frame, text="Show Crop", command=self.show_crop)
        self.show_crop_button.pack(side=tk.LEFT, padx=5)

        # "Save Crop" button
        self.save_crop_button = tk.Button(self.crop_frame, text="Save Crop", command=self.save_crop)
        self.save_crop_button.pack(side=tk.LEFT, padx=5)

        self.close_button = tk.Button(self.stats_frame, text="Close", command=self.root.quit)
        self.close_button.pack(pady=5)

        self.stats_label = tk.Label(self.stats_frame, text="Statistics: ")
        self.stats_label.pack()

    def calculate_statistics(self):
        """Calculates selected statistics for checked DataSeries."""
        selected_stats = []
        selected_series = [series for series in self.measurement_set.data_series_list if self.series_vars[series.name].get()]
        
        for series in selected_series:
            times = list(series.data_series.keys())
            values = list(series.data_series.values())
            
            # Compute selected statistics
            stats_result = []
            if self.stats_options["Mean"].get():
                stats_result.append(f"Mean={series.mean_value:.3f}")
            if self.stats_options["Standard Deviation"].get():
                stats_result.append(f"Std={series.std:.3f}")
            if self.stats_options["Min"].get():
                stats_result.append(f"Min={min(values):.2f}")
            if self.stats_options["Max"].get():
                stats_result.append(f"Max={max(values):.2f}")
            
            if stats_result:
                selected_stats.append(f"{series.name}: " + ", ".join(stats_result))
        
        # Update statistics label
        self.stats_label.config(text="\n".join(selected_stats))
    
    def show_crop(self):
        """Draw vertical lines at user-defined min and max X values."""
        try:
            min_x = float(self.min_x_entry.get())
            max_x = float(self.max_x_entry.get())

            if min_x >= max_x:
                raise ValueError("Min X must be less than Max X.")

            # Clear previous vertical lines
            for ax in self.axs.flatten():
                # Remove only previous crop lines
                for line in ax.get_lines():
                    if hasattr(line, "is_crop_line") and line.is_crop_line:
                        line.remove()

                # Draw new vertical lines
                min_line = ax.axvline(x=min_x, color='r', linestyle='--', label="Crop Min")
                max_line = ax.axvline(x=max_x, color='g', linestyle='--', label="Crop Max")

                # Mark these lines for future removal
                min_line.is_crop_line = True
                max_line.is_crop_line = True

            # Refresh plot
            self.canvas_plot.draw()

        except ValueError:
            print("Invalid input! Please enter valid numbers where Min X < Max X.")

    def save_crop(self):
        """Saves the cropped data into a new MeasurementSet with a filename based on the experiment name and crop boundaries."""
        try:
            min_x = float(self.min_x_entry.get())
            max_x = float(self.max_x_entry.get())

            if min_x >= max_x:
                raise ValueError("Min X must be less than Max X.")

            # Filter the data in the measurement set based on the crop boundaries (min_x, max_x)
            self.measurement_set.crop_MeasurementSet(min_x, max_x)

            messagebox.showinfo("Success", f"Cropped data saved to: {self.measurement_set.file_path}")
        
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")


    def browse_directory(self):
        """Allow the user to browse and select a directory."""
        directory = tk.filedialog.askdirectory(initialdir=os.path.abspath(self.measurement_set.file_path))
        if directory:
            self.save_path_entry.delete(0, tk.END)
            self.save_path_entry.insert(0, directory)
        
    
    def add_filtered_series_to_measurement_set(self):
        """
        Adds a new DataSeries object with deleted outliers to the MeasurementSet
        for each selected checkbox (corresponding to a DataSeries).
        """
        new_series_vars = {}  # Dictionary to hold new series variables

        # Loop over each DataSeries and its associated checkbox
        for series in self.measurement_set.data_series_list:
            if self.series_vars.get(series.name) and self.series_vars[series.name].get():  # Check if checkbox is toggled
                # Get the filtered series (outliers deleted)
                filtered_series = series.get_filtered_series()  # This will create a filtered series

                # Check if the filtered series is already in the MeasurementSet
                if filtered_series not in self.measurement_set.data_series_list:
                    self.measurement_set.data_series_list.append(filtered_series)  # Append the filtered series to the list

                # Create a new BooleanVar for the filtered series checkbox
                filtered_var = tk.BooleanVar()
                chk = tk.Checkbutton(self.scrollable_frame, text=filtered_series.name, variable=filtered_var, anchor="w", width=15)
                chk.grid(row=len(self.measurement_set.data_series_list), column=0, padx=5, pady=2, sticky="w")

                new_series_vars[filtered_series.name] = filtered_var  # Store the filtered series in new_series_vars

                # Add a dropdown for selecting which subplot to use
                plot_options = ['None', "X - Pos", "X - Neg", "Y - Pos", "Y - Neg"]
                plot_menu = ttk.Combobox(self.scrollable_frame, values=plot_options, state="readonly")
                plot_menu.set('None')  # Default option
                plot_menu.grid(row=len(self.measurement_set.data_series_list), column=1, padx=5, pady=2)

                # Store the new dropdown in plot_vars dictionary
                self.plot_vars[filtered_series.name] = plot_menu
                plot_menu.bind("<<ComboboxSelected>>", self.update_plot)

            else:
                # If checkbox is not selected, keep the original series
                new_series_vars[series.name] = self.series_vars.get(series.name, tk.BooleanVar())

        # Update the series_vars with the new series (original + filtered)
        self.series_vars.update(new_series_vars)

        # Replot the data to reflect the newly added checkboxes
        self.plot_selected_data()


    def plot_selected_data(self):
        """Plots the selected data series on the 2x2 grid of subplots."""
        # Clear previous plots from the axes
        for ax in self.axs.flatten():
            ax.clear()

        # Reapply the plot template (axes layout, titles, etc.)
        self.figure, self.axs = create_plot_template()

        selected_series = [series for series in self.measurement_set.data_series_list if self.series_vars[series.name].get()]

        # Plot selected data based on the checkboxes
        for series in selected_series:
            times = list(series.data_series.keys())
            values = list(series.data_series.values())

            for idx, plot_var in enumerate(self.plot_vars[series.name]):
                if plot_var.get():
                    ax = self.axs[idx // 2, idx % 2]  # Get the correct subplot (2x2 grid)
                    ax.plot(times, values, label=series.name)
                    ax.legend(loc="upper right", fontsize=8)

        # Refresh the canvas with the new plot data
        self.canvas_plot.draw()

    def update_plot(self, event=None):
        # First, clear all subplots individually (but don't reset the entire figure)
        for ax in self.axs.flatten():
            ax.clear()
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Magnetic Induction (µT)")
        
        

        # Dictionary mapping dropdown selections to subplot positions "X - Pos", "X - Neg", "Y - Pos", "Y - Neg"
        plot_positions = {
            "X - Pos": (self.axs[0, 0], "X - Pos"),
            "X - Neg": (self.axs[0, 1], "X - Neg"),
            "Y - Pos": (self.axs[1, 0], "Y - Pos"),
            "Y - Neg": (self.axs[1, 1], "Y - Neg")
        }

        # Iterate through all selected series and plot them in their respective dropdown choices
        for series_name, plot_menu in self.plot_vars.items():
            selected_plot = plot_menu.get()  # Get the dropdown selection for this series

            if selected_plot in plot_positions:  # Check if it's a valid subplot option
                ax, title = plot_positions[selected_plot]  # Get the corresponding subplot and title
                series = next((s for s in self.measurement_set.data_series_list if s.name == series_name), None)

                if series:
                    times = list(series.data_series.keys())
                    values = list(series.data_series.values())

                    ax.plot(times, values, label=series.name)

        # Set titles above each subplot
        for _, (ax, title) in plot_positions.items():
            ax.set_title(title, fontsize=10)

        # Update all legends after plotting
        for ax in self.axs.flatten():
            if ax.has_data():
                ax.legend(loc="upper right", fontsize=8)

        # Refresh the canvas
        self.canvas_plot.draw()


def load_measurement_set(path, filename):
    return MeasurementSet(path, filename)

def open_gui(path, filename, experiment_name):
    root = tk.Tk()
    measurement_set = load_measurement_set(path, filename)
    gui = DataSeriesGUI(root, measurement_set, path, experiment_name)
    root.mainloop()
