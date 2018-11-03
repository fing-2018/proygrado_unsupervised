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
			e.set_type(label)
		print(list_occurs)
		return label
	
	def word_list(self,event_list):
		word_list=[]
		for e in event_list:
			#print(str(e.lemma_verb()))
			if e.lemma_verb() != None and e.lemma_verb()!="": 
				word_list.append(e.lemma_verb())
			if e.lemma_subj() != None and e.lemma_subj()!="":
				word_list.append(e.lemma_subj())
			if e.lemma_obj() != None and e.lemma_obj()!="":
				word_list.append(e.lemma_obj())
		return word_list
		
	def index_corpus(self,list_occurs):
		return list_occurs.index(max(list_occurs))
		
	def corpus_map(self,archivo):
		file= open(archivo,'r') 
		dict_corpus = literal_eval(file.read())
		file.close()
		return dict_corpus