from cx_Freeze import setup, Executable
import sys
import os

# Include additional files
include_files = [
    ("icons", "icons"),       # Include the icons directory
    "license.txt"             # Include the license file
]

# Specify dependencies for your program
build_exe_options = {
    "packages": ["tkinter", "pandas", "os"],  # Add other modules used in your project
    "include_files": include_files            # Include files in the executable
}

# Determine the base
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Use this for GUI apps to avoid the console window

# Setup configuration
setup(
    name="NBSCleaning_Tool",
    version="1.0",
    description="A cleaning tool for NBS data",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            script="main.py",         # Your main Python file
            base=base,                # Base configuration
            icon="icons/logo.ico"     # Path to your .ico file for the installer
        )
    ],
)
