class Node():
    """
    Represents a node in a left-leaning red-black tree.
	If multiple nodes have the same key, their values are all stored in a
	single node as a list.
    """
    def __init__(self, key, value, coloured):
        self.key = key
        self.value = value
        self.coloured = coloured  # true if node is red
        self.left = None
        self.right = None


def rotate_left(node):
    right_child = node.right
    node.right = right_child.left
    right_child.left = node
    right_child.coloured = node.coloured
    node.coloured = True
    return right_child


def rotate_right(node):
    left_child = node.left
    node.left = left_child.right
    left_child.right = node
    left_child.coloured = node.coloured
    node.coloured = True
    return left_child


def colour_flip(node):
    node.coloured = True
    node.left.coloured = False
    node.right.coloured = False


def is_red(node):
    if node:
        return node.coloured
    return False


class LLRBTree():
    """
    Represents a left-leaning red-black tree.
    Mantains the following invariants:
        - each path from the root to a leaf has the same number
        of black nodes
        - no node has two red children
        - red nodes lean to the left
    """
    
    def __init__(self, key, value):
        self.root = Node(key, value, False)

    def get(self, node, key_to_find):
        # look for a key in the tree and return the value of its node
        if key_to_find == node.key:
            return node.value
        elif key_to_find < node.key:
            return self.get(node.left, key_to_find)
        elif key_to_find > node.key:
            return self.get(node.right, key_to_find)
        
    def insert(self, node, key, value):
        # insert a new key, value pair into the tree
        if node is None:
            return Node(key, value, True)

        if key == node.key:
            try:
                node.value.append(value)
            except AttributeError:
                node.value = [node.value]
                node.value.append(value)
        elif key < node.key:
            node.left = self.insert(node.left, key, value)
        else:
            node.right = self.insert(node.right, key, value)
        
        return self._fix_up(node)

    def _fix_up(self, node):
        # checks if a node needs to be rotated or have its colour flipped
        # to mantain the invariants
        if is_red(node.right) and not is_red(node.left):
            if node is self.root:
                self.root = node.right
            node = rotate_left(node)

        if is_red(node.left) and is_red(node.left.left):
            if node is self.root:
                self.root = node.left
            node = rotate_right(node)

        if is_red(node.left) and is_red(node.right):
            colour_flip(node)
        
        return node

    def traverse(self, node):
        # credit: geeksforgeeks
        # returns a list with all the keys in the tree
        # in ascending order (in-order traversal)
        traversed = []
        if not node:
            return traversed
        
        traversed = self.traverse(node.left)
        traversed.append(node.key)
        traversed = traversed + self.traverse(node.right)
        return traversed

    def height(self, root):
		# return the height of tallest branch in the tree
        if root is None:
            return 0
        else:
            return max(self.height(root.left), self.height(root.right)) + 1
    
    def min(self, node):
		# returns the key and value of the node with the smallest key in the tree
        if node.left:
            return self.min(node.left)
        else:
            return node.key, node.value
    
    def max(self, node):
		# returns the key and value of the node with the largest key in the tree
        if node.right:
            return self.max(node.right)
        else:
            return node.key, node.value

    def floor(self, node, threshold, current_floor = None):
        # returns the key and value of the node with the
		# largest key such that the key <= threshold
        if threshold == node.key:
            return node.key, node.value
        elif threshold < node.key and node.left:
            return self.floor(node.left, threshold, current_floor)
        elif threshold > node.key and node.right:
            return self.floor(node.right, threshold, node)
        else:
            if node.key < threshold:
                current_floor = node

        if current_floor:
            return current_floor.key, current_floor.value
    
    def ceiling(self, node, threshold, current_ceiling = None):
        # returns the key and value of the node with the
		# smallest key such that the key >= threshold
        if threshold == node.key:
            return node.key, node.value
        elif threshold < node.key and node.left:
            return self.ceiling(node.left, threshold, node)
        elif threshold > node.key and node.right:
            return self.ceiling(node.right, threshold, current_ceiling)
        else:
            if node.key > threshold:
                current_ceiling = node
        
        if current_ceiling:
            return current_ceiling.key, current_ceiling.value
    
    def range(self, node, start, end):
		# returns a list of all nodes with keys between the start 
		# and end values
        traversed = []
        if not node:
            return traversed
        if node.key < start:
            traversed = traversed + self.range(node.right, start, end)
        elif node.key > end:
            traversed = traversed + self.range(node.left, start, end)
        else:
            traversed = traversed + self.range(node.left, start, end)
            traversed.append(node.key)
            traversed = traversed + self.range(node.right, start, end)
        return traversed


if __name__ == "__main__":
	rbtree = LLRBTree(20, "Standing")

	rbtree.insert(rbtree.root, 15, "here,")
	rbtree.insert(rbtree.root, 25, "I realize")
	rbtree.insert(rbtree.root, 18, "you are")
	rbtree.insert(rbtree.root, 13, "just like me")
	rbtree.insert(rbtree.root, 228, "trying to make history")

	print(rbtree.ceiling(rbtree.root, 20))
	print(rbtree.floor(rbtree.root, 16))

	for i in rbtree.traverse(rbtree.root):
		print(i)

	for i in (rbtree.range(rbtree.root, 14, 30)):
		print(i)
    