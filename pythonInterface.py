
import tkinter as tk
from tkinter import ttk, filedialog
from DataInspectionGUI import open_gui  # Import your existing GUI function

class MainGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Main GUI")
        self.root.geometry("400x400")

        # Create a Notebook (Tabbed Interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create Frames for Each Tab
        self.main_tab = ttk.Frame(self.notebook)
        self.settings_tab = ttk.Frame(self.notebook)

        # Add Tabs to Notebook
        self.notebook.add(self.main_tab, text="Data Inspection")
        self.notebook.add(self.settings_tab, text="Experiment Data Treatment")

        # Populate Main Tab
        self.create_main_tab()

        # Populate Settings Tab (Placeholder)
        self.create_settings_tab()

    def create_main_tab(self):
        """Creates the content for the 'Data Inspection' tab."""
        tk.Label(self.main_tab, text="Path:").pack(pady=5)
        self.path_entry = tk.Entry(self.main_tab, width=40)
        self.path_entry.pack(pady=5)
        tk.Button(self.main_tab, text="Browse", command=self.browse_path).pack(pady=5)

        tk.Label(self.main_tab, text="File Name:").pack(pady=5)
        self.filename_entry = tk.Entry(self.main_tab, width=40)
        self.filename_entry.pack(pady=5)

        tk.Label(self.main_tab, text="Experiment Name:").pack(pady=5)
        self.experiment_entry = tk.Entry(self.main_tab, width=40)
        self.experiment_entry.pack(pady=5)

        tk.Button(self.main_tab, text="Open Data Series GUI", command=self.open_data_series_gui).pack(pady=10)

    def create_settings_tab(self):
        """Creates the content for the 'Experiment Data Treatment' tab (currently a placeholder)."""
        tk.Label(self.settings_tab, text="Settings will go here...", font=("Arial", 12)).pack(pady=20)

    def browse_path(self):
        path = filedialog.askdirectory()
        if path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, path)

    def open_data_series_gui(self):
        path = self.path_entry.get()
        filename = self.filename_entry.get()
        experiment_name = self.experiment_entry.get()

        if path and filename and experiment_name:
            open_gui(path, filename, experiment_name)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainGUI(root)
    root.mainloop()