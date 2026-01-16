from data.teacher_loader import load_teachers

teachers = load_teachers()

print("=== TEACHERS LOADED ===")
for tid, t in teachers.items():
    print(tid, "=>", t["name"], "| Subjects:", t["subjects"])
