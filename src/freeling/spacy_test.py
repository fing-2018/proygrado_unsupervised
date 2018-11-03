# -*- coding: utf-8 -*-

# import spacy

from random import shuffle
from chinese import dist,Event,Node

# class Event(object):
#     def __init__(self,token):
#         self.token = token
#         self.type  = -1

#     def __repr__(self):
#         return '{}: {} {}'.format(self.__class__.__name__, self.token, self.type)

#     def __cmp__(self, other):
#         return self.type.__cmp__(other.type)

#Chinese Whispers Algorithm
# def CWA(event_list):
#     for i in range(len(event_list)):
#         event_list[i].type = i
#     not_converged = True
#     while not_converged:
#         shuffle(event_list)
#         clases_antes = [event.type for event in event_list]
#         for i in range(len(event_list)):
#             max_similarity = -1
#             for j in range(len(event_list)):
#                 if i != j:
#                     similarity = event_list[i].token.similarity(event_list[j].token)
#                     if similarity > max_similarity:
#                         max_similarity = similarity
#                         event_list[i].type = event_list[j].type
#         clases_despues = [event.type for event in event_list]
#         not_converged = clases_antes != clases_despues


#Chinese Whispers Algorithm
def CWA(event_list):
    for i in range(len(event_list)):
        event_list[i].type = i
    not_converged = True
    while not_converged:
        for e in event_list:
            print(e)
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


# nlp = spacy.load('es_core_news_md')

# tokens = nlp(unicode('manzana banana pera zapato camisa pantalón sombrero tormenta temporal lluvia uva banana ropa clima fruta comida rayo nieve ozono',"utf-8"))

event_list = []
# for token in tokens:
#     event_list.append(Event(token))


e1  = Event(Node(FORM='causó',      LEMMA='causar',    TAG='verb'),
            Node(FORM='lluvia',     LEMMA='lluvia',    TAG='noun'),
            Node(FORM='destrozos',  LEMMA='destrozo',  TAG='noun'))
event_list.append(e1)

e2  = Event(Node(FORM='provocó',    LEMMA='provocar',  TAG='verb'),
            Node(FORM='guerra',     LEMMA='guerra',    TAG='noun'),
            Node(FORM='muerte',     LEMMA='muerte',    TAG='noun'))
event_list.append(e2)

e3  = Event(Node(FORM='produjo',    LEMMA='producir',  TAG='verb'),
            Node(FORM='nieve',      LEMMA='nieve',     TAG='noun'),
            Node(FORM='felicidad',  LEMMA='felicidad', TAG='noun'))
event_list.append(e3)

e4  = Event(Node(FORM='destruyó',   LEMMA='destruir',  TAG='verb'),
            Node(FORM='tormenta',   LEMMA='tormenta',  TAG='noun'),
            Node(FORM='casa',       LEMMA='casa',      TAG='noun'))
event_list.append(e4)

e5  = Event(Node(FORM='dejó',       LEMMA='dejar',     TAG='verb'),
            Node(FORM='batalla',    LEMMA='batalla',   TAG='noun'),
            Node(FORM='heridos',    LEMMA='herido',    TAG='noun'))
event_list.append(e5)

e6  = Event(Node(FORM='voló',       LEMMA='volar',     TAG='verb'),
            Node(FORM='viento',     LEMMA='viento',    TAG='noun'),
            Node(FORM='techos',     LEMMA='techo',     TAG='noun'))
event_list.append(e6)

e7  = Event(Node(FORM='aumentó',    LEMMA='aumentar',  TAG='verb'),
            Node(FORM='presidente', LEMMA='presidente',TAG='noun'),
            Node(FORM='impuestos',  LEMMA='impuesto',  TAG='noun'))
event_list.append(e7)

e8  = Event(Node(FORM='aprobó',     LEMMA='aprobar',   TAG='verb'),
            Node(FORM='gobierno',   LEMMA='gobierno',  TAG='noun'),
            Node(FORM='ley',        LEMMA='ley',       TAG='noun'))
event_list.append(e8)

e9  = Event(Node(FORM='explotó',    LEMMA='explotar',  TAG='verb'),
            Node(FORM='bomba',      LEMMA='bomba',     TAG='noun'),
            Node(FORM='hospital',   LEMMA='hospital',  TAG='noun'))
event_list.append(e9)

e10 = Event(Node(FORM='mató',       LEMMA='matar',     TAG='verb'),
            Node(FORM='temporal',   LEMMA='temporal',  TAG='noun'),
            Node(FORM='ganado',     LEMMA='ganado',    TAG='noun'))
event_list.append(e10)

e11 = Event(Node(FORM='negó',       LEMMA='negar',     TAG='verb'),
            Node(FORM='ministro',   LEMMA='ministro',  TAG='noun'),
            Node(FORM='acusaciones',LEMMA='acusación', TAG='noun'))
event_list.append(e11)

e12 = Event(Node(FORM='dejó',       LEMMA='dejar',     TAG='verb'),
            Node(FORM='inundación', LEMMA='inundación',TAG='noun'),
            Node(FORM='ahogados',   LEMMA='ahogado',   TAG='noun'))
event_list.append(e12)


# --------
for i in range(len(event_list)):
    res = -1
    max_i = -1
    for j in range(len(event_list)):
        if i != j:
            if dist(event_list[i],event_list[j]) > res:
                res = dist(event_list[i],event_list[j])
                max_i = j
    print("e"+str(i)+"->e"+str(max_i)+"=>"+str(res))

for i in range(len(event_list)):
    for j in range(len(event_list)):
        if i != j:
            print("e"+str(i)+"->e"+str(j)+"=>"+str(dist(event_list[i],event_list[j])))


CWA(event_list)

# print(sorted(event_list))
cluster = -1
for event in sorted(event_list, key=lambda e : e.type):
    if event.type != cluster:
        cluster = event.type
        print("======CLUSTER======")
    print(event)
