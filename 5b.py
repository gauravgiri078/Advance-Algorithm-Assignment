def solve_hour(hr, dem, src):
	"""Greedy allocation for a single hour.

	hr: hour (int)
	dem: dict of district -> demand
	src: list of sources with keys: name, cap, cost, hours (start,end)
	Returns (allocation, total_cost)
	"""
	# Filter available sources at this hour and copy mutable caps
	avail = []
	for s in src:
		start, end = s['hours']
		if start <= hr <= end:
			avail.append({'name': s['name'], 'cap': s['cap'], 'cost': s['cost']})

	# Sort sources by cost (cheapest first)
	avail.sort(key=lambda x: x['cost'])

	# Allocation storage: alloc[district][source_name] = amount
	alloc = {d: {s['name']: 0 for s in avail} for d in dem}

	# Greedy fill: for each district, use cheapest available source capacity
	for d in dem:
		need = dem[d]
		for s in avail:
			if need <= 0:
				break
			cap = s['cap']
			if cap <= 0:
				continue
			take = min(need, cap)
			s['cap'] -= take
			alloc[d][s['name']] += take
			need -= take

	# Compute total cost
	cost_map = {s['name']: s['cost'] for s in avail}
	total_cost = 0.0
	for d in alloc:
		for sname, amt in alloc[d].items():
			total_cost += amt * cost_map[sname]

	return alloc, total_cost


if __name__ == '__main__':
	# Hour 06 test case
	hr = 6
	dem = {'A': 20, 'B': 15, 'C': 25}
	src = [
		{'name': 'Solar', 'cap': 50, 'cost': 1.0, 'hours': (6, 18)},
		{'name': 'Hydro', 'cap': 40, 'cost': 1.5, 'hours': (0, 24)},
		{'name': 'Diesel', 'cap': 60, 'cost': 3.0, 'hours': (17, 23)},
	]

	allocation, total = solve_hour(hr, dem, src)

	print('Allocation:')
	for d in allocation:
		print(f" {d}:")
		for sname, amt in allocation[d].items():
			if amt > 0:
				print(f"  - {sname}: {amt} kWh")

	# Display total cost (expected Rs. 65 for Hour 06)
	if abs(total - round(total)) < 1e-9:
		total_display = int(round(total))
	else:
		total_display = total
	print(f"Total cost: Rs. {total_display}")

	# Complexity notes
	print('Time Complexity: O(H * (S log S + D * S)) where H=hours, S=sources, D=districts.')
	print('Space Complexity: O(D * S) to store allocation.')

