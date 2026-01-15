import hou

def select_node(node_path):
    node = hou.node(node_path)
    if not node:
        return

    hou.clearAllSelected()
    node.setSelected(True, clear_all_selected=True)

    pane = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    if pane:
        pane.frameSelection()

    # Force Houdini UI refresh
    hou.ui.triggerUpdate()
