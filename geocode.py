import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd


class GeocodeWindow:
    def __init__(self, root, data, log_callback, update_data_callback):
        """
        Initialize the Geocode Tool window.

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
        

        # Create the Geocode window
        self.window = tk.Toplevel(root)
        self.window.title("Geocode Tool")
        self.window.geometry("500x450")
        self.window.resizable(False, False)

        #logo
        logo = tk.PhotoImage(file="icons/logo.png")  # Replace with your logo file path
        self.window.iconphoto(False, logo)

        # Initialize UI
        self.initialize_ui()

    def initialize_ui(self):
        """
        Set up the user interface for the Geocode Tool.
        """
        # Title
        ttk.Label(self.window, text="Geocode Tool", font=("Arial", 16, "bold")).pack(pady=10)

        # PREGION value entry
        ttk.Label(self.window, text="Enter Value for PREGION (2 digits):", font=("Arial", 12)).pack(pady=5)
        self.pregion_value = tk.StringVar(value="00")
        ttk.Entry(self.window, textvariable=self.pregion_value, width=10).pack(pady=5)

        # Instructions
        ttk.Label(self.window, text="Generate CODE1, CODE2, and leave GEOCODE empty", font=("Arial", 12)).pack(pady=5)

        # Generate and Save buttons
        ttk.Button(self.window, text="Generate Geocode", command=self.generate_geocode).pack(pady=10)
        ttk.Button(self.window, text="Save File", command=self.save_data).pack(pady=10)
        ttk.Button(self.window, text="Close", command=self.window.destroy).pack(pady=10)

    def generate_geocode(self):
        """
        Generate CODE1 and CODE2, and leave GEOCODE empty.
        """
        try:
            # Ensure required columns are present
            required_columns = [
                "PREGION", "PDISTRICT", "PCOUNCIL",
                "PCONSTITUENCY", "PDIVISION", "PWARD", "PVILLAGE", "PHAMLET"
            ]
            missing_columns = [col for col in required_columns if col not in self.data.columns]
            if missing_columns:
                raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

            # Get the user input for PREGION
            pregion_value = self.pregion_value.get().strip()
            if not pregion_value.isdigit() or len(pregion_value) != 2:
                raise ValueError("PREGION must be a 2-digit numeric value.")

            self.log_callback(f"Using PREGION value: {pregion_value}")

            # Replace PREGION with the user-provided value
            self.data["PREGION"] = pregion_value

            self.log_callback("Generating CODE1...")

            # Format PDISTRICT as two digits and concatenate with PREGION and PCOUNCIL
            self.data["PDISTRICT"] = self.data["PDISTRICT"].apply(lambda x: f"{int(x):02}" if pd.notnull(x) else "00")
            self.data["CODE1"] = (
                self.data["PREGION"] +
                self.data["PDISTRICT"] +
                self.data["PCOUNCIL"].astype(str)
            ).astype(str)

            self.log_callback("CODE1 generated successfully.")

            self.log_callback("Generating CODE2...")

            # Format components of CODE2 to ensure it is 10 characters long
            self.data["PWARD"] = self.data["PWARD"].apply(lambda x: f"{int(x):03}" if pd.notnull(x) else "000")
            self.data["PVILLAGE"] = self.data["PVILLAGE"].apply(lambda x: f"{int(x):02}" if pd.notnull(x) else "00")
            self.data["PHAMLET"] = self.data["PHAMLET"].apply(lambda x: f"{int(x):03}" if pd.notnull(x) else "000")
            self.data["CODE2"] = (
                self.data["PCONSTITUENCY"].astype(str) +
                self.data["PDIVISION"].astype(str) +
                self.data["PWARD"] +
                self.data["PVILLAGE"] +
                self.data["PHAMLET"]
            ).astype(str)

            self.log_callback("CODE2 generated successfully.")

            self.log_callback("Leaving GEOCODE empty...")

            # Initialize GEOCODE column as empty
            self.data["GEOCODE"] = ""

            self.log_callback("GEOCODE initialized as empty.")

            # Reorder columns: CODE1, CODE2, GEOCODE at the beginning
            new_order = ["CODE1", "CODE2", "GEOCODE"] + [col for col in self.data.columns if col not in ["CODE1", "CODE2", "GEOCODE"]]
            self.data = self.data[new_order]

            # Drop original columns
            self.data.drop(columns=required_columns, inplace=True)
            self.log_callback(f"Dropped original columns: {', '.join(required_columns)}")

            # Notify success and update the main data
            messagebox.showinfo("Success", "Geocode columns generated successfully (GEOCODE left empty)!")
            self.update_data_callback(self.data)

        except Exception as e:
            self.log_callback(f"Error generating geocode: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")

    def save_data(self):
        """
        Save the modified dataset to a new file.
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
            self.log_callback(f"File saved as: {save_file}")
            messagebox.showinfo("Success", f"File saved successfully as '{save_file}'.")

        except Exception as e:
            self.log_callback(f"Error saving file: {e}")
            messagebox.showerror("Error", f"An error occurred while saving: {e}")
