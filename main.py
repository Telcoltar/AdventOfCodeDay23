from __future__ import annotations

import logging
from collections import deque
from logging.config import fileConfig
from typing import TextIO

fileConfig("log.ini")

logger = logging.getLogger("dev")


class Node:
    def __init__(self, value: int, next_node: Node = None):
        self.value = value
        self.next_node = next_node

    def set_next_node(self, next_node: Node):
        self.next_node = next_node

    def __str__(self):
        return f"Node with Value {self.value} and next Node {self.next_node}"


def get_input_data(filename: str) -> deque[int]:
    f: TextIO = open(filename)
    cups: deque[int] = deque(map(int, f.readline()))
    f.close()
    return cups


def cycle(current_node: Node, val_dict: dict[int, Node], max_val: int):
    current_val = current_node.value

    stored_chain: tuple[Node, Node] = (current_node.next_node, current_node.next_node.next_node.next_node)
    stored_values = [current_node.next_node.value,
                     current_node.next_node.next_node.value,
                     current_node.next_node.next_node.next_node.value]
    current_node.next_node = stored_chain[1].next_node

    next_val = current_val - 1
    if next_val < 1:
        next_val = max_val - 1
    while next_val in stored_values:
        next_val -= 1
        if next_val < 1:
            next_val = max_val - 1

    insert_node = val_dict[next_val]

    stored_chain[1].next_node = insert_node.next_node

    insert_node.next_node = stored_chain[0]

    return current_node.next_node


def cycle_part_2(cups: deque[int]):
    current_num = cups[0]
    cups.rotate(-1)
    stored_elements: list[int] = []
    for _ in range(3):
        stored_elements.append(cups.popleft())
    i: int = 1
    while i in stored_elements:
        i += 1
    min_label: int = i

    i: int = 1000000
    while i in stored_elements:
        i -= 1
    max_label: int = i

    current_num -= 1
    while current_num not in cups and current_num >= min_label:
        current_num -= 1

    if current_num < min_label:
        current_num = max_label

    dest_index = cups.index(current_num)

    for el in stored_elements[::-1]:
        cups.insert(dest_index + 1, el)


def setup(filename: str, total: int) -> tuple[dict[int, Node], Node]:
    cups: deque[int] = get_input_data(filename)
    value_dict: dict[int, Node] = {}
    head: Node = Node(cups[0])
    value_dict[cups[0]] = head
    previous_node = head
    for i in range(1, len(cups)):
        next_node = Node(cups[i])
        previous_node.set_next_node(next_node)
        value_dict[cups[i]] = next_node
        previous_node = next_node
    for i in range(10, total + 1):
        next_node = Node(i)
        previous_node.set_next_node(next_node)
        value_dict[i] = next_node
        previous_node = next_node
    previous_node.next_node = head
    return value_dict, head


def solution_part_1(filename: str, num_of_cycles: int) -> str:
    value_dict, head = setup(filename, 9)
    current_node: Node = head
    for i in range(num_of_cycles):
        current_node = cycle(current_node, value_dict, 10)
    labels: str = ""
    current_node = value_dict[1].next_node
    for i in range(len(value_dict) - 1):
        labels += str(current_node.value)
        current_node = current_node.next_node
    return labels


def solution_part_2(filename: str, num_of_cycles: int):
    value_dict, head = setup(filename, 1000000)
    current_node: Node = head
    for i in range(num_of_cycles):
        current_node = cycle(current_node, value_dict, 1000001)
    return value_dict[1].next_node.value * value_dict[1].next_node.next_node.value


if __name__ == '__main__':
    logger.info(solution_part_1("inputData.txt", 100))
    logger.info(solution_part_2("inputData.txt", 10000000))
