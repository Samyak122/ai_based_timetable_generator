from ai.variables import generate_variables
from ai.domain import generate_domain
from ai.solver import solve
from data.classes import CLASSES
from engine.output_generator import (
    generate_class_timetable,
    generate_teacher_timetable,
    write_class_csv_with_time,
    write_teacher_csv
)
from engine.excel_export import export_pretty_excel


def main():
    variables = generate_variables(CLASSES)
    domain = generate_domain()

    print("⏳ Generating timetable...")

    solution = solve(variables, domain, CLASSES)

    print("✅ Timetable generated")

    class_tt = generate_class_timetable(solution)
    teacher_tt = generate_teacher_timetable(solution)

    export_pretty_excel(class_tt)
    write_class_csv_with_time(class_tt, "10:30", "17:00")
    write_teacher_csv(teacher_tt)

    print("📁 Files generated successfully")


if __name__ == "__main__":
    main()
