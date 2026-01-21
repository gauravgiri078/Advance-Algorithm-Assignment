class Node:
	def __init__(self, val=0, left=None, right=None):
		self.val = val
		self.left = left
		self.right = right


def solve(root):
	ans = 0

	def dfs(node):
		nonlocal ans
		if not node:
			return 2
		L = dfs(node.left)
		R = dfs(node.right)
		if L == 0 or R == 0:
			ans += 1
			return 1
		if L == 1 or R == 1:
			return 2
		return 0

	if dfs(root) == 0:
		ans += 1
	return ans


def build_tree(arr):
	if not arr:
		return None
	nodes = [None if v is None else Node(v) for v in arr]
	for i in range(len(arr)):
		if nodes[i] is not None:
			l = 2 * i + 1
			r = 2 * i + 2
			if l < len(arr):
				nodes[i].left = nodes[l]
			if r < len(arr):
				nodes[i].right = nodes[r]
	return nodes[0]


if __name__ == '__main__':
	# test: tree = [0,0,null,0,null,0,null,null,0]
	arr = [0, 0, None, 0, None, 0, None, None, 0]
	root = build_tree(arr)
	res = solve(root)
	print(res)
	print('Time Complexity: O(N)')
	print('Space Complexity: O(H)')

