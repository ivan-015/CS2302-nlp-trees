# CS2302-nlp-trees
This program uses self-balancing binary search trees to perform operations with words and their embeddings.

## Important note
* Because GitHub does not allow files larger than 25MB, the glove.6B.50d.txt file had to be significantly reduced in order to be uploaded. However, you can click [here](https://nlp.stanford.edu/data/glove.6B.zip) to download the full glove file and test the program.

## Contents
* "nlp_tree.py" - this is the main file of the program, where most of the relevant functions to the user are performed. It allows the user to populate an AVL or a Red Black tree with words and their embeddings from a file and perform various operations, described below.
* "AVL_Tree.py" - this file represents an AVL Tree, inside it there is an AVLNode and an AVLTree class, both with operations to allow it to self-balance, insert, and remove items from the tree.
* "RB_Tree.py" - this file represents a Red Black Tree, inside it there is an RBTNode and an RBTree class, which similarly to AVL_Tree.py contains functions to allow the tree to self-balance and perform important operations.
* "glove.6B.50d.txt" - this is a reduced txt file that allows the program to create the trees and perform the operations.
* "word_list.txt" - this file is used to compute the cosine similarities between two words.

## Tree Operations
(a) Compute the number of nodes in the tree.

(b) Compute the height of the tree.

(c) Generate a file containing all the words stored in the tree, in ascending order, one per
line.

(d) Given a desired depth, generate a file with all the keys that have that depth, in
ascending order.

(e) Read file containing pairs of words and display their similarities.
