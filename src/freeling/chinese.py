# -*- coding: utf-8 -*-
import nltk

from nltk.corpus import wordnet as wn
from word_embeddings import WordEmbeddings
from node import Node
from evento import Event


def es_similar_we(arg_1,arg_2):
    res = WordEmbeddings().similar_words(arg_1.form(), arg_2.form())
    if arg_1.tag[0] == arg_2.tag[0] == 'v':
        res *= 0.2
    return  res

def es_similar_lch(arg_1,arg_2,ALL=True,VERB_PENAL=0.1):
    if len(wn.synsets(arg_1.lemma,pos=arg_1.tag[0],lang='spa')) > 0 and len(wn.synsets(arg_2.lemma,pos=arg_2.tag[0],lang='spa')) > 0 and arg_1.tag[0] == arg_2.tag[0]:
    # if len(wn.synsets(arg_1.lemma,pos=arg_1.tag[0],lang='spa')) > 0 and len(wn.synsets(arg_2.lemma,pos=arg_2.tag[0],lang='spa')) > 0 and arg_1.tag[0] == arg_2.tag[0] == 'n':
        a1 = wn.synsets(arg_1.lemma,pos=arg_1.tag[0],lang='spa')[0]
        a2 = wn.synsets(arg_2.lemma,pos=arg_2.tag[0],lang='spa')[0]

        if ALL:
            res = -100
            for a1 in wn.synsets(arg_1.lemma,pos=arg_1.tag[0],lang='spa'):
                for a2 in wn.synsets(arg_2.lemma,pos=arg_2.tag[0],lang='spa'):
                    if arg_1.tag[0] == 'v':
                        if a1.lch_similarity(a2)*VERB_PENAL > res:
                            res = a1.lch_similarity(a2)*VERB_PENAL
                    else:
                        if a1.lch_similarity(a2) > res:
                            res = a1.lch_similarity(a2)
            return res
        else:
            if arg_1.tag[0] == 'v':
                return a1.lch_similarity(a2)*VERB_PENAL
            else:
                return a1.lch_similarity(a2)
    else:
        return 0

def dist_combinacion(argumentos_1,argumentos_2,WE=False):
    res = 0
    for i in range(3):
        if argumentos_1[i] is not None and argumentos_2[i] is not None:
            if WE:
                res += es_similar_we(argumentos_1[i],argumentos_2[i])
            else:
                res += es_similar_lch(argumentos_1[i],argumentos_2[i])
    if res == 0:
        return res
    else:
        if WE:
            return res
        else:
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



e1 = Event(Node(ID='1',DEPHEAD='1',FORM='causó',LEMMA='causar',TAG='verb'),Node(ID='1',DEPHEAD='1',FORM='lluvia',LEMMA='lluvia',TAG='noun'),Node(ID='1',DEPHEAD='1',FORM='destrozos',LEMMA='destrozo',TAG='noun'))
e2 = Event(Node(ID='1',DEPHEAD='1',FORM='provocó',LEMMA='provocar',TAG='verb'),Node(ID='1',DEPHEAD='1',FORM='guerra',LEMMA='guerra',TAG='noun'),Node(ID='1',DEPHEAD='1',FORM='muerte',LEMMA='muerte',TAG='noun'))
e3 = Event(Node(ID='1',DEPHEAD='1',FORM='produjo',LEMMA='producir',TAG='verb'),Node(ID='1',DEPHEAD='1',FORM='nieve',LEMMA='nieve',TAG='noun'),Node(ID='1',DEPHEAD='1',FORM='felicidad',LEMMA='felicidad',TAG='noun'))
