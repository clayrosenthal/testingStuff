# Clay Rosenthal



# huffman encoding and decoding

def comes_before(a, b):
    """ returns true if tree rooted at node a comes before tree rooted at node b """
    if a.freq < b.freq:
        return True
    elif b.freq < a.freq:
        return False
    else:
        return a.char > b.char


def combine(a, b):
    """ creates a new huffman node with children a and b with combined freq with name of the right child """
    new_node = HuffmanNode(b.char, a.freq+b.freq)
    new_node.set_left(b)
    new_node.set_right(a)
    return new_node


def cnt_freq(filename):
    # returns a Python list of 256 integers the frequencies of characters in file
    try:
        file = open(filename, "r")
    except:
        raise ValueError
    frequencies = [0]*256
    for line in file.readlines():
        for ch in line:
            frequencies[ord(ch)] += 1
    file.close()
    return frequencies


def create_huff_tree(char_freq): 
    # returns the root node of a Huffman Tree
    huffman_nodes = []
    for i in range(len(char_freq)):
        freq = char_freq[i]
        if freq == 0:
            pass
        else:
            huffman_nodes.append(HuffmanNode(i, freq))

    while len(huffman_nodes) is not 1:
        huffman_nodes.append(combine(find_min(huffman_nodes),find_min(huffman_nodes)))

    return huffman_nodes[0]


def create_code(node):
    # returns a Python list of 256 strings representing the code
    codes = [""]*256
    assign_code(node, "", codes)
    return codes


def assign_code(node, code, codes):
    # assigns code of each char in a tree
    if node.left is not None:
        assign_code(node.left, code + "0", codes)
    if node.right is not None:
        assign_code(node.right, code + "1", codes)
    if is_leaf(node):
        codes[node.char] = code


def tree_preord(node): 
    # writes a string representation of the Huffman tree
    if node is None:
        return ""
    if is_leaf(node):
        return "1" + chr(node.char)
    return "0"+tree_preord(node.left)+tree_preord(node.right)


def huffman_encode(in_file, out_file): 
    # encodes in_file and writes the it to out_file
    freqs = cnt_freq(in_file)
    huffman_tree = create_huff_tree(freqs)
    try:
        file_in = open(in_file, "r")
    except:
        raise ValueError
    codes = create_code(huffman_tree)
    encoded = ""
    for line in file_in.readlines():
        for ch in line:
            encoded += codes[ord(ch)]
    file_in.close()
    file_out = open(out_file, "w")
    file_out.writelines(encoded)
    file_out.close()
    return encoded

    
def huffman_decode(freqs, encoded_file, decode_file):
    # decodes encoded file, writes it to decode
    huffman_tree = create_huff_tree(freqs)
    codes = create_code(huffman_tree)
    decoded = ""
    try:
        file_in = open(encoded_file, "r")
    except:
        raise ValueError
    for line in file_in.readlines():
        decoded += decode_line(huffman_tree, line)
    file_in.close()
    file_out = open(decode_file, "w")
    file_out.writelines(decoded)
    file_out.close()
    return decoded


def decode_line(root, line):
    # decodes an individual line
    tree_iter = root
    decoded = ""
    for i in range(len(line)):
        if line[i] == "0":
            tree_iter = tree_iter.left

        else:
            tree_iter = tree_iter.right

        if is_leaf(tree_iter):
            decoded += chr(tree_iter.char)
            tree_iter = root

    return decoded


def find_min(huff_list):
    # finds and removes the smallest huffman node
    min_node = huff_list[0]
    for node in huff_list[1:]:
        if comes_before(node, min_node):
            min_node = node
    huff_list.remove(min_node)
    return min_node


def is_leaf(node):
    # returns True if node is a leaf
    return node.right is None and node.left is None


class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char  # actually the character code
        self.freq = freq
        self.code = None
        self.left = None
        self.right = None

    def set_code (self, code):
        # sets the code of a huffman node
        self.code = code

    def set_left (self, node):
        # sets the left of a huffman node
        self.left = node

    def set_right (self, node):
        # sets the right of a huffman node
        self.right = node
