# -*- coding: utf-8 -*-

from random import shuffle
from chinese import dist
from node import Node
from evento import Event
from etiquetadoeventos import Etiquetado_eventos

#Chinese Whispers Algorithm
def CWA(event_list):
    for i in range(len(event_list)):
        event_list[i].type = i
    not_converged = True
    while not_converged:
        # for e in event_list:
        #     print(e)
        shuffle(event_list)
        clases_antes = [event.type for event in event_list]
        for i in range(len(event_list)):
            max_similarity = -1
            for j in range(len(event_list)):
                if i != j:
                    similarity = dist(event_list[i],event_list[j])
                    if similarity > max_similarity:
                        max_similarity = similarity
                        event_list[i].type = event_list[j].type
        clases_despues = [event.type for event in event_list]
        not_converged = clases_antes != clases_despues


event_list = []


e1  = Event(Node(ID=1,DEPHEAD=1,FORM='causó',      LEMMA='causar',    TAG='verb'),
            Node(ID=1,DEPHEAD=1,FORM='lluvia',     LEMMA='lluvia',    TAG='noun'),
            Node(ID=1,DEPHEAD=1,FORM='destrozos',  LEMMA='destrozo',  TAG='noun'))
event_list.append(e1)

e2  = Event(Node(ID=1,DEPHEAD=1,FORM='provocó',    LEMMA='provocar',  TAG='verb'),
            Node(ID=1,DEPHEAD=1,FORM='guerra',     LEMMA='guerra',    TAG='noun'),
            Node(ID=1,DEPHEAD=1,FORM='muerte',     LEMMA='muerte',    TAG='noun'))
event_list.append(e2)

e3  = Event(Node(ID=1,DEPHEAD=1,FORM='produjo',    LEMMA='producir',  TAG='verb'),
            Node(ID=1,DEPHEAD=1,FORM='nieve',      LEMMA='nieve',     TAG='noun'),
            Node(ID=1,DEPHEAD=1,FORM='felicidad',  LEMMA='felicidad', TAG='noun'))
event_list.append(e3)

e4  = Event(Node(ID=1,DEPHEAD=1,FORM='destruyó',   LEMMA='destruir',  TAG='verb'),
            Node(ID=1,DEPHEAD=1,FORM='tormenta',   LEMMA='tormenta',  TAG='noun'),
            Node(ID=1,DEPHEAD=1,FORM='casa',       LEMMA='casa',      TAG='noun'))
event_list.append(e4)

e5  = Event(Node(ID=1,DEPHEAD=1,FORM='dejó',       LEMMA='dejar',     TAG='verb'),
            Node(ID=1,DEPHEAD=1,FORM='batalla',    LEMMA='batalla',   TAG='noun'),
            Node(ID=1,DEPHEAD=1,FORM='heridos',    LEMMA='herido',    TAG='noun'))
event_list.append(e5)

e6  = Event(Node(ID=1,DEPHEAD=1,FORM='voló',       LEMMA='volar',     TAG='verb'),
            Node(ID=1,DEPHEAD=1,FORM='viento',     LEMMA='viento',    TAG='noun'),
            Node(ID=1,DEPHEAD=1,FORM='techos',     LEMMA='techo',     TAG='noun'))
event_list.append(e6)

e7  = Event(Node(ID=1,DEPHEAD=1,FORM='aumentó',    LEMMA='aumentar',  TAG='verb'),
            Node(ID=1,DEPHEAD=1,FORM='presidente', LEMMA='presidente',TAG='noun'),
            Node(ID=1,DEPHEAD=1,FORM='impuestos',  LEMMA='impuesto',  TAG='noun'))
event_list.append(e7)

e8  = Event(Node(ID=1,DEPHEAD=1,FORM='aprobó',     LEMMA='aprobar',   TAG='verb'),
            Node(ID=1,DEPHEAD=1,FORM='gobierno',   LEMMA='gobierno',  TAG='noun'),
            Node(ID=1,DEPHEAD=1,FORM='ley',        LEMMA='ley',       TAG='noun'))
event_list.append(e8)

e9  = Event(Node(ID=1,DEPHEAD=1,FORM='explotó',    LEMMA='explotar',  TAG='verb'),
            Node(ID=1,DEPHEAD=1,FORM='bomba',      LEMMA='bomba',     TAG='noun'),
            Node(ID=1,DEPHEAD=1,FORM='hospital',   LEMMA='hospital',  TAG='noun'))
event_list.append(e9)

e10 = Event(Node(ID=1,DEPHEAD=1,FORM='mató',       LEMMA='matar',     TAG='verb'),
            Node(ID=1,DEPHEAD=1,FORM='temporal',   LEMMA='temporal',  TAG='noun'),
            Node(ID=1,DEPHEAD=1,FORM='ganado',     LEMMA='ganado',    TAG='noun'))
event_list.append(e10)

e11 = Event(Node(ID=1,DEPHEAD=1,FORM='negó',       LEMMA='negar',     TAG='verb'),
            Node(ID=1,DEPHEAD=1,FORM='ministro',   LEMMA='ministro',  TAG='noun'),
            Node(ID=1,DEPHEAD=1,FORM='acusaciones',LEMMA='acusación', TAG='noun'))
event_list.append(e11)

e12 = Event(Node(ID=1,DEPHEAD=1,FORM='dejó',       LEMMA='dejar',     TAG='verb'),
            Node(ID=1,DEPHEAD=1,FORM='inundación', LEMMA='inundación',TAG='noun'),
            Node(ID=1,DEPHEAD=1,FORM='ahogados',   LEMMA='ahogado',   TAG='noun'))
event_list.append(e12)


def print_dists(ALL=False):
    for i in range(len(event_list)):
        res = -1
        max_i = -1
        for j in range(len(event_list)):
            if i != j:
                if dist(event_list[i],event_list[j]) > res:
                    res = dist(event_list[i],event_list[j])
                    max_i = j
        print("e"+str(i)+"->e"+str(max_i)+"=>"+str(res))

    if(ALL):
        for i in range(len(event_list)):
            for j in range(len(event_list)):
                if i != j:
                    print("e"+str(i)+"->e"+str(j)+"=>"+str(dist(event_list[i],event_list[j])))

print_dists()

CWA(event_list)


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

clusters = clusterizar(event_list)
print_clusters(clusters)


list_corpus_files=['mapa_corpus_lemma_sociedad.txt','mapa_corpus_lemma_policiales.txt','mapa_corpus_lemma_economia.txt','mapa_corpus_lemma_politica.txt']
et_eventos=Etiquetado_eventos(list_corpus_files)

for cluster in clusters.values():
    label=et_eventos.set_label(cluster)
    # print(cluster)

print_clusters(clusters)
