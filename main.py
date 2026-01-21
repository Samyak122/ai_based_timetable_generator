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



# Generate CSP components
variables = generate_variables(CLASSES)
domain = generate_domain()

# Solve timetable
solution = solve(variables, domain, CLASSES)

print("=== TIMETABLE GENERATED ===")

# Generate tables
class_tt = generate_class_timetable(solution)
teacher_tt = generate_teacher_timetable(solution)

export_pretty_excel(class_tt)
print("✅ Pretty_Timetable.xlsx generated (P1 highlighted)")

# Write outputs
write_class_csv_with_time(
    class_tt,
    start_time="10:30",
    end_time="17:00"
)

write_teacher_csv(teacher_tt)

print("✅ class_timetable.csv generated (with AM/PM)")
print("✅ teacher_timetable.csv generated")
