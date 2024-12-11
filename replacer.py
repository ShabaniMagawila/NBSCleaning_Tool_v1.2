import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd


class ReplacerWindow:
    def __init__(self, root, data, log_callback, update_data_callback):
        """
        Initialize the Replacer Tool window.

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

        # Create the Replacer window
        self.window = tk.Toplevel(root)
        self.window.title("Replacer Tool")
        self.window.geometry("500x400")
        self.window.resizable(False, False)

        # Initialize UI
        self.initialize_ui()

    def initialize_ui(self):
        """
        Set up the user interface for the Replacer Tool.
        """
        # Title
        ttk.Label(self.window, text="Replacer Tool", font=("Arial", 16, "bold")).pack(pady=10)

        # Instructions
        ttk.Label(self.window, text="Replace null-like values with:", font=("Arial", 12)).pack(pady=5)

        #logo
        logo = tk.PhotoImage(file="icons/logo.png")  # Replace with your logo file path
        self.window.iconphoto(False, logo)

        # Replacement value entry
        self.replace_value = tk.StringVar(value="NA")
        ttk.Entry(self.window, textvariable=self.replace_value, width=30).pack(pady=5)

        # File type selection
        ttk.Label(self.window, text="Save File As:", font=("Arial", 12)).pack(pady=5)
        self.file_type = tk.StringVar(value="csv")
        ttk.Radiobutton(self.window, text="CSV (default)", variable=self.file_type, value="csv").pack(anchor=tk.W, padx=40)
        ttk.Radiobutton(self.window, text="Excel (XLSX)", variable=self.file_type, value="xlsx").pack(anchor=tk.W, padx=40)

        # Replace and Save button
        ttk.Button(self.window, text="Replace Values and Save", command=self.replace_and_save).pack(pady=10)

        # Close button
        ttk.Button(self.window, text="Close", command=self.window.destroy).pack(pady=10)

    def replace_and_save(self):
        """
        Replace null-like values and save the modified file.
        """
        replacement = self.replace_value.get()
        if not replacement:
            messagebox.showerror("Error", "Replacement value cannot be empty!")
            return

        try:
            # Replace null-like values
            null_like_values = [None, "", "nan", "NaN", "#NULL!", pd.NA]
            self.data.replace(null_like_values, replacement, inplace=True)

            # Log the action
            self.log_callback(f"Replaced null-like values with '{replacement}'.")

            # Save the modified file
            if self.file_type.get() == "csv":
                save_file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], title="Save File As")
                if not save_file:
                    messagebox.showinfo("Info", "Save operation canceled.")
                    return
                self.data.to_csv(save_file, index=False)
            elif self.file_type.get() == "xlsx":
                save_file = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")], title="Save File As")
                if not save_file:
                    messagebox.showinfo("Info", "Save operation canceled.")
                    return
                self.data.to_excel(save_file, index=False)

            # Log the save action
            self.log_callback(f"File saved as: {save_file}")

            # Update the data in the main application
            self.update_data_callback(self.data)

            messagebox.showinfo("Success", f"File saved successfully as '{save_file}'.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
