# scene_validator/checks/frame_range.py

import hou



def fix_frame_range(start, end):
    hou.playbar.setFrameRange(start, end)
    hou.playbar.setPlaybackRange(start, end)



def run(config):
    """
    Validate Houdini global frame range.
    Returns a list of issue dictionaries.
    """
    issues = []

    frame_cfg = config.get("frame_range", {})
    start_default = frame_cfg.get("start", 1001)
    end_default = frame_cfg.get("end", 1100)

    start, end = hou.playbar.frameRange()

    if start <= 0 or end <= start:
        issues.append({
            "severity": frame_cfg.get("severity", "ERROR"),
            "node": "Global",
            "message": f"Invalid frame range: {start}-{end}. Start must be >= 1 and end > start.",
            "can_fix": frame_cfg.get("can_fix", True),
            "fix": lambda: fix_frame_range(start_default, end_default)
        })

    return issues
