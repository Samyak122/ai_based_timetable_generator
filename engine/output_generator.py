# engine/output_generator.py

import csv
from data.labels import LABELS
from data.teacher_loader import load_teachers
from engine.time_config import generate_weekly_timing


def generate_class_timetable(solution):
    """
    class_id -> day -> period -> (subject, teacher)
    """
    class_table = {}

    for (cls, day, period), (subject, teacher) in solution.items():
        class_table.setdefault(cls, {})
        class_table[cls].setdefault(day, {})
        class_table[cls][day][period] = (subject, teacher)

    return class_table


def generate_teacher_timetable(solution):
    """
    teacher_id -> day -> period -> (class, subject)
    """
    teacher_table = {}

    for (cls, day, period), (subject, teacher) in solution.items():
        teacher_table.setdefault(teacher, {})
        teacher_table[teacher].setdefault(day, {})
        teacher_table[teacher][day][period] = (cls, subject)

    return teacher_table


def write_class_csv_with_time(
    class_table,
    start_time,
    end_time,
    filename="class_timetable.csv"
):
    """
    Writes class-wise timetable with AM/PM time slots.
    Handles Mon–Fri–Sat automatically.
    """
    teachers = load_teachers()
    timing = generate_weekly_timing(start_time, end_time)

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Class",
            "Day",
            "Period",
            "Time (AM/PM)",
            "Subject (EN)",
            "Subject (MR)",
            "Teacher"
        ])

        for cls, days in class_table.items():
            for day, periods in days.items():
                for period, (subject, teacher) in periods.items():

                    time_slot = ""
                    for t in timing.get(day, []):
                        if t["period"] == period:
                            time_slot = t["time"]
                            break

                    writer.writerow([
                        cls,
                        day,
                        period,
                        time_slot,
                        LABELS[subject]["en"],
                        LABELS[subject]["mr"],
                        teachers[teacher]["name"]
                    ])


def write_teacher_csv(
    teacher_table,
    filename="teacher_timetable.csv"
):
    """
    Writes teacher-wise timetable CSV.
    """
    teachers = load_teachers()

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Teacher",
            "Day",
            "Period",
            "Class",
            "Subject (EN)",
            "Subject (MR)"
        ])

        for teacher, days in teacher_table.items():
            for day, periods in days.items():
                for period, (cls, subject) in periods.items():
                    writer.writerow([
                        teachers[teacher]["name"],
                        day,
                        period,
                        cls,
                        LABELS[subject]["en"],
                        LABELS[subject]["mr"]
                    ])
