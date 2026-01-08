import json, os

SETTINGS_PATH = "settings.json"

DEFAULT_SETTINGS = {
    "theme": "dark",
    "window": {"width": 1000, "height": 700},
    "resume_view": "raw",
    "pdf_mode": "page"
}

def load_settings():
    data = {}

    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, "r") as f:
                data = json.load(f)
        except Exception:
            data = {}

    # Merge defaults (fills missing keys)
    for k, v in DEFAULT_SETTINGS.items():
        if k not in data:
            data[k] = v
        elif isinstance(v, dict):
            for dk, dv in v.items():
                if dk not in data[k]:
                    data[k][dk] = dv

    return data

def save_settings(settings):
    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=4)
