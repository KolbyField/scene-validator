# scene_validator/utils/naming.py

import hou
import re

DEFAULT_NODE_TYPES = {
    "geo",
    "null",
    "file",
    "merge",
    "attribwrangle",
    "blast",
    "transform",
    "group"
}

DEFAULT_NAME_REGEX = re.compile(
    r"^({})(\d+)$".format("|".join(DEFAULT_NODE_TYPES))
)


def is_default_name(node):
    return bool(DEFAULT_NAME_REGEX.match(node.name()))


def prompt_rename(node):
    result = hou.ui.readInput(
        message=f"Rename this node?\n{node.path()}",
        initial_contents=node.name(),
        buttons=("Rename", "Skip"),
        default_choice=0,
        close_choice=1
    )

    if result[0] != 0:
        return

    new_name = result[1].strip()

    if not new_name:
        hou.ui.displayMessage(
            "Node name cannot be empty.",
            severity=hou.severityType.Error
        )
        return

    try:
        node.setName(new_name, unique_name=True)
    except hou.OperationFailed:
        hou.ui.displayMessage(
            f"Invalid node name: {new_name}",
            severity=hou.severityType.Error
        )


