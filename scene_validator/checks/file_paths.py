# scene_validator/checks/file_paths.py

import os
import hou




def run(config):
    issues = []

    file_cfg = config.get("file_paths", {})
    severity = file_cfg.get("severity", "ERROR")

    IGNORE_CONTEXTS = ("/tasks", "/stage")

    IGNORE_SUBSTRINGS = (
        "houdini_temp",
        "pdgtemp",
        "rendergallery",
        "taskgraph",
        ".sim",
        "checkpoint",
    )

    #go through all nodes in scene
    for node in hou.node("/").allSubChildren():
        if node.path().startswith(IGNORE_CONTEXTS):
            continue

        #loop through each nodes parameters
        for parm in node.parms():
            #check if the node type is a string 
            if parm.parmTemplate().type() != hou.parmTemplateType.String:
                continue

            try:
                value = parm.eval()
            except:
                continue

            if not value:
                continue

            # Skip relative references (node paths, ../, etc)
            if value.startswith("../") or value.startswith("./"):
                continue
            
            #if there are not slashes in string, skip it 
            if not ("/" in value or "\\" in value):
                continue

            #use expandString to expand node location
            #ex from sidefx
            #hou.text.expandString("$HIP/file.geo")
            #--> '/dir/containing/hip/file/file.geo
            expanded = hou.expandString(value)

            if any(token in expanded.lower() for token in IGNORE_SUBSTRINGS):
                continue

            #core check if the directory exists
            if not os.path.exists(expanded):
                issues.append({
                    "severity": severity,
                    "node": node.path(),
                    "parm": parm.name(),
                    "message": f"Missing file path:\n{expanded}",
                    "can_fix": False
                })

    return issues
