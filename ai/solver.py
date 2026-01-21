# ai/solver.py

from ai.constraints import (
    teacher_clash,
    continuous_rule,
    class_teacher_p1
)
from data.subjects import SUBJECTS


def solve(variables, domain, classes):
    """
    Solves the timetable CSP using backtracking.
    variables : list of (class, day, period)
    domain    : list of (subject, teacher)
    classes   : class metadata (for class teacher rule)
    """

    assignments = {}           # (class, day, period) -> (subject, teacher)
    subject_count = {}         # (class, subject) -> count

    def backtrack(index):
        # ✅ All variables assigned → solution found
        if index == len(variables):
            return True

        var = variables[index]           # (class, day, period)
        class_id, day, period = var

        for val in domain:
            subject, teacher = val

            # 1️⃣ Class teacher must teach P1
            if not class_teacher_p1(var, val, classes):
                continue

            # 2️⃣ Teacher clash constraint
            if not teacher_clash(assignments, var, val):
                continue

            # 3️⃣ Continuous period rule
            if not continuous_rule(assignments, var, val):
                continue

            # 4️⃣ Weekly subject credit constraint
            used = subject_count.get((class_id, subject), 0)
            max_allowed = SUBJECTS.get(subject, 0)

            if used >= max_allowed:
                continue

            # ✅ Assign
            assignments[var] = val
            subject_count[(class_id, subject)] = used + 1

            # 🔁 Recurse
            if backtrack(index + 1):
                return True

            # ❌ Undo assignment (BACKTRACK)
            del assignments[var]
            subject_count[(class_id, subject)] -= 1

        return False

    backtrack(0)
    return assignments
