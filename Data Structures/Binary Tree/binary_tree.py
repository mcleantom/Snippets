from __future__ import annotations

from random import randint
from typing import Any, Optional
from collections import deque

class TreeNode:

    def __init__(self, value: Any, left: Optional[TreeNode] = None, right: Optional[TreeNode] = None):
        self.value = value
        self.left = left
        self.right = right


class BinaryTree:

    def __init__(self):
        self.root: Optional[TreeNode] = None

    def add_node(self, value) -> TreeNode:
        if self.root is None:
            self.root = TreeNode(value)
            return self.root

        node = self.root

        while True:
            if value < node.value:
                if node.left is not None:
                    node = node.left
                else:
                    node.left = TreeNode(value)
                    return node.left
            else:
                if node.right is not None:
                    node = node.right
                else:
                    node.right = TreeNode(value)
                    return node.right

    def breadth_first_search(self, node: TreeNode = None, max_depth=float("inf")):
        """
        Traverse the tree using a breadth first search.

        Example:
            for node in tree.breadth_first_search():
                print(node.value)
        """
        if node is None:
            node = self.root

        queue = deque([(node, 0)])
        while queue:
            node, depth = queue.popleft()
            if node and depth < max_depth:
                yield node, depth
                if node.left:
                    queue.append((node.left, depth + 1))
                if node.right:
                    queue.append((node.right, depth + 1))

    def depth_first_search(self, node: TreeNode = None, max_depth=float("inf")):
        """
        Traverse the tree using a depth first search.

        Example:
            for node in tree.depth_first_search():
               print(node.value)
        """
        if node is None:
            node = self.root

        stack = [(node, 0)]
        while stack:
            node, depth = stack.pop()
            if node and depth < max_depth:
                yield node, depth
                stack.append((node.left, depth+1))
                stack.append((node.right, depth+1))

    def search(self, value, node: TreeNode = None):
        if node is None:
            node = self.root

        while node:
            if node.value == value:
                return node
            if node.value > value:
                node = node.left
            else:
                node = node.right

        return node

    def is_balanced(self, node: TreeNode):
        """
        Binary tree is balanced if:
            1.  The absolute difference between heights of left and right subtrees at any
                node is less than 1.
            2.  For each node, the left subtree is a balanced binary tree.
            3.  For each node, the right subtree is a balanced binary tree.
        """
        if node is None:
            return True

        left_depth = self.depth(node.left)
        right_depth = self.depth(node.right)

        return (
            (abs(left_depth-right_depth) <=1) and
            self.is_balanced(node.left) and
            self.is_balanced(node.right)
        )

    def depth(self, node: TreeNode):
        """
        Get the depth of a tree, from a given node.

        Could this function be cached?
        """
        if node is None:
            return 0
        return max(
            self.depth(node.left),
            self.depth(node.right)
        ) + 1


def main():
    tree = BinaryTree()
    for _ in range(20):
        tree.add_node(randint(0, 10))

    for node, depth in tree.depth_first_search():
        print(f"{' '*depth}    {node.value}")

    print(tree.is_balanced(tree.root))


if __name__ == "__main__":
    main()
