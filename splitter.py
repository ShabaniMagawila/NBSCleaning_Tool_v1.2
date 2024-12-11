import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import pandas as pd
import threading


class SplitterWindow:
    def __init__(self, root, file_path, log_callback, progress_callback):
        """
        Initialize the Splitter window.

        Parameters:
        - root: The main application root.
        - file_path: Path of the file to be split.
        - log_callback: Function to log messages to the main log screen.
        - progress_callback: Function to update the main progress bar.
        """
        self.root = root
        self.file_path = file_path
        self.log_callback = log_callback
        self.progress_callback = progress_callback
        self.df = None
        self.columns = []

        # Initialize UI first
        self.initialize_ui()

        

        # Load data in the background
        threading.Thread(target=self.load_data).start()

    def initialize_ui(self):
        """
        Initialize the Splitter window UI.
        """
        self.window = tk.Toplevel(self.root)
        self.window.title("Splitter Tool")
        self.window.geometry("800x600")
        self.window.resizable(True, True)

        #logo
        logo = tk.PhotoImage(file="icons/logo.png")  # Replace with your logo file path
        self.window.iconphoto(False, logo)

        # Title
        ttk.Label(self.window, text="Splitter Tool", font=("Arial", 18, "bold")).pack(pady=10)

        # File path display
        ttk.Label(self.window, text=f"File: {self.file_path}", wraplength=780, font=("Arial", 10, "italic")).pack(pady=5)

        # Section: Split by Column
        frame_column_split = ttk.Frame(self.window, padding=(10, 10))
        frame_column_split.pack(fill=tk.X, pady=10)

        ttk.Label(frame_column_split, text="Split by Column:", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=5)
        self.column_name = tk.StringVar()
        self.column_dropdown = ttk.Combobox(frame_column_split, textvariable=self.column_name, values=self.columns, state="readonly")
        self.column_dropdown.pack(fill=tk.X, padx=10, pady=5)

        self.file_type = tk.StringVar(value="csv")
        self.save_option = tk.StringVar(value="folder")

        ttk.Label(frame_column_split, text="File Type:", font=("Arial", 12)).pack(anchor=tk.W, pady=5)
        ttk.Radiobutton(frame_column_split, text="CSV (default)", variable=self.file_type, value="csv").pack(anchor=tk.W, padx=20)
        ttk.Radiobutton(frame_column_split, text="Excel (XLSX)", variable=self.file_type, value="xlsx").pack(anchor=tk.W, padx=20)

        ttk.Label(frame_column_split, text="Save Option:", font=("Arial", 12)).pack(anchor=tk.W, pady=5)
        ttk.Radiobutton(frame_column_split, text="Save in Folder (Multiple Files)", variable=self.save_option, value="folder").pack(anchor=tk.W, padx=20)
        ttk.Radiobutton(frame_column_split, text="Save as Single File (Multiple Sheets)", variable=self.save_option, value="single").pack(anchor=tk.W, padx=20)

        ttk.Button(frame_column_split, text="Split by Column", command=self.start_split_by_column).pack(pady=10)

        # Section: Split by Rows
        frame_row_split = ttk.Frame(self.window, padding=(10, 10))
        frame_row_split.pack(fill=tk.X, pady=10)

        ttk.Label(frame_row_split, text="Split by Row Count:", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=5)
        self.row_count = tk.StringVar()
        ttk.Entry(frame_row_split, textvariable=self.row_count, width=40).pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(frame_row_split, text="Split by Rows", command=self.start_split_by_rows).pack(pady=10)

        # Close button
        ttk.Button(self.window, text="Close", command=self.window.destroy).pack(pady=20)

    def load_data(self):
        """
        Load the dataset in the background.
        """
        try:
            self.log_callback("Loading data for Splitter...")
            self.df = self._load_data()
            self.df = self.df.astype(object)  # Convert all columns to object
            self.columns = self.df.columns.tolist()

            # Update the dropdown with column names
            self.window.after(0, lambda: self.column_dropdown.config(values=self.columns))

            self.log_callback("Data loaded successfully for Splitter.")
        except Exception as e:
            self.log_callback(f"Error loading data for Splitter: {e}")
            messagebox.showerror("Error", f"Failed to load data: {e}")

    def start_split_by_column(self):
        """
        Start splitting by column in a separate thread.
        """
        threading.Thread(target=self.split_by_column).start()

    def split_by_column(self):
        """
        Split data by unique values in the selected column and handle invalid rows.
        """
        column_name = self.column_name.get()
        if not column_name:
            messagebox.showerror("Error", "Please select a column for splitting.")
            return

        # Detect invalid rows (where column_name is null or empty)
        invalid_rows = self.df[self.df[column_name].isna()]

        try:
            grouped = self.df[~self.df[column_name].isna()].groupby(column_name)

            if self.save_option.get() == "folder":
                save_folder = filedialog.askdirectory(title="Select Folder to Save Files")
                if not save_folder:
                    messagebox.showinfo("Info", "Save operation canceled.")
                    return
            else:
                default_extension = ".xlsx" if self.file_type.get() == "xlsx" else ".csv"
                file_types = [("CSV files", "*.csv"), ("Excel files", "*.xlsx")]
                save_file = filedialog.asksaveasfilename(defaultextension=default_extension, filetypes=file_types, title="Save File As")
                if not save_file:
                    messagebox.showinfo("Info", "Save operation canceled.")
                    return

            # Save invalid rows to a separate file
            if not invalid_rows.empty:
                invalid_file_path = os.path.join(save_folder if self.save_option.get() == "folder" else os.path.dirname(save_file), "Invalid_Rows.xlsx")
                invalid_rows.to_excel(invalid_file_path, index=False, engine="openpyxl")
                self.log_callback(f"Saved invalid rows to: {invalid_file_path}")
            else:
                self.log_callback("No invalid rows detected.")

            self.progress_callback(0, "green")
            total_groups = grouped.ngroups
            progress_increment = 100 / total_groups

            if self.save_option.get() == "folder":
                os.makedirs(save_folder, exist_ok=True)
                for i, (group_name, group_data) in enumerate(grouped, start=1):
                    file_name = f"{save_folder}/{group_name}"
                    file_name += ".csv" if self.file_type.get() == "csv" else ".xlsx"
                    if self.file_type.get() == "csv":
                        group_data.to_csv(file_name, index=False)
                    else:
                        group_data.to_excel(file_name, index=False, engine="openpyxl")
                    self.progress_callback(int(i * progress_increment), "green")
                    self.log_callback(f"Saved: {file_name}")
                messagebox.showinfo("Success", f"Data split by column '{column_name}' and saved in '{save_folder}'.")
            elif self.save_option.get() == "single":
                # Save all splits in a single file
                if self.file_type.get() == "csv":
                    combined_csv = pd.concat([grouped.get_group(name).assign(**{column_name: name}) for name in grouped.groups])
                    combined_csv.to_csv(save_file, index=False)
                else:
                    with pd.ExcelWriter(save_file, engine="openpyxl") as writer:
                        for i, (group_name, group_data) in enumerate(grouped, start=1):
                            sheet_name = str(group_name)[:31]  # Ensure sheet name length <= 31 characters
                            group_data.to_excel(writer, sheet_name=sheet_name, index=False)
                            self.progress_callback(int(i * progress_increment), "green")
                            self.log_callback(f"Added sheet: {sheet_name}")
                messagebox.showinfo("Success", f"Data saved as a single file: {save_file}.")
        except Exception as e:
            self.progress_callback(0, "green")
            messagebox.showerror("Error", str(e))

    def start_split_by_rows(self):
        """
        Start splitting by rows in a separate thread.
        """
        threading.Thread(target=self.split_by_rows).start()

    def split_by_rows(self):
        """
        Split data into parts with a specified number of rows per part.
        """
        try:
            rows_per_part = int(self.row_count.get().strip())
            if rows_per_part <= 0:
                messagebox.showerror("Error", "Row count must be a positive integer.")
                return

            splits = [
                self.df.iloc[i * rows_per_part: (i + 1) * rows_per_part]
                for i in range((len(self.df) + rows_per_part - 1) // rows_per_part)
            ]

            if self.save_option.get() == "folder":
                save_folder = filedialog.askdirectory(title="Select Folder to Save Files")
                if not save_folder:
                    messagebox.showinfo("Info", "Save operation canceled.")
                    return
            else:
                default_extension = ".xlsx" if self.file_type.get() == "xlsx" else ".csv"
                file_types = [("CSV files", "*.csv"), ("Excel files", "*.xlsx")]
                save_file = filedialog.asksaveasfilename(defaultextension=default_extension, filetypes=file_types, title="Save File As")
                if not save_file:
                    messagebox.showinfo("Info", "Save operation canceled.")
                    return

            self.progress_callback(0, "green")
            progress_increment = 100 / len(splits)

            if self.save_option.get() == "folder":
                os.makedirs(save_folder, exist_ok=True)
                for i, split_data in enumerate(splits, start=1):
                    file_name = f"{save_folder}/Part_{i}"
                    file_name += ".csv" if self.file_type.get() == "csv" else ".xlsx"
                    if self.file_type.get() == "csv":
                        split_data.to_csv(file_name, index=False)
                    else:
                        split_data.to_excel(file_name, index=False, engine="openpyxl")
                    self.progress_callback(int(i * progress_increment), "green")
                    self.log_callback(f"Saved: {file_name}")
                messagebox.showinfo("Success", f"Data split into parts and saved in '{save_folder}'.")
            elif self.save_option.get() == "single":
                if self.file_type.get() == "csv":
                    combined_csv = pd.concat(splits)
                    combined_csv.to_csv(save_file, index=False)
                else:
                    with pd.ExcelWriter(save_file, engine="openpyxl") as writer:
                        for i, split_data in enumerate(splits, start=1):
                            sheet_name = f"Part_{i}"
                            split_data.to_excel(writer, sheet_name=sheet_name, index=False)
                            self.progress_callback(int(i * progress_increment), "green")
                            self.log_callback(f"Added sheet: {sheet_name}")
                messagebox.showinfo("Success", f"Data saved as a single file: {save_file}.")
        except Exception as e:
            self.progress_callback(0, "green")
            messagebox.showerror("Error", str(e))

    def _load_data(self):
        """
        Load the data based on file type.

        Returns:
        - pd.DataFrame: The loaded data.

        Raises:
        - ValueError: If the file type is unsupported.
        """
        if self.file_path.endswith(".csv"):
            return pd.read_csv(self.file_path, dtype=object, low_memory=False)
        elif self.file_path.endswith(".xlsx"):
            return pd.read_excel(self.file_path, dtype=object)
        else:
            raise ValueError("Unsupported file type. Only '.csv' and '.xlsx' are supported.")
