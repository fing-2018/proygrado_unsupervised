class Node:
    def __init__(self, ID, FORM=None, LEMMA=None, TAG=None, SHORT_TAG=None, MSD=None, NEC=None, SENSE=None, SYNTAX=None, DEPHEAD=None, DEPREL=None, COREF=None, SRL=None):
        self._id = int(ID)
        self._form = FORM
        self._lemma = LEMMA
        self._tag = TAG
        self._shorttag = SHORT_TAG
        self._msd = MSD
        self._nec = NEC
        self._sense = SENSE
        self._syntax = SYNTAX
        self._dephead = int(DEPHEAD)
        self._deprel = DEPREL
        self._coref = COREF
        self._srl = SRL
        self._children = []

    @property
    def id(self):
        return self._id

    @property
    def children(self):
        return self._children

    @property
    def dephead(self):
        return self._dephead

    @property
    def nec(self):
        return self._nec

    @property
    def deprel(self):
        return self._deprel

    @property
    def id(self):
        return self._id

    @property
    def form(self):
        return self._form

    @property
    def tag(self):
        return self._tag

    @property
    def lemma(self):
        return self._lemma

    def has_relation(self, relation):
        return len(list(filter(lambda x: x[0] == relation, self.children))) > 0

    def get_node_with_relation(self, relation):
        return (list(filter(lambda x: x[0] == relation, self.children))[0])[1] if self.has_relation(relation) else None

    def add_child(self, node):
        self._children.append((node.deprel, node))

    def display(self, depth):
        print(''.rjust(depth*2),end='')

        print ('{0}'.format(self.form),end='')

        children = self.children
        if (len(children) > 0) :

            for child in children:
                print(' [{0}'.format(child[0]));
                child[1].display(depth+1)

            print(''.rjust(depth*2),end='');
            print(']',end='');

        print('');

    def __repr__(self):
        return self.form



    
