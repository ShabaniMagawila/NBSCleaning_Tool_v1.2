import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pandastable import Table
from splitter import SplitterWindow
from replacer import ReplacerWindow
from fix_coordinate import FixCoordinateWindow
from geocode import GeocodeWindow  # Import GeocodeWindow
import pandas as pd
import threading
import time


class SplashScreen:
    def __init__(self, root, logo_path):
        self.root = root
        self.splash = tk.Toplevel(root)
        self.splash.overrideredirect(True)  # Remove title bar
        self.splash.geometry("800x800")  # Adjust the size of the splash screen
        self.splash.configure(bg="white")  # Set background color

        # Set transparency
        self.splash.wm_attributes("-transparentcolor", "white")  # White becomes transparent

        # Center the splash screen on the screen
        screen_width = self.splash.winfo_screenwidth()
        screen_height = self.splash.winfo_screenheight()
        x = (screen_width // 2) - (800 // 2)
        y = (screen_height // 2) - (800 // 2)
        self.splash.geometry(f"+{x}+{y}")

        # Load and display the logo
        try:
            logo = tk.PhotoImage(file=logo_path)
            logo_label = tk.Label(self.splash, image=logo, bg="white")
            logo_label.image = logo  # Keep a reference to prevent garbage collection
            logo_label.pack(expand=True)
        except Exception as e:
            error_label = tk.Label(self.splash, text=f"Error loading splash image: {e}", bg="white", fg="red", font=("Arial", 12))
            error_label.pack(expand=True)

        # Schedule the splash screen to close after 10 seconds
        self.splash.after(10000, self.splash.destroy)


class ModernFastLoaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NBS Cleaning Tool")
        self.root.geometry("800x500")
        self.root.minsize(800, 500)

        # Set custom logo for the application
        logo_path = "icons/logo.png"  # Replace with your logo file path
        try:
            logo = tk.PhotoImage(file=logo_path)
            self.root.iconphoto(False, logo)
        except Exception as e:
            messagebox.showwarning("Warning", f"Failed to load logo: {e}")

        # Apply modern theme
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Yellow.Horizontal.TProgressbar", foreground="yellow", background="yellow")
        self.style.configure("Green.Horizontal.TProgressbar", foreground="green", background="green")
        self.style.configure("Blue.Horizontal.TProgressbar", foreground="blue", background="blue")

        # Title
        ttk.Label(self.root, text="File Processor", font=("Arial", 18, "bold")).pack(pady=10)

        # File path entry
        self.file_path = tk.StringVar()
        frame_top = ttk.Frame(self.root, padding=(10, 10))
        frame_top.pack(fill=tk.X)

        ttk.Entry(frame_top, textvariable=self.file_path, width=60).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(frame_top, text="Browse", command=self.browse_file).pack(side=tk.LEFT)

        # Load icons
        self.load_icon = tk.PhotoImage(file="icons/load.png")
        self.split_icon = tk.PhotoImage(file="icons/split.png")
        self.reopen_icon = tk.PhotoImage(file="icons/reopen.png")
        self.replace_icon = tk.PhotoImage(file="icons/replace.png")
        self.coordinate_icon = tk.PhotoImage(file="icons/coordinate.png")
        self.geocode_icon = tk.PhotoImage(file="icons/geocode.png")  # Icon for Geocode

        # Progress bar and label
        frame_progress = ttk.Frame(self.root, padding=(10, 10))
        frame_progress.pack(fill=tk.X)

        self.progress = ttk.Progressbar(frame_progress, orient="horizontal", length=500, mode="determinate", style="Yellow.Horizontal.TProgressbar")
        self.progress.pack(fill=tk.X, padx=5)
        self.progress_label = ttk.Label(frame_progress, text="Progress: 0%", anchor="center")
        self.progress_label.pack(pady=5)

        # Action buttons with icons
        frame_buttons = ttk.Frame(self.root, padding=(10, 10))
        frame_buttons.pack(fill=tk.X)

        self.load_button = ttk.Button(frame_buttons, text=" Load and Show Data", image=self.load_icon, compound=tk.LEFT, command=self.start_loading)
        self.load_button.pack(side=tk.LEFT, padx=5)

        self.split_button = ttk.Button(frame_buttons, text=" Split File", image=self.split_icon, compound=tk.LEFT, command=self.open_splitter_window, state="disabled")
        self.split_button.pack(side=tk.LEFT, padx=5)

        self.reopen_button = ttk.Button(frame_buttons, text=" Reopen Data Viewer", image=self.reopen_icon, compound=tk.LEFT, command=self.reopen_data_viewer, state="disabled")
        self.reopen_button.pack(side=tk.LEFT, padx=5)

        self.replace_button = ttk.Button(frame_buttons, text=" Replace Data", image=self.replace_icon, compound=tk.LEFT, command=self.open_replacer_window, state="disabled")
        self.replace_button.pack(side=tk.LEFT, padx=5)

        self.fix_coordinate_button = ttk.Button(frame_buttons, text=" Fix Coordinate", image=self.coordinate_icon, compound=tk.LEFT, command=self.open_fix_coordinate_window, state="disabled")
        self.fix_coordinate_button.pack(side=tk.LEFT, padx=5)

        self.geocode_button = ttk.Button(frame_buttons, text=" Geocode", image=self.geocode_icon, compound=tk.LEFT, command=self.open_geocode_window, state="disabled")
        self.geocode_button.pack(side=tk.LEFT, padx=5)  # Add new Geocode button

        # Logs area
        frame_logs = ttk.Frame(self.root, padding=(10, 10))
        frame_logs.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame_logs, text="Logs", font=("Arial", 12, "bold")).pack(anchor="w")
        self.log_text = tk.Text(frame_logs, bg="#1e1e1e", fg="green", wrap="word", state="disabled", height=10)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.log_text, command=self.log_text.yview)
        self.log_text.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Initialize variables for tracking loaded data
        self.loaded_data = None
        self.data_viewer_window = None

    def browse_file(self):
        filetypes = [("CSV Files", "*.csv"), ("Excel Files", "*.xlsx")]
        file_path = filedialog.askopenfilename(filetypes=filetypes)
        if file_path:
            self.file_path.set(file_path)

    def log_message(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")

    def update_progress(self, progress, color="yellow"):
        style = f"{color.capitalize()}.Horizontal.TProgressbar"
        self.progress["style"] = style
        self.progress["value"] = progress
        self.progress_label.config(text=f"Progress: {progress}%")

    def enable_action_buttons(self):
        self.split_button.config(state="normal")
        self.reopen_button.config(state="normal")
        self.replace_button.config(state="normal")
        self.fix_coordinate_button.config(state="normal")
        self.geocode_button.config(state="normal")  # Enable Geocode button

    def start_loading(self):
        file_path = self.file_path.get()
        if not file_path:
            messagebox.showerror("Error", "Please select a file first!")
            return

        self.log_message("Starting to load file...")
        self.progress["value"] = 0
        thread = threading.Thread(target=self.load_file)
        thread.start()

    def load_file(self):
        file_path = self.file_path.get()
        try:
            if file_path.endswith(".csv"):
                self.log_message("Loading CSV file...")
                self.loaded_data = pd.read_csv(file_path)
            elif file_path.endswith(".xlsx"):
                self.log_message("Loading Excel file...")
                self.loaded_data = pd.read_excel(file_path)
            else:
                raise ValueError("Unsupported file format!")

            for i in range(1, 101):
                self.update_progress(i)
                time.sleep(0.01)

            self.log_message("File loaded successfully.")
            self.enable_action_buttons()
            self.open_data_viewer()
        except Exception as e:
            self.log_message(f"Error loading file: {e}")

    def open_splitter_window(self):
        if not self.file_path.get():
            messagebox.showerror("Error", "Please select a file first!")
            return

        SplitterWindow(
            self.root,
            self.file_path.get(),
            log_callback=self.log_message,
            progress_callback=lambda progress, color="green": self.update_progress(progress, color),
        )

    def reopen_data_viewer(self):
        if self.loaded_data is not None:
            self.open_data_viewer()
        else:
            messagebox.showerror("Error", "No data loaded to display!")

    def open_data_viewer(self):
        if self.data_viewer_window is not None and tk.Toplevel.winfo_exists(self.data_viewer_window):
            self.data_viewer_window.lift()
            return

        self.data_viewer_window = tk.Toplevel(self.root)
        self.data_viewer_window.title("Data Viewer")
        self.data_viewer_window.geometry("1200x600")

        frame = ttk.Frame(self.data_viewer_window, padding=(10, 10))
        frame.pack(fill=tk.BOTH, expand=True)

        pt = Table(frame, dataframe=self.loaded_data, showtoolbar=True, showstatusbar=True)
        pt.show()

    def open_replacer_window(self):
        if self.loaded_data is None:
            messagebox.showerror("Error", "No data loaded to replace!")
            return

        ReplacerWindow(
            self.root,
            self.loaded_data,
            log_callback=self.log_message,
            update_data_callback=self.update_data,
        )

    def open_fix_coordinate_window(self):
        if self.loaded_data is None:
            messagebox.showerror("Error", "No data loaded to fix coordinates!")
            return

        FixCoordinateWindow(
            self.root,
            self.loaded_data,
            log_callback=self.log_message,
            update_data_callback=self.update_data,
        )

    def open_geocode_window(self):
        if self.loaded_data is None:
            messagebox.showerror("Error", "No data loaded to generate geocode!")
            return

        GeocodeWindow(
            self.root,
            self.loaded_data,
            log_callback=self.log_message,
            update_data_callback=self.update_data,
        )

    def update_data(self, updated_data):
        self.loaded_data = updated_data
        self.log_message("Data updated successfully.")


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide main window during splash screen

    # Splash Screen Configuration
    splash_logo_path = "icons/splash_logo.png"  # Replace with your splash image path
    SplashScreen(root, splash_logo_path)

    root.after(10000, lambda: [root.deiconify(), ModernFastLoaderApp(root)])  # Show main app after 10 seconds
    root.mainloop()
