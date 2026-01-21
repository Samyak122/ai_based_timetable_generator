# ai/variables.py

# Days in a school week
DAYS = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY"]

# Teaching periods per day (NO breaks here)
PERIODS_BY_DAY = {
    "MONDAY":    ["P1","P2","P3","P4","P5","P6","P7","P8"],
    "TUESDAY":   ["P1","P2","P3","P4","P5","P6","P7","P8"],
    "WEDNESDAY": ["P1","P2","P3","P4","P5","P6","P7","P8"],
    "THURSDAY":  ["P1","P2","P3","P4","P5","P6","P7","P8"],
    "FRIDAY":    ["P1","P2","P3","P4","P5","P6","P7","P8"],
    "SATURDAY":  ["P1","P2","P3","P4","P5","P6"]
}


def generate_variables(classes):
    """
    Generates CSP variables of the form:
    (class_id, day, period)
    """
    variables = []

    for class_id in classes:
        for day in DAYS:
            for period in PERIODS_BY_DAY[day]:
                variables.append((class_id, day, period))

    return variables
