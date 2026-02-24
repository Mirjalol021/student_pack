from setuptools import setup

setup(
    name='iOS Calculator',
    version='1.0',
    description='iOS-style Calculator Application',
    author='Your Name',
    py_modules=['calculator'],
    install_requires=[],  # tkinter comes with Python
    entry_points={
        'gui_scripts': [
            'calculator=calculator:main',
        ],
    },
    options={
        'py2exe': {
            'includes': ['tkinter'],
        }
    }
)
