import spacy

class WordEmbeddings():

    def __init__(self):
        self.__nlp = spacy.load('es_core_news_md') 

    def similar_words(self,a,b,THRESHOLD=0.3,PRINT=True):
        token_a = self.__nlp(a)
        token_b = self.__nlp(b)
        similarity = token_a.similarity(token_b)
        if PRINT:
            print("Similitud entre "+a+" y "+b+": "+str(similarity))
        return similarity > THRESHOLD

    def similar_words(self,a,b):
        token_a = self.__nlp(a)
        token_b = self.__nlp(b)
        similarity = token_a.similarity(token_b)
        return similarity

