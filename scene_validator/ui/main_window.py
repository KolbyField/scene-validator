# scene_validator/ui/main_window.py

import hou
from PySide2 import QtWidgets, QtCore

from scene_validator import validator_core


class SceneValidatorWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(SceneValidatorWindow, self).__init__(parent)

        self.setWindowTitle("Scene Validator")
        self.setMinimumWidth(700)
        self.setMinimumHeight(450)

        self.current_filter = "ALL"
        self._current_issues = []
        self.current_issue = None

        self._build_ui()

    # ---------------- UI ---------------- #

    def _build_ui(self):
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)

        layout = QtWidgets.QVBoxLayout(central)

        # Run button
        self.run_btn = QtWidgets.QPushButton("Run Validation")
        self.run_btn.clicked.connect(self.run_validation)
        layout.addWidget(self.run_btn)

        # Filter buttons
        filter_layout = QtWidgets.QHBoxLayout()

        self.filter_all_btn = QtWidgets.QPushButton("All")
        self.filter_error_btn = QtWidgets.QPushButton("Errors")
        self.filter_warning_btn = QtWidgets.QPushButton("Warnings")

        self.filter_all_btn.clicked.connect(lambda: self.apply_filter("ALL"))
        self.filter_error_btn.clicked.connect(lambda: self.apply_filter("ERROR"))
        self.filter_warning_btn.clicked.connect(lambda: self.apply_filter("WARNING"))

        filter_layout.addWidget(self.filter_all_btn)
        filter_layout.addWidget(self.filter_error_btn)
        filter_layout.addWidget(self.filter_warning_btn)

        layout.addLayout(filter_layout)

        # Fix buttons
        button_row = QtWidgets.QHBoxLayout()

        self.fix_button = QtWidgets.QPushButton("Fix Selected")
        self.fix_button.setEnabled(False)
        self.fix_button.clicked.connect(self.fix_selected_issue)
        button_row.addWidget(self.fix_button)

        self.fix_all_button = QtWidgets.QPushButton("Fix All")
        self.fix_all_button.setEnabled(False)
        self.fix_all_button.clicked.connect(self.fix_all_issues)
        button_row.addWidget(self.fix_all_button)

        button_row.addStretch()
        layout.addLayout(button_row)

        # Issue list
        self.issue_list = QtWidgets.QListWidget()
        self.issue_list.itemClicked.connect(self.on_issue_clicked)
        self.issue_list.itemDoubleClicked.connect(self.on_issue_double_clicked)
        layout.addWidget(self.issue_list)

    # ---------------- Interaction ---------------- #

    def on_issue_clicked(self, item):
        issue = item.data(QtCore.Qt.UserRole)
        self.current_issue = issue

        self.fix_button.setEnabled(issue.get("can_fix", False))

        node_path = issue.get("node")
        if not node_path:
            return

        node = hou.node(node_path)
        if not node:
            return

        hou.clearAllSelected()
        node.setSelected(True, clear_all_selected=True)
        node.setCurrent(True, clear_all_selected=True)

    def on_issue_double_clicked(self, item):
        issue = item.data(QtCore.Qt.UserRole)

        if not issue or not issue.get("can_fix"):
            return

        fix_fn = issue.get("fix")
        if not callable(fix_fn):
            return

        with hou.undos.group("Scene Validator - Double Click Fix"):
            fix_fn()

        self.run_validation()

    # ---------------- Fixing ---------------- #

    def fix_selected_issue(self):
        issue = self.current_issue
        if not issue:
            return

        fix_fn = issue.get("fix")
        if not callable(fix_fn):
            return

        with hou.undos.group("Scene Validator - Fix Selected"):
            fix_fn()

        self.run_validation()

    def fix_all_issues(self):
        if not self._current_issues:
            return

        with hou.undos.group("Scene Validator - Fix All"):
            for issue in self._current_issues:
                if not issue.get("can_fix"):
                    continue

                fix_fn = issue.get("fix")
                if not callable(fix_fn):
                    continue

                try:
                    did_fix = fix_fn()
                except Exception as e:
                    print(f"Fix failed for {issue.get('node')}: {e}")

        self.run_validation()

    def _update_fix_all_state(self):
        can_fix_any = any(
            issue.get("can_fix") and callable(issue.get("fix"))
            for issue in self._current_issues
        )
        self.fix_all_button.setEnabled(can_fix_any)

    # ---------------- Filtering ---------------- #

    def apply_filter(self, severity):
        self.current_filter = severity
        self.issue_list.clear()

        if not self._current_issues:
            self.issue_list.addItem(QtWidgets.QListWidgetItem("No issues found"))
            return

        for issue in self._current_issues:
            issue_sev = issue.get("severity", "INFO")

            if severity != "ALL" and issue_sev != severity:
                continue

            node = issue.get("node", "Global")
            message = issue.get("message", "")
            text = f"[{issue_sev}] {node} — {message}"

            item = QtWidgets.QListWidgetItem(text)
            item.setData(QtCore.Qt.UserRole, issue)

            if issue_sev == "ERROR":
                item.setForeground(QtCore.Qt.red)
            elif issue_sev == "WARNING":
                item.setForeground(QtCore.Qt.yellow)

            self.issue_list.addItem(item)

    # ---------------- Validation ---------------- #

    def run_validation(self):
        issues = validator_core.run_all_checks()
        SEVERITY_ORDER = {"ERROR": 0, "WARNING": 1, "INFO": 2}

        issues.sort(key=lambda i: SEVERITY_ORDER.get(i.get("severity", "INFO"), 99))
        
        self._current_issues = issues

        # Logging
        from scene_validator.utils import logger
        logger.write_log(issues)

        # UI state
        self._update_fix_all_state()
        self.fix_button.setEnabled(False)
        self.current_issue = None

        self.apply_filter(self.current_filter)


def show():
    global _scene_validator_window
    try:
        _scene_validator_window.close()
    except Exception:
        pass

    _scene_validator_window = SceneValidatorWindow(
        parent=hou.ui.mainQtWindow()
    )
    _scene_validator_window.show()
