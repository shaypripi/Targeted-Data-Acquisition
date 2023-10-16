from __future__ import annotations
from typing import Optional, Any


from typing import Any, Optional

class Node:
    """
    A class representing a node in a tree data structure.

    Attributes:
    - name (str): The name of the node.
    - code (str): The code associated with the node.
    - value (Any): The value associated with the node.
    - parent (Optional[Node]): The parent node of the current node.
    - children (set[Node]): The set of child nodes of the current node.
    """

    def __init__(self, name: str, code: str, value: Any = None, parent: Optional[Node] = None):
        """
        Initializes a new instance of the Node class.

        Args:
        - name (str): The name of the node.
        - code (str): The code associated with the node.
        - value (Any): The value associated with the node.
        - parent (Optional[Node]): The parent node of the current node.
        """
        self._name: str = name
        self._value: Any = value
        self._code: str = code
        self._parent: Optional[Node] = parent
        self._children: set[Node] = set()

    def add_child(self, child: Node) -> None:
        """
        Adds a child node to the current node.

        Args:
        - child (Node): The child node to add.
        """
        self._children.add(child)

    def get_code(self) -> str:
        """
        Gets the code associated with the current node.

        Returns:
        - str: The code associated with the current node.
        """
        return self._code
    
    def get_value(self) -> Any:
        """
        Gets the value associated with the current node.

        Returns:
        - Any: The value associated with the current node.
        """
        return self._value

    def __str__(self) -> str:
        """
        Gets the name of the current node.

        Returns:
        - str: The name of the current node.
        """
        return self._name
    
    def get_details(self) -> str:
        """
        Gets the details of the current node.

        Returns:
        - str: The details of the current node.
        """
        return self._name + " has the following properties: " + \
            str({str(child) : child.get_value() for child in self._children})
        
    
