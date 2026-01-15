# scene_validator/checks/locked_nodes.py

import hou

def run(config):
    issues = []

    lock_cfg = config.get("locked_nodes", {})
    severity = lock_cfg.get("severity", "WARNING")

    for node in hou.node("/").allSubChildren():
    # Only meaningful lock type we can reliably detect
        if node.isLockedHDA():
            issues.append({
                "severity": severity,
                "node": node.path(),
                "message": "HDA is locked",
                "can_fix": False
            })

    return issues
