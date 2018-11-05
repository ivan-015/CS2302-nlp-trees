# Ivan Vigliante
# CS2302 TR 10:20am-11:50am
# Lab 3A
# Professor Aguirre, Diego
# TA Saha, Manoj
# Date of last modification: 10/24/2018
# This program represents a red black tree meant to be used from another program
# Implementation from ZyBooks.com


class RBTNode:
    def __init__(self, item, embedding, parent, is_red=False, left=None, right=None):
        self.item = item
        self.embedding = embedding
        self.left = left
        self.right = right
        self.parent = parent

        if is_red:
            self.color = "red"
        else:
            self.color = "black"

    # Checks if both children nodes are black and returns true is that is the case
    def are_both_children_black(self):
        # If left or right children are red return false
        if self.left is not None and self.left.is_red():
            return False
        if self.right is not None and self.right.is_red():
            return False
        return True

    # Counts the number of nodes in the tree
    def count(self):
        # Count the current node
        counter = 1
        # If left child is not none, recursively count left child
        if self.left is not None:
            counter = counter + self.left.count()
        # If right child is not none, recursively count right child
        if self.right is not None:
            counter = counter + self.right.count()
        # After all nodes have been checked return count
        return counter

    # Returns grandparent of current node
    def get_grandparent(self):
        # If the parent of the current node is none, return none
        if self.parent is None:
            return None
        # Otherwise, return grandfather
        return self.parent.parent

    # Gets node's predecessor from left child
    # Left child cannot be empty
    def get_predecessor(self):
        # Go to left node
        node = self.left
        # Get rightmost node from left child
        while node.right is not None:
            node = node.right
        return node

    # Gets the current node's sibling
    def get_sibling(self):
        if self.parent is not None:
            # If the current node is the left child, return right child of parent
            if self is self.parent.left:
                return self.parent.right
            # Otherwise, return the left
            return self.parent.left
        # Return none if parent is None
        return None

    # Gets the node's uncle
    def get_uncle(self):
        # Get the grandparent of node
        grandparent = self.get_grandparent()
        # If no grandparent, return none
        if grandparent is None:
            return None
        # If node's parent is grandparent's left child, return
        # right child of node's grandparent
        if grandparent.left is self.parent:
            return grandparent.right
        # Otherwise, return left child of grandparent
        return grandparent.left

    def is_black(self):
        return self.color == "black"

    def is_red(self):
        return self.color == "red"

    def set_child(self, which_child, child):
        # Return false if given anything other than left or right
        if which_child != "left" and which_child != "right":
            return False

        # Replaces left child of current node
        if which_child == "left":
            self.left = child
        # Replaces right child of current node
        else:
            self.right = child

        # Set the parent if child is not none
        if child is not None:
            child.parent = self

        return True

    # Replaces the node's child with a new node
    def replace_child(self, current_child, new_child):
        # If the left matches current_child, replace it
        if self.left is current_child:
            return self.set_child("left", new_child)
        # If the right matches current_child, replace it
        elif self.right is current_child:
            return self.set_child("right", new_child)
        # Node to replace is neither on the left or right, return false
        return False

class RBTree:
    def __init__(self):
        self.root = None

    def __len__(self):
        if self.root is None:
            return 0
        return self.root.count()

    def insert(self, item, embedding):
        # When inserting new node, always red
        new_node = RBTNode(item, embedding, None, True, None, None)
        # Insert the new node into RBTree
        self.insert_node(new_node)

    # Function that inserts a node and re-balances if necessary
    def insert_node(self, node):
        # If root is none, insert node as root
        if self.root is None:
            self.root = node
        else:
            # Traverse tree to insert node
            current_node = self.root
            while current_node is not None:
                # If the item of the node to insert is less than the node being looked
                # at, insert if left is none, or continue left is there is another child
                if node.item < current_node.item:
                    if current_node.left is None:
                        current_node.set_child("left", node)
                        break
                    current_node = current_node.left
                # If the item of the node to insert is greater than the node being looked
                # at, insert if right child is none, or continue right if there is another child
                else:
                    if current_node.right is None:
                        current_node.set_child("right", node)
                        break
                    current_node = current_node.right

        # insert node as red
        node.color = "red"

        # re-balance if necessary
        self.insertion_balance(node)

    # Function that balances the tree after inserting
    def insertion_balance(self, node):
        # If a root was just inserted, make it black
        if node.parent is None:
            node.color = "black"
            return

        # If parent is black, return
        if node.parent.is_black():
            return

        parent = node.parent
        grandparent = node.get_grandparent()
        uncle = node.get_uncle()

        # If parent and uncle are red, color parent and uncle black,
        # Make grandparent red and balance grandparent
        if uncle is not None and uncle.is_red():
            parent.color = uncle.color = "black"
            grandparent.color = "red"
            self.insertion_balance(grandparent)
            return

        # if node is right child of parent, and parent is left child of grandparent,
        # rotate left at parent
        if node is parent.right and parent is grandparent.left:
            self.rotate_left(parent)
            node = parent
            parent = node.parent
        elif node is parent.left and parent is grandparent.right:
            self.rotate_right(parent)
            node = parent
            parent = node.parent

        parent.color = "black"
        grandparent.color = "red"

        # If node is left child of parent, rotate right at grandparent
        if node is parent.left:
            self.rotate_right(grandparent)
        # Otherwise, rotate left at grandparent
        else:
            self.rotate_left(grandparent)

    def rotate_left(self, node):
        right_left_child = node.right.left
        # Rotating on an internal node
        if node.parent is not None:
            node.parent.replace_child(node, node.right)
        # Rotating on the root
        else:
            self.root = node.right
            self.root.parent = None

        node.right.set_child("left", node)
        node.set_child("right", right_left_child)

    def rotate_right(self, node):
        left_right_child = node.left.right
        # Rotating on an internal node
        if node.parent is not None:
            node.parent.replace_child(node, node.left)
        # Rotating on the root
        else:
            self.root = node.left
            self.root.parent = None
        node.left.set_child("right", node)
        node.set_child("left", left_right_child)

    def _bst_remove(self, item):
        node = self.search(item)
        self._bst_remove_node(node)

    def _bst_remove_node(self, node):
        # Return if trying to remove empty node
        if node is None:
            return

        # Removing internal node with 2 children
        if node.left is not None and node.right is not None:
            # Find successor
            successor_node = node.right
            while successor_node.left is not None:
                successor_node = successor_node.left

            # Copy successor's item and embedding
            successor_item = successor_node.item
            successor_embedding = successor_node.embedding

            # Recursively remove successor
            self._bst_remove_node(successor_node)

            # Set node's item and embedding to copied successor values
            node.item = successor_item
            node.embedding = successor_embedding

        # Removing root node (with 1 or 0 children)
        elif node is self.root:
            if node.left is not None:
                self.root = node.left
            else:
                self.root = node.right

            # Set parent to none since removed root
            if self.root is not None:
                self.root.parent = None

        # Removing internal node with left child only
        elif node.left is not None:
            node.parent.replace_child(node, node.left)

        # Removing internal with right child or removing leaf
        else:
            node.parent.replace_child(node, node.right)

    # Returns true if node is black
    def is_none_or_black(self, node):
        if node is None:
            return True
        return node.is_black()

    # Returns true if node is red
    def is_not_none_and_red(self, node):
        if node is None:
            return False
        return node.is_red()

    def prepare_for_removal(self, node):
        if self.try_case1(node):
            return

        sibling = node.get_sibling()
        if self.try_case2(node, sibling):
            sibling = node.get_sibling()
        if self.try_case3(node, sibling):
            return
        if self.try_case4(node, sibling):
            return
        if self.try_case5(node, sibling):
            sibling = node.get_sibling()
        if self.try_case6(node, sibling):
            sibling = node.get_sibling()

        sibling.color = node.parent.color
        node.parent.color = "black"
        if node is node.parent.left:
            sibling.right.color = "black"
            self.rotate_left(node.parent)
        else:
            sibling.left.color = "black"
            self.rotate_right(node.parent)

    def remove(self, item):
        node = self.search(item)
        if node is not None:
            self.remove_node(node)
            return True
        return False

    def remove_node(self, node):
        if node.left is not None and node.right is not None:
            # Get predecessor node, item and embedding
            predecessor_node = node.get_predecessor()
            predecessor_item = predecessor_node.item
            predecessor_embedding = predecessor_node.embedding
            self.remove_node(predecessor_node)
            node.item = predecessor_item
            node.embedding = predecessor_embedding
            return

        if node.is_black():
            self.prepare_for_removal(node)
        self._bst_remove(node.item)

        # One special case if the root was changed to red
        if self.root is not None and self.root.is_red():
            self.root.color = "black"

    def search(self, item):
        current_node = self.root
        while current_node is not None:
            # Return the node if the item matches.
            if current_node.item == item:
                return current_node

            # Navigate to the left if the search item is
            # less than the node's item.
            elif item < current_node.item:
                current_node = current_node.left

            # Navigate to the right if the search item is
            # greater than the node's item.
            else:
                current_node = current_node.right

        # item was not found
        return None

    def try_case1(self, node):
        if node.is_red() or node.parent is None:
            return True
        return False  # node case 1

    def try_case2(self, node, sibling):
        if sibling.is_red():
            node.parent.color = "red"
            sibling.color = "black"
            if node is node.parent.left:
                self.rotate_left(node.parent)
            else:
                self.rotate_right(node.parent)
            return True
        return False  # not case 2

    def try_case3(self, node, sibling):
        if node.parent.is_black() and sibling.are_both_children_black():
            sibling.color = "red"
            self.prepare_for_removal(node.parent)
            return True
        return False  # not case 3

    def try_case4(self, node, sibling):
        if node.parent.is_red() and sibling.are_both_children_black():
            node.parent.color = "black"
            sibling.color = "red"
            return True
        return False  # not case 4

    def try_case5(self, node, sibling):
        if self.is_not_none_and_red(sibling.left):
            if self.is_none_or_black(sibling.right):
                if node is node.parent.left:
                    sibling.color = "red"
                    sibling.left.color = "black"
                    self.rotate_right(sibling)
                    return True
        return False  # not case 5

    def try_case6(self, node, sibling):
        if self.is_none_or_black(sibling.left):
            if self.is_not_none_and_red(sibling.right):
                if node is node.parent.right:
                    sibling.color = "red"
                    sibling.right.color = "black"
                    self.rotate_left(sibling)
                    return True
        return False  # not case 6