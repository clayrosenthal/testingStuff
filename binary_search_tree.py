# Clay Rosenthal



# Binary search tree class

class BinarySearchTree:

    def __init__(self):
        self.root = None

    def insert(self, newkey):
        # inserts a new node with a given key
	#  ""  Insert new node with key, assumes data not present """
        
        if self.root is None:            # if tree is empty
            self.root = TreeNode(newkey)
            return
        else:
            p = self.root
            if p.get_key() > newkey:
                if p.get_left() is None:
                    p.set_left(TreeNode(newkey))
                    p.get_left().set_parent(p)
                else:
                    p.get_left().insert(newkey)

            else:
                if p.get_right() is None:
                    p.set_right(TreeNode(newkey))
                    p.get_right().set_parent(p)
                else:
                    p.get_right().insert(newkey)

    def find(self, key):
        # finds a node with a given key, returns true if it exists
        p = self.root      # current node
        while p is not None and p.get_key() != key :
            if key < p.get_key():
                p = p.get_left()
            else:
                p = p.get_right()

        if p is None :
            return False        
        else:
            return True

    def print_tree(self):
        # print the tree in order
        self.root.inorder_print_tree()

    def print_tree_levels(self):
        # print the tree in order
        self.root.print_levels()


    def is_empty(self):
        # checks if the tree is empty
        return (self.root == None)

    def delete(self, key):
        # deletes the node containing key, assuming node exists
	#   deletes the node containing key, assuming node exists
        if self.is_empty():
            raise ValueError
        if self.root.get_key() is key:
            temp = TreeNode(0)
            temp.set_left(self.root)
            toReturn = self.delete_helper(key, self.root, temp)
            self.root = temp.get_left()
            return toReturn
        else:
            return self.delete_helper(key, self.root, None)

    def delete_helper(self, key, child, parent):
        # helps the deletion method
        if key < child.get_key():
            if child.get_left() != None:
                return self.delete_helper(key, child.get_left(), child)
            else:
                return None
        elif key > child.get_key():
            if child.get_right() != None:
                return self.delete_helper(key, child.get_right(), child)
            else:
                return None
        else:
            temp = child.get_left() if child.get_left() != None else child.get_right()
            if (child.get_left() != None and child.get_right() != None):
                child.set_key(self.max_left(child.get_right()).get_key())
                self.delete_helper(child.get_key(), child.get_right(), child)
            elif (parent.get_left().get_key() == child.get_key()):
                parent.set_left(child.get_left() if child.get_left() != None else child.get_right())
            elif (parent.get_right().get_key() == child.get_key()):
                parent.set_right(temp)
        return key

    def max_left(self, node):
        # finds leftmost node given a node
        if node.get_left() != None:
            return self.max_left(node.get_left())
        return node

    def get_root(self):
        # gets the root of a tree
        return self.root
    
class TreeNode:
    """Tree node: left and right child + data which can be any object"""

    def __init__(self,key,data=None,left=None,right=None, parent=None):

        self.key = key
        self.data = None
        self.left = None
        self.right = None
        self.parent = None

    def set_key(self, new_key):
        # sets the node key
        self.key = new_key

    def set_data(self, new_data):
        # sets the node data
        self.data = new_data

    def set_left(self, new_left):
        # sets the node left
        self.left = new_left

    def set_right(self, new_right):
        # sets the node right
        self.right = new_right

    def set_parent(self, new_parent):
        # sets the node parent
        self.parent = new_parent

    def get_key(self):
        # gets the node key
        return self.key

    def get_data(self):
        # gets the node data
        return self.data

    def get_left(self):
        # gets the node left
        return self.left 

    def get_right(self):
        # gets the node right
        return self.right

    def get_parent(self):
        # gets the node parent
        return self.parent

    def insert(self, key):
	#  ""  Insert new node with key, assumes data not present """
        """  Insert new node with key, assumes data not present """
        if self.key != None:
            if key < self.key:
                if self.left is None:
                    self.left = TreeNode(key)
                    self.left.parent = self
                else:
                   self.left.insert(key)
            elif key > self.key:
                if self.right is None:
                    self.right = TreeNode(key)
                    self.right.parent = self
                else:
                    self.right.insert(key)
        else:
            self.key = key

    def inorder_print_tree(self):
	#  ""   Print tree content inorder        """
        """   Print tree content inorder        """

        if (self.left != None):
            self.left.inorder_print_tree()
            
        print(self.key)
        
        if (self.right != None):
            self.right.inorder_print_tree()

    def print_levels(self):
	#  ""   Print tree content inorder with the level of the tree """
        """   Print tree content inorder with the level of the tree """
        self.print_level(0)

    def print_level(self, level):
        # recursive printing of key and level
        if (self.left != None):
            self.left.print_level(level + 1)
            
        print("[ " + str(self.key) + ", " + str(level) + " ]")
        
        if (self.right != None):
            self.right.print_level(level + 1)

    def find_min(self):
        # finds smallest node in the tree
        if self.left != None:
            return self.left.find_min()
        return self

    def find_max(self):
        # finds largest node in the tree
        if self.right != None:
            return self.right.find_max()
        return self

    def find_successor(self):
        # returns the inorder successor to the node
        searcher = self
        while searcher.get_parent() != None:
            searcher = searcher.get_parent()
        successor = searcher
        while searcher.has_children():
            if (successor.get_key() < searcher.get_key() or successor.get_key() < self.key) and searcher.get_key() > self.key:
                successor = searcher
            if searcher.get_key() <=  self.key:
                if searcher.get_right() == None:
                    break
                searcher = searcher.get_right()
            else:
                if searcher.get_left() == None:
                    break
                searcher = searcher.get_left()
        return successor
            

    def has_children(self):
        # checks if a node has at leats one child
        return (self.left != None or self.right != None)


