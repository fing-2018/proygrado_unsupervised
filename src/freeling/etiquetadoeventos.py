# -*- coding: utf-8 -*-
from ast import literal_eval

class Etiquetado_eventos():
    def __init__(self,list_corpus_files=[]):
        self.list_corpus_files = list_corpus_files
        
    def set_label(self,event_list):
        word_list=self.word_list(event_list)
        list_occurs=[]
        for corpus in self.list_corpus_files:
            map=self.corpus_map(corpus)
            count_occurrs=0
            for w in word_list:
                if w in map:
                    count_occurrs=count_occurrs+map[w]
            list_occurs.append(count_occurrs)
        res={}
        res["corpus_occurs"] = list_occurs
        label=self.list_corpus_files[self.index_corpus(list_occurs)].split(".")[0]
        res["label"]=label
        for e in event_list:
            e.label = label
        print(list_occurs)
        return label
    
    def word_list(self,event_list):
        word_list=[]
        for e in event_list:
            #print(str(e.verb))
            if e.verb.lemma != None and e.verb.lemma!="": 
                word_list.append(e.verb.lemma)
            if e.subj.lemma != None and e.subj.lemma!="":
                word_list.append(e.subj)
            if e.obj.lemma != None and e.obj.lemma!="":
                word_list.append(e.obj.lemma)
        return word_list
        
    def index_corpus(self,list_occurs):
        return list_occurs.index(max(list_occurs))
        
    def corpus_map(self,archivo):
        file= open(archivo,'r',encoding='latin1') 
        dict_corpus = literal_eval(file.read())
        file.close()
        return dict_corpus