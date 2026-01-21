def teacher_clash(assignments, var, val):
    _, d, p = var
    _, t = val
    for (_, d2, p2), (_, t2) in assignments.items():
        if d == d2 and p == p2 and t == t2:
            return False
    return True

def continuous_rule(assignments, var, val):
    c, d, p = var
    s, t = val
    pno = int(p[1:])

    count = 1
    for (c2,d2,p2),(s2,t2) in assignments.items():
        if c==c2 and d==d2 and t==t2:
            if abs(int(p2[1:]) - pno) == 1:
                if s2 != s:
                    return False
                count += 1
    return count <= 2

def class_teacher_p1(variable, value, classes):
    class_id, _, period = variable
    _, teacher = value

    if period != "P1":
        return True

    return classes[class_id]["class_teacher"] == teacher
