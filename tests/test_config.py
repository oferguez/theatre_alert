import os
import sys

project_root = os.path.dirname(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
netlify_functions_path = os.path.join(project_root, "netlify/functions")
if netlify_functions_path not in sys.path:
    sys.path.insert(0, netlify_functions_path)

import json
from config import config

if __name__ == "__main__":
    print("Configuration loaded and validated successfully.")
    print("Current configuration:")
    print(json.dumps(obj=config.__dict__, indent=2))
