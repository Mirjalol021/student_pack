import PyInstaller.__main__
import sys
import os

# Build the executable
PyInstaller.__main__.run([
    'calculator.py',
    '--onefile',                    # Create a single executable file
    '--windowed',                   # No console window (GUI mode)
    '--icon=NONE',                  # You can add an icon later
    '--name=Calculator',            # Name of the executable
    '--distpath=./dist',            # Output directory
    '--workpath=./build',           # Build directory
    '--specpath=./build',           # Spec file directory
])

print("\n✓ Build complete! Your .exe file is in the 'dist' folder")
