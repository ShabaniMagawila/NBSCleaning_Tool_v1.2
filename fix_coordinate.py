import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd


class FixCoordinateWindow:
    def __init__(self, root, data, log_callback, update_data_callback):
        """
        Initialize the Fix Coordinate Tool window.

        Parameters:
        - root: The main application root.
        - data: The DataFrame loaded in the main application.
        - log_callback: Function to log messages to the main log screen.
        - update_data_callback: Function to update the DataFrame in the main application.
        """
        self.root = root
        self.data = data
        self.log_callback = log_callback
        self.update_data_callback = update_data_callback

        # Create the Fix Coordinate window
        self.window = tk.Toplevel(root)
        self.window.title("Fix Coordinate Tool")
        self.window.geometry("500x400")
        self.window.resizable(False, False)

        #logo
        logo = tk.PhotoImage(file="icons/logo.png")  # Replace with your logo file path
        self.window.iconphoto(False, logo)

        # Initialize UI
        self.initialize_ui()

    def initialize_ui(self):
        """
        Set up the user interface for the Fix Coordinate Tool.
        """
        # Title
        ttk.Label(self.window, text="Fix Coordinate Tool", font=("Arial", 16, "bold")).pack(pady=10)

        # Latitude column selection
        ttk.Label(self.window, text="Select Latitude Column:", font=("Arial", 12)).pack(pady=5)
        self.latitude_column = tk.StringVar()
        self.latitude_dropdown = ttk.Combobox(self.window, textvariable=self.latitude_column, values=self.data.columns.tolist(), state="readonly")
        self.latitude_dropdown.pack(pady=5, padx=20, fill=tk.X)

        # Longitude column selection
        ttk.Label(self.window, text="Select Longitude Column:", font=("Arial", 12)).pack(pady=5)
        self.longitude_column = tk.StringVar()
        self.longitude_dropdown = ttk.Combobox(self.window, textvariable=self.longitude_column, values=self.data.columns.tolist(), state="readonly")
        self.longitude_dropdown.pack(pady=5, padx=20, fill=tk.X)

        # Buttons
        ttk.Button(self.window, text="Fix Coordinates", command=self.fix_coordinates).pack(pady=10)
        ttk.Button(self.window, text="Save Fixed Data", command=self.save_fixed_data).pack(pady=10)
        ttk.Button(self.window, text="Close", command=self.window.destroy).pack(pady=10)

    def fix_coordinates(self):
        """
        Fix the latitude and longitude columns.
        """
        lat_col = self.latitude_column.get()
        lon_col = self.longitude_column.get()

        if not lat_col or not lon_col:
            messagebox.showerror("Error", "Please select both latitude and longitude columns!")
            return

        try:
            # Log the action
            self.log_callback(f"Fixing coordinates for columns '{lat_col}' and '{lon_col}'...")

            # Convert columns to float and handle invalid values
            self.data[lat_col] = pd.to_numeric(self.data[lat_col], errors="coerce")
            self.data[lon_col] = pd.to_numeric(self.data[lon_col], errors="coerce")

            # Fill missing values with the mean
            lat_mean = self.data[lat_col].mean()
            lon_mean = self.data[lon_col].mean()
            self.data[lat_col].fillna(lat_mean, inplace=True)
            self.data[lon_col].fillna(lon_mean, inplace=True)

            # Log the results
            self.log_callback(f"Coordinates fixed: Missing values replaced with column means (Lat: {lat_mean:.6f}, Lon: {lon_mean:.6f}).")
            messagebox.showinfo("Success", "Coordinates fixed successfully!")
            self.update_data_callback(self.data)  # Update the data in the main application

        except Exception as e:
            self.log_callback(f"Error fixing coordinates: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")

    def save_fixed_data(self):
        """
        Save the fixed dataset to a new file.
        """
        try:
            save_file = filedialog.asksaveasfilename(defaultextension=".csv",
                                                     filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xlsx")],
                                                     title="Save File As")
            if not save_file:
                messagebox.showinfo("Info", "Save operation canceled.")
                return

            if save_file.endswith(".csv"):
                self.data.to_csv(save_file, index=False)
            elif save_file.endswith(".xlsx"):
                self.data.to_excel(save_file, index=False, engine="openpyxl")
            else:
                raise ValueError("Unsupported file format!")

            # Log the save action
            self.log_callback(f"Fixed data saved as: {save_file}")
            messagebox.showinfo("Success", f"File saved successfully as '{save_file}'.")

        except Exception as e:
            self.log_callback(f"Error saving file: {e}")
            messagebox.showerror("Error", f"An error occurred while saving: {e}")
