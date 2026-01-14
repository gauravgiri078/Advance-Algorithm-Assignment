import random
import math
import time

N = 20

def dist(a, b):
	return math.hypot(a[0]-b[0], a[1]-b[1])

def total_distance(cities, tour):
	d = 0.0
	for i in range(len(tour)):
		a = cities[tour[i]]
		b = cities[tour[(i+1) % len(tour)]]
		d += dist(a, b)
	return d

def two_opt_swap(tour):
	n = len(tour)
	i = random.randrange(0, n-1)
	j = random.randrange(i+1, n)
	new = tour[:i] + tour[i:j+1][::-1] + tour[j+1:]
	return new

def swap_two(tour):
	n = len(tour)
	i, j = random.sample(range(n), 2)
	new = tour[:]
	new[i], new[j] = new[j], new[i]
	return new

def exp_schedule(T0, alpha, k):
	return T0 * (alpha ** k)

def lin_schedule(T0, beta, k):
	return T0 - beta * k

def simulated_annealing(cities, T0, schedule, param, max_iters=5000):
	n = len(cities)
	curr_tour = list(range(n))
	random.shuffle(curr_tour)
	curr_d = total_distance(cities, curr_tour)
	best_tour = curr_tour[:]
	best_d = curr_d

	for k in range(1, max_iters+1):
		if random.random() < 0.5:
			new_tour = two_opt_swap(curr_tour)
		else:
			new_tour = swap_two(curr_tour)

		new_d = total_distance(cities, new_tour)
		delta = new_d - curr_d

		if schedule == 'exp':
			temp = exp_schedule(T0, param, k)
		else:
			temp = lin_schedule(T0, param, k)

		if temp <= 0:
			break

		if delta < 0 or random.random() < math.exp(-delta / temp):
			curr_tour = new_tour
			curr_d = new_d
			if curr_d < best_d:
				best_d = curr_d
				best_tour = curr_tour[:]

	return best_d, best_tour

def main():
	random.seed(0)
	cities = [(random.uniform(0,1000), random.uniform(0,1000)) for _ in range(N)]

	T0 = 1000.0
	max_iters = 5000

	alpha = 0.995
	start = time.time()
	best_exp_d, _ = simulated_annealing(cities, T0, 'exp', alpha, max_iters)
	t_exp = time.time() - start

	beta = T0 / max_iters
	start = time.time()
	best_lin_d, _ = simulated_annealing(cities, T0, 'lin', beta, max_iters)
	t_lin = time.time() - start

	print(f"Exponential schedule best distance: {best_exp_d:.4f} (time {t_exp:.3f}s)")
	print(f"Linear schedule best distance:      {best_lin_d:.4f} (time {t_lin:.3f}s)")
	print("Time Complexity: O(K * N)")

if __name__ == '__main__':
	main()

