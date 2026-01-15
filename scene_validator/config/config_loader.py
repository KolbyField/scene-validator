# scene_validator/config/config_loader.py

import json
import os


def load_config():
    config_path = os.path.join(
        os.path.dirname(__file__),
        "default_config.json"
    )

    if not os.path.exists(config_path):
        return {}

    with open(config_path, "r") as f:
        return json.load(f)
