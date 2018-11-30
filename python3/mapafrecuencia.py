from ast import literal_eval
def mapa_frecuencia():
    archivos=['corpus_lemma_clima.txt', 'corpus_lemma_policiales.txt', 'corpus_lemma_sociedad.txt', 'corpus_lemma_economia.txt', 'corpus_lemma_politica.txt']
    for archivo in archivos:
        file = open(archivo,'r')
        lemma_list=file.read().split()
        file.close()
        mapa_corpus={}
        count_words=len(lemma_list)
        for l in lemma_list:
            if l in mapa_corpus:
                mapa_corpus[l]+=1/count_words
            else:
                mapa_corpus[l]=1/count_words
        print(mapa_corpus)
        file=open("mapa_"+archivo,'w')
        file.write(str(mapa_corpus))
        file.close()
        print(count_words)

mapa_frecuencia() 
