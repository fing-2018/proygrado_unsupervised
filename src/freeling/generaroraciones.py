#1  La        el        DA0FS0  - - - -          - 2 spec     - -
from node import Node

class Tupla(object):
   def __init__(self,suj,obj,padre):
       self.suj = suj
       self.obj = obj
       self.padre = padre

   def __repr__(self):
       return '{}: {} {} {}'.format(self.__class__.__name__, self.suj, self.obj, self.padre)

   def __cmp__(self, other):
       return self.type.__cmp__(other.type)

def pepe123(table,node,padre):
    if node.tag()[0] == 'V':
        if padre is not None and set.intersection(node.subtree_tags(), padre.subtree_tags()) != set():
            table[node.id()] = [None, None, None, node.dephead()]
        else:
            table[node.id()] = [None, None, None, 0]
    for child in node.children():
        node_child = child[1]
        relation_child = child[0]
        if node.tag()[0] == 'V':
            if relation_child == 'suj':
                table[node.id()][0] = node_child
                idx_padre = table[node.id()][3]
                if idx_padre != 0:
                    if table[idx_padre][0] == None:
                        table[idx_padre][0] = node_child
            elif relation_child == 'cd':
                table[node.id()][1] = node_child
                idx_padre = table[node.id()][3]
                if idx_padre != 0:
                    if table[idx_padre][1] == None:
                        table[idx_padre][1] = node_child
            elif relation_child == 'cc':
                table[node.id()][2] = node_child
                idx_padre = table[node.id()][3]
                if idx_padre != 0:
                    if table[idx_padre][2] == None:
                        table[idx_padre][2] = node_child
            # if relation_child == 'suj':
            #     idx = 0
            # elif relation_child == 'cd':
            #     idx = 1
            # elif relation_child == 'cc':
            #     idx = 2
            # table[node.id()][idx] = node_child
            # idx_padre = table[node.id()][3]
            # if idx_padre != 0:
            #     if table[idx_padre][idx] == None:
            #         table[idx_padre][idx] = node_child
        pepe123(table,node_child, node) 


def getFromAncestor(table,idx,l):
    res = table[l[3]][idx]
    res_p = table[l[3]][3]
    while res is None and res_p != 0:
        res = table[res_p][idx]
        res_p = table[res_p][3]
    l[idx] = res


def main(node):
    table = {}
    pepe123(table,node,None)
    print(table)
    for k,v in table.items():
        if v[3] != 0:
            for idx in range(3):
                if v[idx] is None:
                    getFromAncestor(table,idx,v)
    for k,v in table.items():
        print("Clave: "+str(k))
        if v[0] is not None:
            print(" Suj: "+v[0].form())
        if v[1] is not None:
            print(" Cd: "+v[1].form())
        if v[2] is not None:
            print(" Cc: "+v[2].form())
        print(" Padre: "+str(v[3]))