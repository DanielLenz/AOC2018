from typing import NamedTuple, List


TESTINPUT  = """2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"""

class Node(NamedTuple):

    n_children: int
    n_meta: int 
    children: List['Node']
    metadata: List[int]

def parse_nodes(inputs: List[int], start: int=0) -> Node:
    n_children = inputs[start]
    n_meta = inputs[start+1]
    start += 2
    children = []

    for _ in range(n_children):
        child, start = parse_nodes(inputs, start)
        children.append(child)

    metadata = inputs[start:start+n_meta]

    node = Node(n_children, n_meta, children, metadata)

    return node, (start+n_meta)

def sum_all_metadata(node: Node) -> int:
    return sum(node.metadata) + sum(sum_all_metadata(child) for child in node.children)


def sum_all_metadata2(node: Node) -> int:
    if not node.children:
        return sum(node.metadata)
    else:
        total = 0
        for idx in node.metadata:
            
            if (idx > 0) and (idx <= node.n_children):
                total += sum_all_metadata2(node.children[idx - 1])
        
        return total


if __name__ == "__main__":
    testlist = [int(ch) for ch in TESTINPUT.split(' ')]
    head, _ = parse_nodes(testlist)
    assert sum_all_metadata(head) == 138 

    with open('input.txt') as f:
        input_str = f.read().strip()
        inputs = [int(ch) for ch in input_str.split(' ')]

    root, _ = parse_nodes(inputs)
    print(sum_all_metadata2(root))
