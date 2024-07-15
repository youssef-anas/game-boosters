def extract_ids(boss_string):
    bosses = boss_string.split(',')
    ids = [int(boss[4:]) for boss in bosses]
    return ids