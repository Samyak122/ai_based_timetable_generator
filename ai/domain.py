# ai/domain.py

from data.subjects import SUBJECTS
from data.teacher_loader import load_teachers


def generate_domain():
    """
    Generates all possible (subject, teacher) pairs
    that are valid based on teacher qualifications.
    """
    teachers = load_teachers()
    domain = []

    for teacher_id, teacher_data in teachers.items():
        for subject in teacher_data["subjects"]:
            if subject in SUBJECTS:
                domain.append((subject, teacher_id))

    return domain
