import base64
from pathlib import Path
import os

def write_resume(secret_name, output_path):
    data = os.getenv(secret_name)
    if data:
        Path(output_path).write_bytes(base64.b64decode(data))
