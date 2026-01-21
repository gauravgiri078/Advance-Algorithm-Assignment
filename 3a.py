class Node:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def solve(root):
    ans = 0
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
        l = dfs(node.left)
        r = dfs(node.right)
        if l == 0 or r == 0:
            ans += 1
            return 1
        if l == 1 or r == 1:
            return 2
        return 0

    if dfs(root) == 0:
        ans += 1
    return ans


def build_tree(arr):
    if not arr:
        return None
    nodes = [None if v is None else Node(v) for v in arr]
    n = len(arr)
    for i in range(n):
        if nodes[i] is not None:
            li = 2 * i + 1
            ri = 2 * i + 2
            if li < n:
                nodes[i].left = nodes[li]
            if ri < n:
                nodes[i].right = nodes[ri]
    return nodes[0]


if __name__ == "__main__":
    arr = [0, 0, None, 0, None, 0, None, None, 0]
    root = build_tree(arr)
    print(solve(root))
    
    
    print("Time Complexity: O(N)")
    print("Space Complexity: O(H)")
