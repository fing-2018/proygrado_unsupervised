# -*- coding: utf-8 -*-
import nltk

from nltk.corpus import wordnet as wn
from word_embeddings import WordEmbeddings
from node import Node
from evento import Event
import time

def es_similar_we(arg_1,arg_2, we):
    res = we.similarity(arg_1[0], arg_2[0])
    if arg_1[1] == arg_2[1] == 'v':
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

def dist_combinacion(argumentos_1,argumentos_2, w, WE=True):
    #tic = time.time()
    res = 0
    for i in range(3):
        if argumentos_1[i][0] is not None and argumentos_2[i][0] is not None:
            if WE:
                res += es_similar_we(argumentos_1[i],argumentos_2[i], w)
            else:
                res += es_similar_lch(argumentos_1[i],argumentos_2[i])
    #print("dist_combinacion: " + str(time.time() - tic))
    return res

# # Combinaciones posibles y me quedo con la mayor
# def dist(evento_1,evento_2, we):
#     a = we.similarity(evento_1.full,evento_2.full)
#     # print("dist: " + str(a))    
#     # print("full1: " + str(evento_1.full))
#     # print("full2: " + str(evento_2.full))
#     return a

# Combinaciones posibles y me quedo con la mayor
def dist(evento_1,evento_2, we):
    #tic = time.time()
    res = -1

    #w.similarity(evento_1.full,evento_2.full)
    # sanity rename
    v1 = (evento_1.verb_full, 'v')
    s1 = (evento_1.subj_full, 'n')
    o1 = (evento_1.obj_full, 'n')
    v2 = (evento_2.verb_full, 'v')
    s2 = (evento_2.subj_full, 'n')
    o2 = (evento_2.obj_full, 'n')

    # v1,v2,s1,s2,o1,o2
    res = max(res, dist_combinacion([v1,s1,o1],[v2,s2,o2], we))
    # v1,v2,s1,o2,o1,s2
    res = max(res, dist_combinacion([v1,s1,o1],[v2,o2,s2], we))
    # v1,s2,s1,v2,o1,o2
    res = max(res, dist_combinacion([v1,s1,o1],[s2,v2,o2], we))
    # v1,o2,s1,v2,o1,s2
    res = max(res, dist_combinacion([v1,s1,o1],[o2,v2,s2], we))
    # v1,s2,s1,o2,o1,v2
    res = max(res, dist_combinacion([v1,s1,o1],[s2,o2,v2], we))
    # v1,o2,s1,s2,o1,v2
    res = max(res, dist_combinacion([v1,s1,o1],[o2,s2,v2], we))

    #print("dist: " + str(time.time() - tic))
    print("dist")
    return res


def silouhette_coefficent_single_event(idx, full_event_list, dist_map):
    
    # event_tuples = [(dist(event,x,we),x.type) for x in full_event_list if event != x]
    event = full_event_list[idx]
    event_tuples = [(value, full_event_list[key].type) for key, value in dist_map[idx].items()]
    map_clusters = {}
    for event_tuple in event_tuples:
        if event_tuple[1] in map_clusters:
            map_clusters[event_tuple[1]][0] += event_tuple[0]
            map_clusters[event_tuple[1]][1] += 1
        else:
            map_clusters[event_tuple[1]] = [event_tuple[0],1]
    list_avg_dist = [(1/(value[0]/value[1]),key) for key,value in map_clusters.items()]
    
    #a = calcular media con su propio cluster
    a = next((x for x in list_avg_dist if x[1] == event.type),None)[0]
    #b = calcular media con cluster mas cercano
    chuare = [avg for avg in list_avg_dist if avg[1] != event.type]
    if len(chuare) == 0:
        b = 0
    else:
        b = min(chuare,key=lambda x : x[0])[0]

    return (b-a)/max(a,b)

def silouhette_coefficent(full_event_list, dist_map):
    a = [silouhette_coefficent_single_event(idx,full_event_list, dist_map) for idx in range(len(full_event_list))]
    return sum(a)/len(a)



e1 = Event(Node(ID='1',DEPHEAD='1',FORM='causó',LEMMA='causar',TAG='verb'),Node(ID='1',DEPHEAD='1',FORM='lluvia',LEMMA='lluvia',TAG='noun'),Node(ID='1',DEPHEAD='1',FORM='destrozos',LEMMA='destrozo',TAG='noun'))
e2 = Event(Node(ID='1',DEPHEAD='1',FORM='provocó',LEMMA='provocar',TAG='verb'),Node(ID='1',DEPHEAD='1',FORM='guerra',LEMMA='guerra',TAG='noun'),Node(ID='1',DEPHEAD='1',FORM='muerte',LEMMA='muerte',TAG='noun'))
e3 = Event(Node(ID='1',DEPHEAD='1',FORM='produjo',LEMMA='producir',TAG='verb'),Node(ID='1',DEPHEAD='1',FORM='nieve',LEMMA='nieve',TAG='noun'),Node(ID='1',DEPHEAD='1',FORM='felicidad',LEMMA='felicidad',TAG='noun'))
