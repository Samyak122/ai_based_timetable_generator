# data/teacher_loader.py

import json
import os


def load_teachers():
    """
    Loads teachers from teachers.json
    """
    file_path = os.path.join("data", "teachers.json")

    if not os.path.exists(file_path):
        raise FileNotFoundError("teachers.json not found in data folder")

    with open(file_path, "r", encoding="utf-8") as f:
        teachers = json.load(f)

    if not teachers:
        raise ValueError("No teachers found. Please add teachers first.")

    return teachers
