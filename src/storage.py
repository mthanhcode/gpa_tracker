import json
from pathlib import Path

DATA_FILE = Path("data/courses.json")

def load_courses():
    if not DATA_FILE.exists():
        return []
    try:
        with open(DATA_FILE, encoding = "utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(" File dữ liệu bị lỗi, bắt đầu lại từ đầu!")
        return[]


def save_courses(courses):
    DATA_FILE.parent.mkdir(parents = True, exist_ok = True)
    with open(DATA_FILE, "w", encoding = "utf-8") as f:
        json.dump(courses, f, ensure_ascii = False, indent = 2)