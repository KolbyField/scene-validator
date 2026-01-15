# scene_validator/checks/unused_nodes.py

import hou


def run(config):
    issues = []

    unused_cfg = config.get("unused_nodes", {})
    severity = unused_cfg.get("severity", "WARNING")

    IGNORE_TYPES = (
        "output",
        "ropnet",
        "usd_rop",
        "fetch",
    )
    ROOT_CONTEXTS = (
    "/obj",
    "/out",
    "/ch",
    "/img",
    "/vex",
    "/mat",
    "/stage",
    "/tasks",
    )   

    for node in hou.node("/").allSubChildren():

        # ONLY SOP nodes
        if node.type().category() != hou.sopNodeTypeCategory():
            continue

        # Skip bypassed SOPs
        bypass_parm = node.parm("bypass")
        if bypass_parm and bypass_parm.eval():
            continue

        # Skip nodes with outputs
        if node.outputs():
            continue

        # Skip displayed SOP
        if node.isDisplayFlagSet():
            continue

        issues.append({
            "severity": severity,
            "node": node.path(),
            "message": "Node appears to be unused (no outputs)",
            "can_fix": False
        })

    return issues
