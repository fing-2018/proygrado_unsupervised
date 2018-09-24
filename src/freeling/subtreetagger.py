from node import Node

def subtreetagger(tag, node, pendings):
    children = node.children()
    if len(children) > 0:
        for child in children:
            node_child = child[1]
            if node.tag()[0] != 'V' and node_child.tag()[0] == 'V':
                pendings.append(node_child) 
            else:
                subtreetagger(tag, node_child, pendings)
                node.add_subtree_tag(tag)
    else:
        node.add_subtree_tag(tag)

def tagtree(node):
    pendings = [node]
    tag = 0
    while len(pendings) > 0:
        subnode = pendings.pop()
        subtreetagger(tag, subnode, pendings)
        tag += 1
