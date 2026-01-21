from flask import Flask, render_template, request, redirect, url_for, send_file
from data.teacher_loader import load_teachers
from data.classes import CLASSES
from ai.variables import generate_variables
from ai.domain import generate_domain
from ai.solver import solve
from engine.output_generator import (
    generate_class_timetable,
    generate_teacher_timetable,
    write_class_csv_with_time,
    write_teacher_csv
)
from engine.excel_export import export_pretty_excel
import json
from data.subjects import SUBJECTS

app = Flask(__name__)

# Global storage (simple & safe for college project)
solution = {}
class_tt = {}
teacher_tt = {}


# ---------------- HOME PAGE ----------------
@app.route("/")
def home():
    teachers = load_teachers()
    class_data = []

    for class_id, info in CLASSES.items():
        ct_id = info.get("class_teacher")
        ct_name = teachers[ct_id]["name"] if ct_id in teachers else "Not Assigned"

        class_data.append({
            "class_id": class_id,
            "class_teacher": ct_name
        })

    return render_template("index.html", classes=class_data)


# ---------------- TEACHERS PAGE ----------------
@app.route("/teachers")
def teachers_page():
    return render_template("teachers.html", teachers=load_teachers())


# ---------------- GENERATE TIMETABLE ----------------
@app.route("/generate", methods=["GET", "POST"])
def generate_page():
    global solution, class_tt, teacher_tt

    if request.method == "POST":
        start_time = request.form["start_time"]
        end_time = request.form["end_time"]

        variables = generate_variables(CLASSES)
        domain = generate_domain()
        solution = solve(variables, domain, CLASSES)

        class_tt = generate_class_timetable(solution)
        teacher_tt = generate_teacher_timetable(solution)

        write_class_csv_with_time(class_tt, start_time, end_time)
        write_teacher_csv(teacher_tt)
        export_pretty_excel(class_tt)

        return redirect(url_for("class_timetable_page"))

    return render_template("generate.html")


# ---------------- CLASS TIMETABLE ----------------
@app.route("/class")
def class_timetable_page():
    return render_template("class_timetable.html", timetable=class_tt)


# ---------------- TEACHER TIMETABLE ----------------
@app.route("/teacher")
def teacher_timetable_page():
    return render_template("teacher_timetable.html", timetable=teacher_tt)


# ---------------- DOWNLOAD FILES ----------------
@app.route("/download/<filename>")
def download_file(filename):
    return send_file(filename, as_attachment=True)


# ---------------- ADD TEACHER ----------------
@app.route("/add-teacher", methods=["GET", "POST"])
def add_teacher_web():
    if request.method == "POST":
        tid = request.form["teacher_id"].strip()
        name = request.form["teacher_name"].strip()
        subjects = request.form.getlist("subjects")

        with open("data/teachers.json", "r") as f:
            teachers = json.load(f)

        teachers[tid] = {
            "name": name,
            "subjects": subjects
        }

        with open("data/teachers.json", "w") as f:
            json.dump(teachers, f, indent=4)

        return redirect(url_for("teachers_page"))

    return render_template("add_teacher.html", subjects=SUBJECTS)


# ---------------- MANAGE CLASS TEACHERS ----------------
@app.route("/class-teachers", methods=["GET", "POST"])
def manage_class_teachers():
    teachers = load_teachers()

    if request.method == "POST":
        # Update class teachers
        for class_id in CLASSES:
            ct_id = request.form.get(f"class_teacher_{class_id}")
            if ct_id and ct_id in teachers:
                CLASSES[class_id]["class_teacher"] = ct_id
            else:
                CLASSES[class_id]["class_teacher"] = None

        # Save to file (in a real app, this would be a database)
        with open("data/classes.py", "w") as f:
            f.write("# data/classes.py\n\n")
            f.write("CLASSES = {\n")
            for class_id, info in CLASSES.items():
                f.write(f'    "{class_id}": {{\n')
                f.write(f'        "name": "{info["name"]}",\n')
                f.write(f'        "class_teacher": "{info["class_teacher"]}"\n')
                f.write("    },\n")
            f.write("}\n")

        return redirect(url_for("home"))

    # Prepare data for template
    class_data = []
    for class_id, info in CLASSES.items():
        ct_id = info.get("class_teacher")
        ct_name = teachers[ct_id]["name"] if ct_id and ct_id in teachers else "Not Assigned"
        class_data.append({
            "class_id": class_id,
            "name": info["name"],
            "current_teacher_id": ct_id,
            "current_teacher_name": ct_name
        })

    return render_template("class_teachers.html", classes=class_data, teachers=teachers)


if __name__ == "__main__":
    app.run(debug=True)