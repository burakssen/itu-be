from pathlib import Path
import random
import string

def randomnamegen(size=6):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))

def get_project_root() -> Path:
    return Path(__file__).parent.parent