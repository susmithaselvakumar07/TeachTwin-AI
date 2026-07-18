from dotenv import dotenv_values
from pathlib import Path

env_path = Path(".env")

config = dotenv_values(env_path)

print(config)