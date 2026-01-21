from data.teacher_loader import load_teachers
from data.subjects import SUBJECTS

teachers = load_teachers()

# Count how many teachers can teach each subject
subject_coverage = {}
for subj in SUBJECTS.keys():
    count = 0
    qualified_teachers = []
    for tid, t in teachers.items():
        if subj in t['subjects']:
            count += 1
            qualified_teachers.append(tid)
    subject_coverage[subj] = {
        'count': count,
        'teachers': qualified_teachers,
        'required_credits': SUBJECTS[subj]
    }

print('Subject Coverage Analysis:')
for subj, info in subject_coverage.items():
    status = 'OK' if info['count'] > 0 else 'NONE'
    print(f'{subj}: {info["count"]} teachers, {info["required_credits"]} credits - {status}')

# Check if any subject has no teachers
missing_subjects = [subj for subj, info in subject_coverage.items() if info['count'] == 0]
if missing_subjects:
    print(f'Critical: No teachers for subjects: {missing_subjects}')
else:
    print('All subjects have qualified teachers')