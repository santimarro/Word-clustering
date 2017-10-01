import re
import process_dump
from sklearn.feature_extraction import DictVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans
import spacy


def word_clustering():

  with open(r"features.pickle", "rb") as input_file:
    features = cPickle.load(input_file)
    
  with open(r"control_list.pickle", "rb") as input_file:
    control_list = cPickle.load(input_file)

  # Vectorize the feature dictionary
  v = DictVectorizer()
  X = v.fit_transform(features)
  # Normalize the matrix
  X_norm = normalize(X)
  # Reduce dimensionality
  svd = TruncatedSVD(n_components=100, n_iter=7, random_state=42)
  Y = svd.fit_transform(X)
  # Kmeans
  n = 120
  kmeans = KMeans(n_clusters=n, random_state=0).fit(Y)
  labels = kmeans.labels_
  clusters = []
  count = [0]*n

  for i, val in enumerate(labels):
    item = (control_list[i], val)
    if item not in clusters:
      clusters.append(item)
      count[val] += 1

  clusters.sort(key=lambda x: x[1])
  print (count)
  cluster_number = 0
  counter = 0
  cluster = []
  with open("resultado_clustering_" + str(n) + "_clusters", "wb") as f:
    for i in range(sum(count)):
      if counter >= count[val]:
        cluster_number += 1
        counter = 0
        f.write('\n')
        f.write('----------- Cluster: ' + str(cluster_number) + '----------------')
        f.write('\n')
        f.write(cluster)
        cluster = []

      counter += 1
      cluster.append(clusters[i][0])

  return 0


word_clustering()



