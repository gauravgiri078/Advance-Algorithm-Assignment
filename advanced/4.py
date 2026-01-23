def allocate(hour, demands, sources):
    # find available sources
    avail = []
    for src in sources:
        if hour in src['hours'] and src['cap'] > 0:
            avail.append({'name': src['name'], 'cap': src['cap'], 'cost': src['cost']})
    avail.sort(key=lambda x: x['cost'])

    alloc = {d: {} for d in demands}

    for dist, dem in demands.items():
        need = dem
        for s in avail:
            if need <= 0:
                break
            if s['cap'] <= 0:
                continue
            use = min(s['cap'], need)
            alloc[dist][s['name']] = alloc[dist].get(s['name'], 0) + use
            s['cap'] -= use
            need -= use

        # allow up to 10% extra if still short
        if need > 0:
            extra_allowed = dem * 0.1
            extra = extra_allowed
            for s in avail:
                if extra <= 0:
                    break
                if s['cap'] <= 0:
                    continue
                use = min(s['cap'], extra)
                alloc[dist][s['name']] = alloc[dist].get(s['name'], 0) + use
                s['cap'] -= use
                extra -= use

    return alloc


if __name__ == '__main__':
    hour = 6
    dem = {'A': 20, 'B': 15, 'C': 25}
    srcs = [
        {'name': 'Solar', 'cap': 50, 'cost': 1.0, 'hours': set(range(6, 19))},
        {'name': 'Hydro', 'cap': 40, 'cost': 1.5, 'hours': set(range(0, 24))},
    ]

    alloc = allocate(hour, dem, srcs)

    print('Hour | District | Source | Used | % Met')
    total_by_src = {}
    for d, demand in dem.items():
        used_total = 0
        if alloc.get(d):
            for sname, used in alloc[d].items():
                used_total += used
                total_by_src[sname] = total_by_src.get(sname, 0) + used
                pct = (used_total / demand) * 100 if demand > 0 else 100
                print(f"{hour} | {d} | {sname} | {used} | {pct:.1f}%")
        else:
            print(f"{hour} | {d} | None | 0 | 0.0%")

    print('\nTotal used by source:')
    for s, t in total_by_src.items():
        print(f"{s}: {t}")

    print('\nTime Complexity: O(H * D * S)')
    print('Space Complexity: O(D * S)')
