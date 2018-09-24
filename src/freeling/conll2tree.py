#1  La        el        DA0FS0  - - - -          - 2 spec     - -
from node import Node

def conll2tree(conll_text):
    conll_table = [[Node(ID=0, DEPREL='sentence', DEPHEAD=-1),[]]]#array de 0 a cant tokens, con cada elemento un array de (nodo, lista_nodos_hijos)
    for conll_line in conll_text.split('\n'):
        if conll_line.strip() != "":
            conll_split = conll_line.split()
            new_node = Node(conll_split[0], conll_split[1], conll_split[2], conll_split[3], conll_split[4], conll_split[5], 
                    conll_split[6], conll_split[7], conll_split[8], conll_split[9], conll_split[10], conll_split[11], conll_split[12])
            if len(conll_table) > new_node.id() and len(conll_table[new_node.id()][1]) > 0:
                for child_node in conll_table[new_node.id()][1]:
                    new_node.add_child(child_node) 
            rellenar_tuplas(max(new_node.dephead(), new_node.id()), conll_table)
            conll_table[new_node.dephead()][1].append(new_node)
            conll_table[new_node.id()][0] = new_node
            if new_node.dephead() < new_node.id():
                father_node = conll_table[new_node.dephead()][0]
                father_node.add_child(new_node)
    return conll_table[0][0]

def rellenar_tuplas(idx, conll_table):
    if len(conll_table) < idx + 1:
        for indice in range(idx + 1): 
            try:
                conll_table[indice]
            except IndexError:
                conll_table.append([None,[]])
