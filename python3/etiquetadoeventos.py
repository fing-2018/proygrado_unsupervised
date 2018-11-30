# -*- coding: utf-8 -*-
from ast import literal_eval
from nltk.corpus import stopwords

class Etiquetado_eventos():
    def __init__(self):
        self._list_corpus_files = [('mapa_corpus_lemma_clima.txt', 'clima'),\
        ('mapa_corpus_lemma_policiales.txt', 'policiales'),\
        ('mapa_corpus_lemma_politica.txt', 'politica'),\
        ('mapa_corpus_lemma_economia.txt', 'economia'),\
        ('mapa_corpus_lemma_sociedad.txt', 'sociedad')]
        
    def set_label(self,event_list):
        word_list=self.word_list(event_list)
        list_occurs=[]
        for corpus in self._list_corpus_files:
            mapa=self.corpus_map(corpus)
            count_occurrs=0
            for w in word_list:
                if w in mapa:
                    count_occurrs=count_occurrs+mapa[w]
            list_occurs.append(count_occurrs)
        label=self._list_corpus_files[self.index_corpus(list_occurs)][1]
        # res={}
        # res["corpus_occurs"] = list_occurs
        # res["label"]=label
        for e in event_list:
            e.label = label
        print(list_occurs)
        return label
    
    def word_list(self,event_list):
        word_list=[]
        for e in event_list:
            word_list += self.get_lemmas(e.get_full_node(e.verb, is_verb=True, text=False))
            if (e.subj is not None):
                word_list += self.get_lemmas(e.get_full_node(e.subj, is_verb=False, text=False))
            if (e.obj is not None):
                word_list += self.get_lemmas(e.get_full_node(e.obj, is_verb=False, text=False))
        return word_list
        
    def get_lemmas(self, nodes_list):
        res = []
        for node in nodes_list:
            split_node = node.lemma.split('_')
            for split in split_node:
                if split not in stopwords.words('spanish'):
                    res.append(split)
        return res

    def index_corpus(self,list_occurs):
        return list_occurs.index(max(list_occurs))
        
    def corpus_map(self,archivo):
        ruta_dir = '/home/pablo/proygrado/freeling/share/freeling/APIs/python3/'
        file= open(ruta_dir+archivo[0],'r') 
        dict_corpus = literal_eval(file.read())
        file.close()
        return dict_corpus
