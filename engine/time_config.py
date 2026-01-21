# engine/time_config.py

def to_minutes(time_str):
    h, m = map(int, time_str.split(":"))
    return h * 60 + m


def minutes_to_ampm(minutes):
    hour = minutes // 60
    minute = minutes % 60

    suffix = "AM"
    if hour >= 12:
        suffix = "PM"
    if hour > 12:
        hour -= 12
    if hour == 0:
        hour = 12

    return f"{hour:02d}:{minute:02d} {suffix}"


SHORT_BREAK = 15
LUNCH_BREAK = 45


DAY_RULES = {
    "MON_THU": {
        "periods": 8,
        "short_break_after": 3,
        "lunch_after": 5,
        "has_lunch": True
    },
    "FRI": {
        "periods": 8,
        "short_break_after": 3,
        "lunch_after": 5,
        "has_lunch": True
    },
    "SAT": {
        "periods": 6,
        "short_break_after": 3,
        "has_lunch": False
    }
}


def generate_day_timing(start_time, end_time, rule):
    start = to_minutes(start_time)
    end = to_minutes(end_time)

    total_break = SHORT_BREAK + (LUNCH_BREAK if rule["has_lunch"] else 0)
    period_duration = (end - start - total_break) // rule["periods"]

    slots = []
    current = start

    for p in range(1, rule["periods"] + 1):
        p_start = minutes_to_ampm(current)
        current += period_duration
        p_end = minutes_to_ampm(current)

        slots.append({
            "period": f"P{p}",
            "time": f"{p_start} - {p_end}"
        })

        if p == rule["short_break_after"]:
            slots.append({
                "period": "BREAK",
                "time": f"{minutes_to_ampm(current)} - {minutes_to_ampm(current + SHORT_BREAK)}"
            })
            current += SHORT_BREAK

        if rule["has_lunch"] and p == rule["lunch_after"]:
            slots.append({
                "period": "LUNCH",
                "time": f"{minutes_to_ampm(current)} - {minutes_to_ampm(current + LUNCH_BREAK)}"
            })
            current += LUNCH_BREAK

    return slots


def generate_weekly_timing(start_time, end_time):
    return {
        "MONDAY": generate_day_timing(start_time, end_time, DAY_RULES["MON_THU"]),
        "TUESDAY": generate_day_timing(start_time, end_time, DAY_RULES["MON_THU"]),
        "WEDNESDAY": generate_day_timing(start_time, end_time, DAY_RULES["MON_THU"]),
        "THURSDAY": generate_day_timing(start_time, end_time, DAY_RULES["MON_THU"]),
        "FRIDAY": generate_day_timing(start_time, end_time, DAY_RULES["FRI"]),
        "SATURDAY": generate_day_timing(start_time, end_time, DAY_RULES["SAT"])
    }
