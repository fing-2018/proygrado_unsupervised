# -*- coding: utf-8 -*-
import nltk

from nltk.corpus import wordnet as wn
from word_embeddings import WordEmbeddings

class Node:
    def __init__(self, ID=-1, FORM=None, LEMMA=None, TAG=None, SHORT_TAG=None, MSD=None, NEC=None, SENSE=None, SYNTAX=None, DEPHEAD=-1, DEPREL=None, COREF=None, SRL=None):
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

    def lemma(self):
        return self._lemma

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

    def add_child(self, node):
        self._children.append((node.deprel(), node))

    # def display(self, depth):
    #     print(''.rjust(depth*2),end='')

    #     print ('{0}'.format(self.form()),end='')

    #     children = self.children()
    #     if (len(children) > 0) :

    #         for child in children:
    #             print(' [{0}'.format(child[0]));
    #             child[1].display(depth+1)

    #         print(''.rjust(depth*2),end='');
    #         print(']',end='');

    #     print('');

class Event(object):
    def __init__(self,verb=None,subj=None,obj=None):
        self.verb = verb
        self.subj = subj
        self.obj  = obj
        self.type = -1

    def __repr__(self):
        return '{}: {} {} {} {}'.format(self.__class__.__name__, self.verb.form(), self.subj.form(), self.obj.form(), self.type)

    def __cmp__(self, other):
        return self.type.__cmp__(other.type)


def nounify(verb_word):
    set_of_related_nouns = set()
    # for lemma in wn.lemmas(wn.morphy(verb_word, wn.VERB), pos="v"):
    for lemma in wn.lemmas(verb_word, pos="v", lang="spa"):
        print("LEMMA: "+str(lemma))
        for related_form in lemma.derivationally_related_forms():
            print("RELATED FORM: "+related_form)
            for synset in wn.synsets(related_form.name(), pos=wn.NOUN):
                print("SYNSET: "+synset)
                if wn.synset('person.n.01') in synset.closure(lambda s:s.hypernyms()):
                    set_of_related_nouns.add(synset)
    return set_of_related_nouns

def es_similar_we(arg_1,arg_2):
    res = we.similar_words(arg_1.form(), arg_2.form())
    if arg_1.tag()[0] == arg_2.tag()[0] == 'v':
        res *= 0.2
    return  res
def es_similar_lch(arg_1,arg_2,ALL=True,VERB_PENAL=0.1):
    if len(wn.synsets(arg_1.lemma(),pos=arg_1.tag()[0],lang='spa')) > 0 and len(wn.synsets(arg_2.lemma(),pos=arg_2.tag()[0],lang='spa')) > 0 and arg_1.tag()[0] == arg_2.tag()[0]:
    # if len(wn.synsets(arg_1.lemma(),pos=arg_1.tag()[0],lang='spa')) > 0 and len(wn.synsets(arg_2.lemma(),pos=arg_2.tag()[0],lang='spa')) > 0 and arg_1.tag()[0] == arg_2.tag()[0] == 'n':
        a1 = wn.synsets(arg_1.lemma(),pos=arg_1.tag()[0],lang='spa')[0]
        a2 = wn.synsets(arg_2.lemma(),pos=arg_2.tag()[0],lang='spa')[0]

        if ALL:
            # res = 100
            res = -100
            for a1 in wn.synsets(arg_1.lemma(),pos=arg_1.tag()[0],lang='spa'):
                for a2 in wn.synsets(arg_2.lemma(),pos=arg_2.tag()[0],lang='spa'):
                    # print(a1)
                    # print(a2)
                    # print("res: "+str(a1.lch_similarity(a2)))
                    # if a1.lch_similarity(a2) < res:
                    if arg_1.tag()[0] == 'v':
                        if a1.lch_similarity(a2)*VERB_PENAL > res:
                            res = a1.lch_similarity(a2)*VERB_PENAL
                    else:
                        if a1.lch_similarity(a2) > res:
                            res = a1.lch_similarity(a2)
            return res
        else:
            if arg_1.tag()[0] == 'v':
                return a1.lch_similarity(a2)*VERB_PENAL
            else:
                return a1.lch_similarity(a2)
    else:
        return 0


def dist_combinacion(argumentos_1,argumentos_2,WE=True):
    res = 0
    for i in range(3):
        if argumentos_1[i] is not None and argumentos_2[i] is not None:
            if WE:
                res += es_similar_we(argumentos_1[i],argumentos_2[i])
            else:
                res += es_similar_lch(argumentos_1[i],argumentos_2[i])
    # print(argumentos_1," ",argumentos_2,": ",res)
    if res == 0:
        return res
    else:
        if WE:
            return res
        else:
            # return 1/res
            return res

# Combinaciones posibles y me quedo con la mayor
def dist(evento_1,evento_2):
    res = -1

    # sanity rename
    v1 = evento_1.verb
    s1 = evento_1.subj
    o1 = evento_1.obj
    v2 = evento_2.verb
    s2 = evento_2.subj
    o2 = evento_2.obj

    # v1,v2,s1,s2,o1,o2
    res = max(res, dist_combinacion([v1,s1,o1],[v2,s2,o2]))
    # v1,v2,s1,o2,o1,s2
    res = max(res, dist_combinacion([v1,s1,o1],[v2,o2,s2]))
    # v1,s2,s1,v2,o1,o2
    res = max(res, dist_combinacion([v1,s1,o1],[s2,v2,o2]))
    # v1,o2,s1,v2,o1,s2
    res = max(res, dist_combinacion([v1,s1,o1],[o2,v2,s2]))
    # v1,s2,s1,o2,o1,v2
    res = max(res, dist_combinacion([v1,s1,o1],[s2,o2,v2]))
    # v1,o2,s1,s2,o1,v2
    res = max(res, dist_combinacion([v1,s1,o1],[o2,s2,v2]))

    return res

# 


we = WordEmbeddings()

e1 = Event(Node(ID='1',DEPHEAD='1',FORM='causó',LEMMA='causar',TAG='verb'),Node(ID='1',DEPHEAD='1',FORM='lluvia',LEMMA='lluvia',TAG='noun'),Node(ID='1',DEPHEAD='1',FORM='destrozos',LEMMA='destrozo',TAG='noun'))
e2 = Event(Node(ID='1',DEPHEAD='1',FORM='provocó',LEMMA='provocar',TAG='verb'),Node(ID='1',DEPHEAD='1',FORM='guerra',LEMMA='guerra',TAG='noun'),Node(ID='1',DEPHEAD='1',FORM='muerte',LEMMA='muerte',TAG='noun'))
e3 = Event(Node(ID='1',DEPHEAD='1',FORM='produjo',LEMMA='producir',TAG='verb'),Node(ID='1',DEPHEAD='1',FORM='nieve',LEMMA='nieve',TAG='noun'),Node(ID='1',DEPHEAD='1',FORM='felicidad',LEMMA='felicidad',TAG='noun'))


# print("e1-e2: "+str(dist(e1,e2)))
# print("e1-e3: "+str(dist(e1,e3)))
# print("e2-e3: "+str(dist(e2,e3)))

# print(nounify('llover'))
