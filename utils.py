from __future__ import annotations
from typing import Optional, Any


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
        self._name: str = name
        self._value: Any = value
        self._code: str = code
        self._parent: Optional[Node] = parent
        self._children: set[Node] = set()

    def add_child(self, child: Node) -> None:
        self._children.add(child)

    def get_code(self) -> str:
        return self._code
    
    def get_value(self) -> Any:
        return self._value

    def __str__(self) -> str:
        return self._name
    
    def get_details(self) -> str:
        return self._name + " has the following properties: " + \
            str({str(child) : child.get_value() for child in self._children})
        
    
