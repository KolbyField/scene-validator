# scene_validator/checks/fps.py

import hou

def fix_fps(target_fps):
    hou.setFps(target_fps)

def run(config):
    issues = []

    fps_cfg = config.get("fps", {})
    allowed = fps_cfg.get("allowed", [24])
    severity = fps_cfg.get("severity", "ERROR")
    can_fix = fps_cfg.get("can_fix", True)
    default_fps = fps_cfg.get("default", allowed[0])

    current_fps = hou.fps()

    if current_fps not in allowed:
        issues.append({
            "severity": severity,
            "node": "Global",
            "message": (
            f"Scene FPS is {current_fps}. "
            f"Standard values are {allowed}. "
            "Please confirm this is intentional."
            ),
            "can_fix": can_fix,
            "fix": lambda: fix_fps(default_fps)
        })

    return issues
