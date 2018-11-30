# -*- coding: utf-8 -*-

from random import shuffle
from chinese import dist, silouhette_coefficent
from node import Node
from evento import Event
from etiquetadoeventos import Etiquetado_eventos
from word_embeddings import WordEmbeddings
from functools import reduce
from collections import Counter
import math

we = WordEmbeddings()

#Chinese Whispers Algorithm
# def CWA(event_list):
#     for i in range(len(event_list)):
#         event_list[i].type = i
#     not_converged = True
#     iteracion = 0
#     while not_converged:
#         # for e in event_list:
#         #     print(e)
#         iteracion += 1
#         print("==ITERACION==>"+str(iteracion))
#         shuffle(event_list)
#         clases_antes = [event.type for event in event_list]
#         for i in range(len(event_list)):
#             max_similarity = -1
#             for j in range(len(event_list)):
#                 if i != j:
#                     similarity = dist(event_list[i],event_list[j], we)
#                     if similarity > max_similarity:
#                         max_similarity = similarity
#                         event_list[i].type = event_list[j].type
#         clases_despues = [event.type for event in event_list]
#         not_converged = clases_antes != clases_despues

def CWA(event_list):
    for i in range(len(event_list)):
        event_list[i][0].type = i
    not_converged = True
    iteracion = 0
    while not_converged:
        iteracion += 1
        print("==ITERACION==>"+str(iteracion))
        shuffle(event_list)
        clases_antes = [event[0].type for event in event_list]
        print(len(set(clases_antes)))
        print([(x.type,y.type) for (x,y) in event_list])
        for i in range(len(event_list)):
            event_list[i][0].type = event_list[i][1].type
        clases_despues = [event[0].type for event in event_list]
        print(len(set(clases_despues)))
        print([(x.type,y.type) for (x,y) in event_list])
        not_converged = clases_antes != clases_despues

# event_list = []


# e1  = Event(Node(ID=1,DEPHEAD=1,FORM='causó',      LEMMA='causar',    TAG='verb'),
#             Node(ID=1,DEPHEAD=1,FORM='lluvia',     LEMMA='lluvia',    TAG='noun'),
#             Node(ID=1,DEPHEAD=1,FORM='destrozos',  LEMMA='destrozo',  TAG='noun'))
# event_list.append(e1)

# e2  = Event(Node(ID=1,DEPHEAD=1,FORM='provocó',    LEMMA='provocar',  TAG='verb'),
#             Node(ID=1,DEPHEAD=1,FORM='guerra',     LEMMA='guerra',    TAG='noun'),
#             Node(ID=1,DEPHEAD=1,FORM='muerte',     LEMMA='muerte',    TAG='noun'))
# event_list.append(e2)

# e3  = Event(Node(ID=1,DEPHEAD=1,FORM='produjo',    LEMMA='producir',  TAG='verb'),
#             Node(ID=1,DEPHEAD=1,FORM='nieve',      LEMMA='nieve',     TAG='noun'),
#             Node(ID=1,DEPHEAD=1,FORM='felicidad',  LEMMA='felicidad', TAG='noun'))
# event_list.append(e3)

# e4  = Event(Node(ID=1,DEPHEAD=1,FORM='destruyó',   LEMMA='destruir',  TAG='verb'),
#             Node(ID=1,DEPHEAD=1,FORM='tormenta',   LEMMA='tormenta',  TAG='noun'),
#             Node(ID=1,DEPHEAD=1,FORM='casa',       LEMMA='casa',      TAG='noun'))
# event_list.append(e4)

# e5  = Event(Node(ID=1,DEPHEAD=1,FORM='dejó',       LEMMA='dejar',     TAG='verb'),
#             Node(ID=1,DEPHEAD=1,FORM='batalla',    LEMMA='batalla',   TAG='noun'),
#             Node(ID=1,DEPHEAD=1,FORM='heridos',    LEMMA='herido',    TAG='noun'))
# event_list.append(e5)

# e6  = Event(Node(ID=1,DEPHEAD=1,FORM='voló',       LEMMA='volar',     TAG='verb'),
#             Node(ID=1,DEPHEAD=1,FORM='viento',     LEMMA='viento',    TAG='noun'),
#             Node(ID=1,DEPHEAD=1,FORM='techos',     LEMMA='techo',     TAG='noun'))
# event_list.append(e6)

# e7  = Event(Node(ID=1,DEPHEAD=1,FORM='aumentó',    LEMMA='aumentar',  TAG='verb'),
#             Node(ID=1,DEPHEAD=1,FORM='presidente', LEMMA='presidente',TAG='noun'),
#             Node(ID=1,DEPHEAD=1,FORM='impuestos',  LEMMA='impuesto',  TAG='noun'))
# event_list.append(e7)

# e8  = Event(Node(ID=1,DEPHEAD=1,FORM='aprobó',     LEMMA='aprobar',   TAG='verb'),
#             Node(ID=1,DEPHEAD=1,FORM='gobierno',   LEMMA='gobierno',  TAG='noun'),
#             Node(ID=1,DEPHEAD=1,FORM='ley',        LEMMA='ley',       TAG='noun'))
# event_list.append(e8)

# e9  = Event(Node(ID=1,DEPHEAD=1,FORM='explotó',    LEMMA='explotar',  TAG='verb'),
#             Node(ID=1,DEPHEAD=1,FORM='bomba',      LEMMA='bomba',     TAG='noun'),
#             Node(ID=1,DEPHEAD=1,FORM='hospital',   LEMMA='hospital',  TAG='noun'))
# event_list.append(e9)

# e10 = Event(Node(ID=1,DEPHEAD=1,FORM='mató',       LEMMA='matar',     TAG='verb'),
#             Node(ID=1,DEPHEAD=1,FORM='temporal',   LEMMA='temporal',  TAG='noun'),
#             Node(ID=1,DEPHEAD=1,FORM='ganado',     LEMMA='ganado',    TAG='noun'))
# event_list.append(e10)

# e11 = Event(Node(ID=1,DEPHEAD=1,FORM='negó',       LEMMA='negar',     TAG='verb'),
#             Node(ID=1,DEPHEAD=1,FORM='ministro',   LEMMA='ministro',  TAG='noun'),
#             Node(ID=1,DEPHEAD=1,FORM='acusaciones',LEMMA='acusación', TAG='noun'))
# event_list.append(e11)

# e12 = Event(Node(ID=1,DEPHEAD=1,FORM='dejó',       LEMMA='dejar',     TAG='verb'),
#             Node(ID=1,DEPHEAD=1,FORM='inundación', LEMMA='inundación',TAG='noun'),
#             Node(ID=1,DEPHEAD=1,FORM='ahogados',   LEMMA='ahogado',   TAG='noun'))
# event_list.append(e12)


# def print_dists(event_list, ALL=False):
#     for i in range(len(event_list)):
#         res = -1
#         max_i = -1
#         for j in range(len(event_list)):
#             if i != j:
#                 if dist(event_list[i],event_list[j], we) > res:
#                     res = dist(event_list[i],event_list[j], we)
#                     max_i = j
#         print("e"+str(i)+"->e"+str(max_i)+"=>"+str(res))

#     if(ALL):
#         for i in range(len(event_list)):
#             for j in range(len(event_list)):
#                 if i != j:
#                     print("e"+str(i)+"->e"+str(j)+"=>"+str(dist(event_list[i],event_list[j], we)))
def generate_dist_map(event_list):
    res = {}
    for i in range(len(event_list)):
        for j in range(len(event_list)):
            if j > i:
                dist_ei_ej = dist(event_list[i],event_list[j], we)
                if i in res:
                    res[i][j] = dist_ei_ej
                else:
                    res[i] = {j:dist_ei_ej}
                if j in res:
                    res[j][i] = dist_ei_ej
                else:
                    res[j] = {i:dist_ei_ej}
    return res

def list_most_similar_event(event_list,map_dists):
    return [(event_list[key], event_list[max(value.items(),key=lambda x: x[1])[0]]) for key,value in map_dists.items()]


def clusterizar(event_list):
    clusters = {}
    for event in event_list:
        if event.type not in clusters:
            clusters[event.type] = [event]
        else:
            clusters[event.type].append(event)
    return clusters

def print_clusters(clusters):
    for key in clusters.keys():
        print("======CLUSTER_"+str(key)+"======")
        for value in clusters[key]:
            print(value)

def to_count_list(input_list):
  a1 = [v.true_label for v in input_list]
  return [(v,a1.count(v)) for v in set(a1)]

def entropy(clusters,event_amount):
  return sum([-sum(map(lambda x: x*math.log(x,2),map(lambda x: x[1]/float(len(value)),to_count_list(value))))*(len(value)/float(event_amount)) for key,value in clusters.items()])

def labeling_evaluation(clusters):
    return len(['_' for (x,y) in  [(value[0].label,max(to_count_list(value),key=lambda x: x[1])[0]) for key,value in clusters.items()] if x == y])/float(len(clusters.keys()))

def purity(clusters, total_event_size):
    return reduce(lambda true_value, cluster : true_value + Counter(list(map(lambda ev : ev.true_label, cluster))).most_common(1)[0][1], clusters.values(), 0)/float(total_event_size)

def cluster_and_labeling(event_list):

    for x in event_list:
        x.generate_full_nodes()
    dist_map = generate_dist_map(event_list)
    # print(dist_map)
    list_most_similar = list_most_similar_event(event_list,dist_map)

    # print(list_most_similar)

    CWA(list_most_similar)

    # print(list_most_similar)

    clusters = clusterizar(event_list)

    print_clusters(clusters)

    et_eventos=Etiquetado_eventos()

    for cluster in clusters.values():
        label=et_eventos.set_label(cluster)
        # print(cluster)
    
    print_clusters(clusters)
    print("==SILOUHETTE_COEFFICENT==>"+str(silouhette_coefficent(event_list, dist_map)))
    print("==PURITY_COEFFICENT==>"+str(purity(clusters, len(event_list))))
    print("==ENTROPY_COEFFICENT==>"+str(entropy(clusters, len(event_list))))
    print(labeling_evaluation(clusters))


# cluster_and_labeling(event_list)
