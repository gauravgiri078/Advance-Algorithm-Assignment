import math


def get_min_distance(sensors):
	"""Compute geometric median using Weiszfeld's algorithm.

	sensors: list of [x, y]
	Returns: (hub_x, hub_y, total_distance)
	"""
	if not sensors:
		return None, None, 0.0

	n = len(sensors)
	hub_x = sum(p[0] for p in sensors) / n
	hub_y = sum(p[1] for p in sensors) / n

	tol = 1e-6
	max_iter = 10000

	for _ in range(max_iter):
		num_x = 0.0
		num_y = 0.0
		denom = 0.0

		for sensor in sensors:
			sensor_x, sensor_y = sensor[0], sensor[1]
			dx = sensor_x - hub_x
			dy = sensor_y - hub_y
			dist = math.hypot(dx, dy)

			# skip sensor if coincides with current hub (avoid div by zero)
			if dist < 1e-12:
				continue

			w = 1.0 / dist
			num_x += sensor_x * w
			num_y += sensor_y * w
			denom += w

		if denom == 0.0:
			break

		hub_next_x = num_x / denom
		hub_next_y = num_y / denom

		if abs(hub_next_x - hub_x) < tol and abs(hub_next_y - hub_y) < tol:
			hub_x, hub_y = hub_next_x, hub_next_y
			break

		hub_x, hub_y = hub_next_x, hub_next_y

	total_distance = sum(math.hypot(p[0] - hub_x, p[1] - hub_y) for p in sensors)

	return hub_x, hub_y, total_distance


if __name__ == "__main__":
	sensor_locations = [[1, 1], [3, 3]]

	hub_x, hub_y, min_dist = get_min_distance(sensor_locations)

	print(f"Final hub coordinates: ({hub_x:.6f}, {hub_y:.6f})")
	print(f"Minimum distance sum: {min_dist:.6f}")
	print("Time Complexity: O(N*K)")
	print("Space Complexity: O(1) excluding input storage")
	print("Note: sensors that coincide with the current hub are skipped to avoid division by zero.")

