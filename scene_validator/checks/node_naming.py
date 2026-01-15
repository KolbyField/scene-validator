# scene_validator/checks/node_naming.py

import hou
from scene_validator.utils.naming import is_default_name, prompt_rename

def is_inside_locked_hda(node):
    parent = node.parent()
    while parent:
        if parent.isLockedHDA():
            return True
        parent = parent.parent()
    return False

def run(config):
    issues = []

    naming_cfg = config.get("naming", {})
    if not naming_cfg.get("enabled", True):
        return issues

    severity = naming_cfg.get("severity", "WARNING")

    #check all nodes that are in the obj network
    #if they have a default name add a warning to issues
    for node in hou.node("/obj").allSubChildren():
        if is_default_name(node):
            inside_locked = is_inside_locked_hda(node)

            if inside_locked:
                issues.append({
                    "severity": "INFO",
                    "node": node.path(),
                    "message": (
                        f"Locked HDA contains default-named node: {node.name()} "
                        "(cannot be auto-fixed)"
                    ),
                    "can_fix": False,
                    "fix": None
                })
            else:
                issues.append({
                    "severity": "WARNING",
                    "node": node.path(),
                    "message": f"Node uses default name: {node.name()}",
                    "can_fix": True,
                    "fix": lambda n=node: prompt_rename(n)
                })


    return issues