import spacy
from nltk.corpus import stopwords

class WordEmbeddings():

    def __init__(self):
        print('entro al spacy.load')
        self.__nlp = spacy.load('es_core_news_md') 

    def similar_words(self,a,b,THRESHOLD=0.3,PRINT=False):
        token_a = self.__nlp(a)
        token_b = self.__nlp(b)
        similarity = token_a.similarity(token_b)
        #if PRINT:
        #    print("Similitud entre "+a+" y "+b+": "+str(similarity))
        return similarity > THRESHOLD

    def similarity(self,a,b):
        a_sin_sw = ' '.join([word for word in a.split() if word not in stopwords.words('spanish')])
        b_sin_sw = ' '.join([word for word in b.split() if word not in stopwords.words('spanish')])
        return self.__nlp(a_sin_sw).similarity(self.__nlp(b_sin_sw))

         

