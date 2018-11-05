# Ivan Vigliante
# CS2302 TR 10:20am-11:50am
# Lab 3A
# Professor Aguirre, Diego
# TA Saha, Manoj
# Date of last modification: 10/24/2018
# The purpose of this program is to read from a file containing words and
# their word embeddings, store them in a binary search tree, and do various
# functions using the tree.

from AVL_Tree import AVLTree
from AVL_Tree import AVLNode
from RB_Tree import RBTree
import sys
import math

# Function that creates a file with all the words with a certain
# depth from a tree
def generate_file_depth(root, depth, file):
    if root is None:
        return
    if depth == 0:
        file.write(root.item + "\n")
    else:
        generate_file_depth(root.left, depth-1, file)
        generate_file_depth(root.right, depth-1, file)

# Function that generates a file with all the keys in the tree
def generate_file_inorder(root, file):
    if root is None:
        return
    generate_file_inorder(root.left, file)
    file.write(root.item + "\n")
    generate_file_inorder(root.right, file)

# Function that counts and returns the nodes in the tree
def count_tree(root):
    if root is None:
        return 0
    count = 1
    if root.left is not None:
        count = count + count_tree(root.left)
    if root.right is not None:
        count = count + count_tree(root.right)
    return count

# Function that returns the height of the tree
def get_height(root):
    if root is None:
        return -1
    return max(get_height(root.left), get_height(root.right)) + 1

# Function that prints every word in the tree and its embedding
def print_tree_inorder(root):
    if root is None:
        return
    print_tree_inorder(root.left)
    print(root.item)
    print(root.embedding)
    print_tree_inorder(root.right)

# Function that populates an AVL tree with keys and embeddings
# from glove file
def populate_AVL(filename):
    file = open(filename, "r", encoding="utf8")
    tree = AVLTree()
    for line in file:
        current = line.split(" ")
        # For each line in the file, if the word starts with an alphabetic
        # character, insert the word and embedding in a node within the tree
        if "a" <= current[0][0].lower() <= "z":
            embedding = []
            # Populate the embedding list
            for num in current[1:]:
                embedding.append(float(num))
            node = AVLNode(current[0].strip(), embedding)
            tree.insert(node)
    return tree

# Function that populates a red black tree
def populate_RBT(filename):
    file = open(filename, "r", encoding="utf8")
    tree = RBTree()
    for line in file:
        current = line.split(" ")
        # For each line in the file, if the word starts with an alphabetic
        # character, insert the word and embedding in a node within the tree
        if "a" <= current[0][0].lower() <= "z":
            embedding = []
            for num in current[1:]:
                embedding.append(float(num))
            tree.insert(current[0].strip(), embedding)
    return tree

# Function that gives the user operation options and then performs
# the operation chosen
def tree_functionalities(tree):
    while True:
        # Give user operation options
        operation = input("\n [a]: Print the number of nodes in the tree\n"+
                          " [b]: Print the height of the tree\n"+
                          " [c]: Generate a file containing all the words in the tree\n" +
                          " [d]: Generate the file containing all the words with a certain depth in the tree\n"+
                          " [f]: Compute similarity between two words from a file\n" +
                          " [p]: Print the words and embeddings in the tree\n" +
                          " [e]: Cancel and go back\n" +
                          "Input an operation to perform: ")
        # Counts the node in the tree
        if operation == "a":
            print(count_tree(tree.root))
        # Computes the height of the tree
        elif operation == "b":
            print(get_height(tree.root))
        # Generates a file with all the words in the file
        elif operation == "c":
            file = open("words_in_tree.txt", "w", encoding="utf8")
            generate_file_inorder(tree.root, file)
            file.close()
        # Generates a file that contains all nodes with a certain depth
        elif operation == "d":
            d = input("Provide the depth of the nodes you wish to generate: ")
            file = open("words_with_depth_" + d + ".txt", "w", encoding="utf8")
            generate_file_depth(tree.root, int(d), file)
            file.close()
        elif operation == "e":
            return
        # Computes similarities of two words in a file
        elif operation == "f":
            read_words_file(tree)
        # Prints all nodes and embeddings from the tree
        elif operation == "p":
            print_tree_inorder(tree.root)
        else:
            print("Operation not recognized. Please try again.")

# Function that reads the glove file
def read_glove_file():
    glove_filename = "glove.6B.50d.txt"
    while True:
        try:
            # Ask user the operation they want to perform
            tree_pref = input("What type of tree would you like to work with?\n" +
                              " [1]: AVL Tree\n [2]: Red-Black Tree\n" +
                              "Input the number of desired command (or \"e\" to exit): ")
            # If user enters 1 use avl tree
            if tree_pref == "1":
                tree = populate_AVL(glove_filename)
                tree_functionalities(tree)
            # If user enters 2 use red black tree
            elif tree_pref == "2":
                tree = populate_RBT(glove_filename)
                tree_functionalities(tree)
            # If user enters e, exit
            elif tree_pref.lower() == "e":
                return
            else:
                print("Command not recognized. Try again.")
        # Give user option to provide filename if glove file not in default location
        except FileNotFoundError:
            print(glove_filename + " file was not found on same directory as this program.\n" +
                  "Provide path and name of file with word and embeddings(\"e\" to exit): ")
            prompt = input()
            if prompt.lower() == "e":
                sys.exit()
            else:
                glove_filename = prompt
        # This will likely execute if the embedding for a word is incorrect
        except ValueError as ee:
            print("ValueError found, likely in the embeddings for the file. Check the embedding in the file and try again.")
        except Exception as ee:
            print(ee)

# Searches a binary search tree for a words and returns its embedding if present
def get_embedding(word, root):
    # This executes if word could not be found
    if root is None:
        print("Word not found within the tree, make sure the word is in the glove file")
        return None
    # Use binary search to find word
    if word.lower().strip() == root.item.lower():
        return root.embedding
    elif word.lower().strip() < root.item.lower():
        return get_embedding(word, root.left)
    else:
        return get_embedding(word, root.right)

# Computes and prints the similarities between two words
def compute_similarity(words, tree):
    # If there are less than two words, return,
    # cannot compute similarity
    if len(words) < 2:
        print("Less than two words detected. Check the text file and try again.")
        return
    # Search for words in tree
    embedding_a = get_embedding(words[0], tree.root)
    embedding_b = get_embedding(words[1], tree.root)
    # compute cosine similarity only if both words were found
    if embedding_a is not None and embedding_b is not None:
        numerator = 0
        denominator_a = 0
        denominator_b = 0
        # both embeddings have the same length
        for i in range(len(embedding_a)):
            # Numerator is the sum of every element in embedding_a * embedding_b
            numerator = numerator + (embedding_a[i]*embedding_b[i])
            # Store both parts of the denominator to compute later
            denominator_a = denominator_a + (embedding_a[i]**2)
            denominator_b = denominator_b + (embedding_b[i]**2)
        # Compute and return similarity
        similarity = numerator / (math.sqrt(denominator_a) * math.sqrt(denominator_b))
        return similarity

# Function that reads a file with two words on each line and computes their similarities
def read_words_file(tree):
    # Default name of word list file
    words_filename = "word_list.txt"
    while True:
        try:
            # Open the file
            file = open(words_filename, "r", encoding="utf8")
            # Compute and print the similarity for each line in the file
            for line in file:
                words = line.split(" ")
                print("Similarity between", words[0], "and", words[1].strip(), ":", compute_similarity(words, tree))
            return
        # If file was not found, give user option to provide custom path to a file
        except FileNotFoundError:
            print(words_filename + " file was not found on the same directory as this program.\n" +
                  "Provide path and name of file to compute similarities(\"e\" to exit): ")
            prompt = input()
            if prompt.lower() == "e":
                return
            else:
                words_filename = prompt
        except Exception as ee:
            print(ee)

def main():
    read_glove_file()

main()