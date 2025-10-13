import sys
import os

def get_path_for_resource(relative_path):
    """
    Get the absolute path to a resource, whether in development or packaged by PyInstaller.
    
    In development: Resources are located relative to the 'src/' directory
    In packaged mode: Resources are in PyInstaller's temporary _MEIPASS directory
    """
    try:
        # PyInstaller creates a temporary folder and stores the path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # Not running as a PyInstaller executable
        # Get the 'src/' directory (parent of 'core/' where this file lives)
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    return os.path.join(base_path, relative_path)