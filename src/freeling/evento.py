class Event(object):

    def __init__(self, verb=None, subj=None, obj=None, parent_verb=None):
        self._verb = verb
        self._subj = subj
        self._obj  = obj
        self._complement = None
        self._circumstance_complements = []
        self._parent_verb = parent_verb
        self._type = -1
        self._label = "NONE"

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
    def label(self):
        return self._label

    @label.setter
    def label(self, label):
        self._label = label

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

    def __repr__(self):
        return '{}: {} {} {} {} {}'.format(self.__class__.__name__, self.verb.form, self.subj.form, self.obj.form, self.type, self.label)
