from nltk.cluster import KMeansClusterer
import nltk
import numpy as np 

def dist(i,j):
    return 1

def average_min_semantic_distance(u, v):
    matrix=np.matrix([[dist(i, j) for j in v] for i in u])
    return np.amin(matrix,axis=1).mean()

NUM_CLUSTERS=2#cantidad de secciones del diario
X=[['hola','loca'],['tu','vieja']]
#kclusterer = KMeansClusterer(NUM_CLUSTERS, distance=nltk.cluster.util.cosine_distance, repeats=25)
kclusterer = KMeansClusterer(NUM_CLUSTERS, distance=average_min_semantic_distance, repeats=25)
assigned_clusters = kclusterer.cluster(X, assign_clusters=True)
