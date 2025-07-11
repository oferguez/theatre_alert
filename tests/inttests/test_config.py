import json
from config import Config

if __name__ == "__main__":
    config = Config().load_and_validate()
    print("Configuration loaded and validated successfully.")
    print("Current configuration:")
    print(json.dumps(obj=config.__dict__, indent=2))
