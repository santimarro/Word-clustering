import re
from sklearn.feature_extraction import DictVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans
from sklearn.preprocessing import normalize
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
import _pickle as cPickle

  
def normalize(X):
    X_norm = normalize(X)
    return X_norm


def reduce_dimm_svd(X, n, m):
  svd = TruncatedSVD(n_components=n, n_iter=m, random_state=42)
  Y = svd.fit_transform(X)
  return Y


def univariate_feature_selection(X, y):
  X_new = SelectKBest(chi2, k=2).fit_transform(X, y)
  return X_new

def kmeans(X, n):
  kmeans = KMeans(n_clusters=n, random_state=0).fit(X)
  labels = kmeans.labels_
  return labels

def word_clustering(features, control_list, X, target_vector=0):

  # Normalize the matrix
  X_norm = normalize(X)
  # Reduce dimensionality
  if target_vector:
    Y = univariate_feature_selection(X_norm, target_vector)
  else:
    Y = reduce_dimm_svd(X_norm, 100, 7)

  # Kmeans
  n = 120
  labels = kmeans(Y, n)
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
        f.write(str(cluster))
        cluster = []

      counter += 1
      cluster.append(clusters[i][0])

  return 0

# Get the features dict
with open(r"features.pickle", "rb") as input_file:
  features = cPickle.load(input_file)

# Get the control_list  
with open(r"control_list.pickle", "rb") as input_file:
  control_list = cPickle.load(input_file)

# Get the target_vector
with open(r"target_vector.pickle", "rb") as input_file:
  target_vector = cPickle.load(input_file)

#Get the vectorized matrix
with open(r"X.pickle", "rb") as input_file:
  X = cPickle.load(input_file)

word_clustering(features, control_list, X, target_vector)



