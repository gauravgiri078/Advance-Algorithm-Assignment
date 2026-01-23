def solve(tiles):
	nums = [1] + tiles + [1]
	n = len(nums)
	dp = [[0] * n for _ in range(n)]

	for L in range(2, n):
		for i in range(0, n - L):
			j = i + L
			for k in range(i + 1, j):
				val = nums[i] * nums[k] * nums[j] + dp[i][k] + dp[k][j]
				if val > dp[i][j]:
					dp[i][j] = val

	return dp[0][n - 1]


if __name__ == "__main__":
	tiles = [1, 5]
	result = solve(tiles)
	print(result)
	print("Time Complexity: O(n^3)")
	print("Space Complexity: O(n^2)")

