# scene_validator/run.py

import importlib
from scene_validator.ui import main_window

importlib.reload(main_window)


def run():
    """
    Entry point for shelf tool.
    Launches the Scene Validator UI.
    """
    main_window.show()