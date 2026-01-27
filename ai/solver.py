# ai/solver.py

from data.subjects import SUBJECTS
import random

def solve(variables, domain, classes):
    """
    Greedy constructive solver - assigns subjects to meet minimum requirements
    """
    assignments = {}
    subject_count = {}
    
    # Group variables by class
    class_vars = {}
    for var in variables:
        class_id = var[0]
        if class_id not in class_vars:
            class_vars[class_id] = []
        class_vars[class_id].append(var)
    
    # For each class, assign subjects greedily
    for class_id, vars_list in class_vars.items():
        # Shuffle variables to randomize assignment
        random.shuffle(vars_list)
        
        # Track remaining requirements
        remaining = SUBJECTS.copy()
        
        for var in vars_list:
            day, period = var[1], var[2]
            
            # Find available assignments for this slot
            available = []
            for subject, teacher in domain:
                if remaining.get(subject, 0) > 0:
                    # Check teacher availability
                    conflict = False
                    for other_var, other_val in assignments.items():
                        other_day, other_period = other_var[1], other_var[2]
                        other_teacher = other_val[1]
                        if other_day == day and other_period == period and other_teacher == teacher:
                            conflict = True
                            break
                    if not conflict:
                        available.append((subject, teacher))
            
            if available:
                # Pick random available assignment
                subject, teacher = random.choice(available)
                assignments[var] = (subject, teacher)
                remaining[subject] -= 1
                subject_count[(class_id, subject)] = subject_count.get((class_id, subject), 0) + 1
    
    # Verify all requirements are met
    for class_id in classes:
        for subject in SUBJECTS:
            assigned = subject_count.get((class_id, subject), 0)
            if assigned < SUBJECTS[subject]:
                raise Exception(
                    f"❌ Timetable could not be generated.\n"
                    f"Class {class_id} needs {SUBJECTS[subject]} {subject} but only got {assigned}."
                )
    
    return assignments
