# scene_validator/utils/logger.py

import os
import hou
from datetime import datetime


def get_log_path():
    hip_path = hou.hipFile.path()

    if hip_path == "untitled.hip":
        return None

    #gets directory and creates a scene validation log file
    directory = os.path.dirname(hip_path)
    return os.path.join(directory, "scene_validation.log")


def write_log(issues):
    log_path = get_log_path()
    if not log_path:
        return

    with open(log_path, "w") as f:
        f.write("Scene Validation Log\n")
        f.write(f"Timestamp: {datetime.now()}\n\n")

        for issue in issues:
            f.write(
                f"[{issue['severity']}] "
                f"{issue['node']} - "
                f"{issue['message']}\n"
            )
