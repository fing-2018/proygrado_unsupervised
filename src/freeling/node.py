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
        self._subtreetags = set()

    def children(self):
        return self._children

    def dephead(self):
        return self._dephead

    def deprel(self):
        return self._deprel

    def id(self):
        return self._id

    def form(self):
        return self._form

    def tag(self):
        return self._tag

    def children(self):
        return self._children

    def subtree_tags(self):
        return self._subtreetags

    def add_child(self, node):
        self._children.append((node.deprel(), node))

    def add_subtree_tag(self, tag):
        self._subtreetags.add(tag)

    def display(self, depth):
        print(''.rjust(depth*2),end='')

        print ('{0}/{1}'.format(self.form(), self.subtree_tags()),end='')

        children = self.children()
        if (len(children) > 0) :

            for child in children:
                print(' [{0}'.format(child[0]));
                child[1].display(depth+1)

            print(''.rjust(depth*2),end='');
            print(']',end='');

        print('');

    
