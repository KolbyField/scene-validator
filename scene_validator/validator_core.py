# scene_validator/validator_core.py
import importlib

from scene_validator.checks import frame_range, node_naming, file_paths, unused_nodes, fps, locked_nodes
from scene_validator.config.config_loader import load_config

importlib.reload(frame_range)
importlib.reload(node_naming)
importlib.reload(file_paths)
importlib.reload(unused_nodes)
importlib.reload(fps)
importlib.reload(locked_nodes)

def run_all_checks():
    """
    Runs all registered validation checks.
    Returns a list of all issues.
    """
    config = load_config()
    issues = []

    #adds output from framerate check to issues list
    issues.extend(fps.run(config))
    issues.extend(frame_range.run(config))
    issues.extend(node_naming.run(config))
    issues.extend(file_paths.run(config))
    issues.extend(unused_nodes.run(config))
    issues.extend(locked_nodes.run(config))

    return issues
