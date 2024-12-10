"""
Linked list implementations.
"""

from typing import Any


class SinglyLinkedListNode[T]:
    """
    Singly linked list node of type T.
    """

    _item: T
    _next: Any

    def __init__(self, item: T):
        """
        Initialize this SinglyLinkedListNode.
        """
        self._item = item
        self._next = None

    def __iter__(self):
        """
        Iterate over the items of this linked list.

        Yields items of type T.
        """
        curr_node = self
        while curr_node is not None:
            yield curr_node.get_item()
            curr_node = curr_node.get_next()

    def get_item(self) -> T:
        """
        Get this node's item.
        """
        return self._item

    def set_item(self, item: T):
        """
        Set this node's item.
        """
        self._item = item

    def get_next(self) -> Any:
        """
        Get the next node.
        """
        return self._next

    def set_next(self, node: Any):
        """
        Set the next node.
        """
        self._next = node


def add_to_end[T](item: T, node: SinglyLinkedListNode[T]) -> SinglyLinkedListNode[T]:
    """
    Add item to the end of the linked list.
    """
    new_node = SinglyLinkedListNode(item)
    prev_node = node
    curr_node = node.get_next()

    while curr_node is not None:
        prev_node = curr_node
        curr_node = curr_node.get_next()

    prev_node.set_next(new_node)
    return new_node
