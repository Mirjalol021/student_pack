# iOS Calculator - Executable Build Guide

## What Was Built

✓ **Linux Executable** created in the `dist/` folder
- File: `Calculator` (executable for Linux)
- To run on Linux: `./dist/Calculator`

## Building .EXE for Windows

Since you're on Linux, the build created a Linux executable. To create a **Windows .exe** file, follow these steps:

### Option 1: Build on Windows (Easiest)

1. Transfer these files to a **Windows computer**:
   - `calculator.py`
   - `build.py`

2. On Windows, install Python and PyInstaller:
   ```bash
   pip install pyinstaller
   ```

3. Run the build script:
   ```bash
   python build.py
   ```

4. Your `.exe` file will be in the `dist/` folder

### Option 2: Using GitHub Actions (Automated)

Create a `.github/workflows/build-windows.yml` file to build on GitHub's Windows servers automatically.

### Option 3: Use Wine (Cross-compilation on Linux)

```bash
# Install Wine and Python Windows runtime
sudo apt-get install wine wine32 wine64

# Run build script with Wine
wine python build.py
```

## Files Created

- **calculator.py** - Main Python calculator application
- **build.py** - Build script for creating executable
- **setup.py** - Setup configuration
- **dist/Calculator** - Compiled Linux executable

## Running the Application

### On Linux:
```bash
./dist/Calculator
```

### On Windows (after building .exe):
```bash
dist\Calculator.exe
```
Double-click the `.exe` file to run it!

## Features

✓ iOS-style dark design
✓ Orange operation buttons
✓ All basic math operations
✓ Decimal point support
✓ Percentage calculations
✓ Sign toggle (+/-)
✓ Clear button (AC)
✓ Fully functional calculator

## Installation Package

To create a full Windows installer (.msi), you can use:

```bash
pip install pyinstaller pynsist
```

Then use `pynsist` to create a proper Windows installer that users can double-click to install.

---

**Question?** Check the build output above - it was successful! 🎉
