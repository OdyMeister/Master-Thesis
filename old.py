def generate_schedules(n, matchups, schedules, schedule=[]):
    if len(schedule) is (n-1) * n:
        schedules.append(schedule)
        return

    prev = []
    index = len(schedule) % (n // 2)

    if index != 0:
        temp = schedule[-index:]
        for t in temp:
            prev.append(t[0])
            prev.append(t[1])

    for m in matchups:
        if len(prev) > 0 and (m[0] in prev or m[1] in prev):
            continue

        new_matchups = matchups.copy()
        new_matchups.remove(m)
        new_schedule = schedule.copy()
        new_schedule.append(m)

        generate_schedules(n, new_matchups, schedules, new_schedule)