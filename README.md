# NBSCleaning_Tool

NBSCleaning_Tool is a powerful data processing application designed for cleaning, splitting, replacing, fixing coordinates, and geocoding large datasets. Built with Python, this tool provides an intuitive GUI powered by `tkinter` and comes with multiple utilities for handling complex data operations efficiently.

## Features

1. **Data Viewer:**
   - Load and display large `.csv` or `.xlsx` files in a modern GUI table.

2. **Replacer Tool:**
   - Replace all null-like values (e.g., `NaN`, `None`, empty strings) in any column with a specified value.
   - Supports all data types (integer, float, object).
   - Save the modified file in `.csv` or `.xlsx` format.

3. **Splitter Tool:**
   - Split data by unique column values or by a specified number of rows.
   - Save the output as multiple files in a folder or as multiple sheets in a single file.

4. **Fix Coordinates Tool:**
   - Convert latitude and longitude columns to proper float format.
   - Automatically calculate and generate missing coordinates based on the mean value.

5. **Geocode Tool:**
   - Format and create unique codes (`CODE1`, `CODE2`, `GEOCODE`) based on specific columns.
   - Customizable and ensures all codes are formatted as text.

6. **Modern GUI:**
   - Splash screen on startup with a custom logo.
   - Progress bars for real-time feedback.
   - Log screen for tracking all processes.
   - Intuitive buttons for easy navigation.

## Prerequisites

Ensure you have the following installed on your system:

- Python 3.10+
- Required Python libraries:
  ```bash
  pip install pandas openpyxl tkinter cx-Freeze
  ```

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd NBSCleaning_Tool
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

## Build Executable

To generate an executable for distribution:

1. Use `cx_Freeze` to build the application:
   ```bash
   python setup.py build
   ```

2. Create an installer using Inno Setup:
   - Compile the provided `.iss` script using the [Inno Setup Compiler](https://jrsoftware.org/isinfo.php).

## How to Use

### **Main Window**
1. **Load and Show Data:**
   - Browse and load `.csv` or `.xlsx` files.
   - View the data in an interactive table.

2. **Splitter Tool:**
   - Split files by a selected column or a specific row count.
   - Save the results as multiple files or sheets.

3. **Replacer Tool:**
   - Replace all null-like values in your dataset with a specified value.

4. **Fix Coordinates Tool:**
   - Clean latitude and longitude data and calculate missing values.

5. **Geocode Tool:**
   - Generate unique geocodes and format specific columns.

### **Saving Results**
- Save modified files in `.csv` or `.xlsx` format.

## Directory Structure

```
NBSCleaning_Tool/
├── build/                   # Build directory for cx_Freeze
├── icons/                   # Icons and images used in the application
├── main.py                  # Entry point of the application
├── splitter.py              # Splitter Tool implementation
├── replacer.py              # Replacer Tool implementation
├── fix_coordinate.py        # Fix Coordinates Tool implementation
├── geocode.py               # Geocode Tool implementation
├── license.txt              # License file for the installer
├── README.md                # Documentation file
├── setup.py                 # cx_Freeze setup file
└── requirements.txt         # Python dependencies
```

## Troubleshooting

1. **Error: `File not found` during installer execution:**
   - Ensure all required files (e.g., icons, executables) are included in the build directory and specified in the `.iss` script.

2. **GUI Freezes During Large File Operations:**
   - The application uses multithreading for large file operations. Ensure your system meets the required specifications.

3. **Missing Python Libraries:**
   - Install the required dependencies with:
     ```bash
     pip install -r requirements.txt
     ```

## Contributing

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m 'Add some feature'
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

## License

This project is licensed under the MIT License. See the `license.txt` file for details.

## Contact

For support or inquiries, please contact:

- **Email:** shabanimagawila@gmail.com
- **Website:** [NBS](https://nbscleaningtool.com)
