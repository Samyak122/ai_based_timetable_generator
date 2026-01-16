# data/add_teacher.py

import json
import os

FILE_PATH = os.path.join("data", "teachers.json")

def add_teacher():
    # Ensure file exists and is valid JSON
    if not os.path.exists(FILE_PATH):
        teachers = {}
    else:
        try:
            with open(FILE_PATH, "r", encoding="utf-8") as f:
                teachers = json.load(f)
        except json.JSONDecodeError:
            teachers = {}

    teacher_id = input("Enter Teacher ID (e.g., T1): ").strip()
    name = input("Enter Teacher Name: ").strip()

    print("Available subjects:")
    print("MARATHI, HINDI, ENGLISH, MATHS, SCIENCE, SOCIAL, PARISAR, SECURITY, WATER_SAFETY, ART, PE, WORK")

    subjects = input("Enter subjects (comma separated): ").split(",")

    teachers[teacher_id] = {
        "name": name,
        "subjects": [s.strip().upper() for s in subjects]
    }

    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(teachers, f, indent=2, ensure_ascii=False)

    print("✅ Teacher added successfully")


if __name__ == "__main__":
    add_teacher()
