from abc import ABC, abstractmethod

class Node(ABC):
    """Base class for all nodes in the abstract syntax tree (AST) of a regex pattern."""

    @abstractmethod
    def matches(self, string: str) -> bool:
        """Returns a boolean if the node matches the given string."""
        raise NotImplementedError("Node is an abstract class and cannot be instantiated.")

class Literal(Node):
    """A literal character in a regex pattern."""
    def __init__(self, char):
        self.char = char

    def matches(self, string: str) -> bool:
        return string and len(string) > 0 and string[0] == self.char

    def __repr__(self):
        return f"Literal({self.char!r})"
    
class CharacterClass(Node):
    """A character class in a regex pattern."""
    def __init__(self, chars):
        self.chars = chars

    def matches(self, string: str) -> bool:
        return string and len(string) > 0 and string[0] in self.chars

    def __repr__(self):
        return f"CharacterClass({self.chars!r})"

class Concat(Node):
    """A concatenation of two nodes in a regex pattern."""
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def matches(self, string: str) -> bool:
        # starting with the left node, check if the string matches the left node
        # if it does, then check if the string matches the right node
        # if it does, then return True
        for split in range(len(string) + 1):
            if self.left.matches(string[:split]) and self.right.matches(string[split:]): return True
        return False

    def __repr__(self):
        return f"Concat({self.left!r}, {self.right!r})"
    
class Repetition(Node):
    """A repitition of a node in a regex pattern."""
    def __init__(self, child: Node):
        self.child = child

    def matches(self, string: str, position: int = 0) -> bool:
        # Match zero occurrences
        if self.child.matches(string, position):
            return True
        
        # Match one or more occurrences
        i = position
        while i < len(string):
            if not self.child.matches(string, i):
                break
            i += 1
        
        # If we matched something and the rest of the string also matches, return True
        return i > position and (i == len(string) or self.matches(string, i))

class EOF(Node):
    """Represents the end of a pattern."""
    def matches(self, string: str, position: int = 0) -> bool:
        return position == len(string)

def parse_regex(pattern):
    """Parses a regex pattern string and constructs an AST."""
    if not pattern: raise ValueError("Pattern cannot be empty.")

    # convert the pattern string into a list of tokens
    tokens = [Literal(char) for char in pattern]

    # reduce the list of tokens into a single AST
    # use left associative concatentation to reduce the list of tokens
    ast = tokens[0]
    for token in tokens[1:]:
        ast = Concat(ast, token)
    return ast

def match(ast, string: str, position: int = 0):
    """Matches a string against the AST of a regex pattern."""

    if isinstance(ast, EOF): return position == len(string) # base case, we've reached the end of the string
    if isinstance(ast, Literal):
        if position >= len(string): return False # If the position is out of bounds, return False
        return ast.char == string[position] and match(EOF(), string, position + 1) # Check if the current character matches and proceed to the next character
    elif isinstance(ast, CharacterClass):
        if position >= len(string): return False # If the position is out of bounds, return False
        return string[position] in ast.chars and match(EOF(), string, position + 1) # Check if the current character is in the character class and proceed
    elif isinstance(ast, Concat): # Try every possible split of the string
        for split in range(position, len(string) + 1):
            if match(ast.left, string, position) and match(ast.right, string, split): return True # If the left node matches the first part of the string and the right node matches the second part of the string, return True
        return False
    elif isinstance(ast, Repetition):
        # Match zero occurrences or more by trying to match the repeated node and the rest of the string
        if match(ast.child, string, position): return True  # Match one occurrence of the child
        # Try to match the rest of the string after skipping the current character
        if position < len(string) and match(ast, string, position + 1): return True
        return match(EOF(), string, position) # Match zero occurrences by moving to the next node

    # TODO add more cases for other types of nodes
    else:
        raise ValueError(f"Unknown node type: {type(ast)}")