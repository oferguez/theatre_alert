import json
from config import config

if __name__ == "__main__":
    print("Configuration loaded and validated successfully.")
    print("Current configuration:")
    print(json.dumps(obj=config.__dict__, indent=2))
