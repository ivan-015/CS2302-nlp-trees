# Ivan Vigliante
# CS2302 TR 10:20am-11:50am
# Lab 3A
# Professor Aguirre, Diego
# TA Saha, Manoj
# Date of last modification: 10/24/2018
# This program represents an AVL tree meant to be used from another program
# Implementation from ZyBooks.com

class AVLTree:

    def __init__(self):
        self.root = None

    # Rotates left at a node and returns the new root of subtree
    def rotate_left(self, node):
        # Get the left child of this node's right child
        right_left_child = node.right.left

        # Replace the current node for the right child if node has parent
        if node.parent is not None:
            node.parent.replace_child(node, node.right)
        # Otherwise, set the node's left child to the new root
        else:
            self.root = node.right
            self.root.parent = None

        # Make the right child of the node its new parent, on the left
        node.right.set_child("left", node)

        # Make the left_right_child the node's right child
        node.set_child("right", right_left_child)

        # Return the new roof of subtree/tree
        return node.parent

    # Rotates right at a node and returns the new root of subtree
    def rotate_right(self, node):
        # Right child of the node's left child
        left_right_child = node.left.right

        # If node has a parent, make node.left the parent's new left child
        if node.parent is not None:
            node.parent.replace_child(node, node.left)
        # Otherwise, set the node's left child to the new root
        else:
            self.root = node.left
            self.root.parent = None

        # Make the left child of the node its new parent, on the right
        node.left.set_child("right", node)

        # Make left_right_child the node's new left child
        node.set_child("left", left_right_child)

        # Return the new root of subtree/tree
        return node.parent

    # Re-balances the tree by rotating ,if required.
    def rebalance(self, node):

        node.update_height()

        # Imbalance happens to the right
        if node.get_balance() == -2:
            # Double rotation needed, so rotate right on the right child first
            if node.right.get_balance() == 1:
                self.rotate_right(node.right)

            # Rotate left on the node to re-balance tree
            return self.rotate_left(node)

        # Imbalance happens to the left
        elif node.get_balance() == 2:
            # Double rotation needed, so rotate left on left child
            if node.left.get_balance() == -1:
                self.rotate_left(node.left)

            # Rotate right on the node to re-balance tree
            return self.rotate_right(node)

        # No imbalance, return the node
        return node

    def insert(self, node):

        # If tree is empty, make the node the root
        if self.root is None:
            self.root = node
            self.root.parent = None
            return

        # Search for where the node should be inserted
        curr = self.root
        while curr is not None:
            # If the node to insert is less than the current node being inspected, go left
            if node.item < curr.item:
                # If the left is none, insert node here
                if curr.left is None:
                    curr.left = node
                    node.parent = curr
                    break
                # Otherwise continue with the search
                curr = curr.left
            # If the node to insert is greater than the current node being inspected, go right
            else:
                # If the right is none, insert node here
                if curr.right is None:
                    curr.right = node
                    node.parent = curr
                    break
                # Otherwise continue with the search
                curr = curr.right

        # Re-balance the tree if necessary
        node = node.parent
        while node is not None:
            self.rebalance(node)
            node = node.parent

    def remove_node(self, node):
        if node is None:
            return False

        parent = node.parent

        # Removing the root node
        if node is self.root:
            # If the left is populated, make it the new root
            if node.left is not None:
                self.root = node.left
            # Otherwise, make the root the right node
            else:
                self.root = node.right

            # If the root is not node, set its parent to none
            if self.root is not None:
                self.root.parent = None
            return True

        # Internal node with 2 children
        elif node.left is not None and node.right is not None:
            successor = node.right
            # Get the new node to replace node to be removed
            while successor.left is not None:
                successor = successor.left
            # Move the value from successor to the node
            node.item = successor.item
            node.embedding = successor.embedding

            # Remove successor node since it has been moved up
            self.remove_node(successor)
            return True

        # Internal node with a left child only
        elif node.left is not None:
            parent.replace_child(node, node.left)
        # Internal node with only right child or leaf
        else:
            parent.replace_child(node, node.right)

        # After removing the node, re-balance the tree
        node = parent
        while node is not None:
            self.rebalance(node)
            node = node.parent

        return True

    # Searches for a key inside the tree
    def search(self, key):
        current = self.root
        while current is not None:
            # If the keys are the same, return the node
            if current.item == key:
                return current
            # If the item in the node is less than the key, go right
            elif current.item < key:
                current = current.right
            # Otherwise, go left
            else:
                current = current.left

    # Searches for the key inside the tree and removes a node if
    # the key is in the tree
    def remove_key(self, key):
        node = self.search(key)
        # If the key is not in the tree, return false
        if node is None:
            return False
        # Otherwise, remove the node
        else:
            return self.remove_node(node)

# Node class for AVL Tree
class AVLNode:

    def __init__(self, item, embedding):
        self.item = item
        self.embedding = embedding
        self.left = None
        self.right = None
        self.parent = None
        self.height = 0

    # Calculates the balance of the current node
    def get_balance(self):
        # Get the height of the left subtree
        left_height = -1
        if self.left is not None:
            left_height = self.left.height

        # Get the height of the right subtree
        right_height = -1
        if self.right is not None:
            right_height = self.right.height

        # return balance factor
        return left_height - right_height

    # Updates the height of the tree after it has
    # been modified
    def update_height(self):
        # Get height of left subtree
        left_height = -1
        if self.left is not None:
            left_height = self.left.height

        # Get height of right subtree
        right_height = -1
        if self.right is not None:
            right_height = self.right.height

        # New height is the max between the two +1 counting the root
        self.height = max(left_height, right_height) + 1

    # Set the left or right child of a node to insert_node
    def set_child(self, lr_child, insert_node):
        # Return false if invalid parameter was passed
        if lr_child != "left" and lr_child != "right":
            return False

        # Place the insert node in the left or right subtree
        if lr_child == "left":
            self.left = insert_node
        else:
            self.right = insert_node

        # If the insert node is not none, make the current node its parent
        if insert_node is not None:
            insert_node.parent = self

        # Since the tree was modified, update its height
        self.update_height()

        return True

    # Replaces the current node with a new one
    def replace_child(self, replace, new):
        # If the left or right of this node matches the node to replace,
        # call the set_child method where the new node should go
        if self.left is replace:
            return self.set_child("left", new)
        elif self.right is replace:
            return self.set_child("right", new)

        # Returns false if neither the left nor right children match the node to replace
        return False