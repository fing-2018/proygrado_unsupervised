class Event(object):

    def __init__(self, verb=None, subj=None, obj=None, parent_verb=None):
        self._verb = verb
        self._subj = subj
        self._obj  = obj
        self._complement = None
        self._label = 'NONE'
        self._circumstance_complements = []
        self._parent_verb = parent_verb
        self._type = -1
        self._verb_full = ''
        self._subj_full = ''
        self._obj_full = ''
        self._full = ''
        self._true_label = None

    @property
    def verb(self):
        return self._verb

    @property
    def subj(self):
        return self._subj
    
    @subj.setter
    def subj(self, subj):
        self._subj = subj

    @property
    def obj(self):
        return self._obj

    @obj.setter
    def obj(self, obj):
        self._obj = obj

    @property
    def parent_verb(self):
        return self._parent_verb

    @parent_verb.setter
    def parent_verb(self, parent_verb):
        self._parent_verb = parent_verb

    @property
    def circumstance_complements(self):
        return self._circumstance_complements
    
    def add_circumstance_complements(self, node):
        self._circumstance_complements.append(node)

    @property
    def complement(self):
        return self._complement
    
    @complement.setter
    def complement(self, node):
        self._complement = node

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, label):
        self._label = label

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        self._type = type

    @property
    def subj_full(self):
        return self._subj_full

    @property
    def verb_full(self):
        return self._verb_full

    @property
    def obj_full(self):
        return self._obj_full

    @property
    def full(self):
        return self._full

    @property
    def true_label(self):
        return self._true_label
    
    @true_label.setter
    def true_label(self, true_label):
        self._true_label = true_label

    def generate_full_nodes(self):
        self._subj_full = self.get_full_node(self.subj) if self.subj is not None else ''
        self._verb_full = self.get_full_node(self.verb, is_verb=True) if self.verb is not None else ''
        self._obj_full = self.get_full_node(self.obj) if self.obj is not None else ''
        self._full = (self._subj_full + ' ' + self._verb_full + ' ' + self._obj_full).replace('_', ' ')

    def recursive_full_node(self, list_nodes, node):
        list_nodes.append(node)
        for tuple in node.children:
            if not ((tuple[0] == 'S' and node.tag[0] == 'V' and tuple[1].tag[0] == 'V')
                or tuple[0] == 'f' 
                #or tuple[0] == 'coord'
                ):
                self.recursive_full_node(list_nodes, tuple[1])


    def get_full_node(self, node, is_verb=False, text=True):
        if node is None and text:
            return ''
        elif node is None:
            return []
        if is_verb:
            list_nodes = [node]
            for node_child in node.children:
                if node_child[0] in ['v','s','c','infinitiu']:
                    list_nodes.append(node_child[1])
                elif node_child[1].tag[0] == 'R':
                    list_nodes.append(node_child[1])
        else:
            list_nodes = []
            self.recursive_full_node(list_nodes, node)
        list_nodes = sorted(list_nodes, key=lambda node: node.id)
        if text: 
            list_nodes = ' '.join(list(map(lambda x: x.form, list_nodes)))
        return list_nodes

    def bag_of_words(self):
        bow_list = list()
        if self.subj is not None:
            bow_list += self.get_full_node(self.subj).split()
        if self.verb is not None:
            bow_list += self.get_full_node(self.verb, is_verb=True).split() 
        if self.obj is not None:
            bow_list += self.get_full_node(self.obj).split() 
        return set(bow_list)
        
    #def __repr__(self):
    #    if self._full is None:
    #        return '{} {} {}|TRUE:{}, ETIQUETADO:{}'.format(self.get_full_node(self.subj) if self.subj is not None else '', self.get_full_node(self.verb, is_verb=True) if self.verb is not None else '', self.get_full_node(self.obj) if self.obj is not None else '', self._true_label, self._label)
    #    return self._full

    def __repr__(self):
        return '{} {} {}|TRUE:{}, ETIQUETADO:{}'.format(self.get_full_node(self.subj) if self.subj is not None else '', self.get_full_node(self.verb, is_verb=True) if self.verb is not None else '', self.get_full_node(self.obj) if self.obj is not None else '', self._true_label, self._label)
