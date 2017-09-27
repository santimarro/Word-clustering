import re
from sklearn.feature_extraction import DictVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans
import spacy

'''
# Load the spanish lemma dictionary
lemma_dict = {}
with open("lemmatization-es.txt") as f:
  for line in f:
     (key, val) = line.split()
     lemma_dict[key] = val
'''

def process_dump():
  with open("xaa") as f:
      lavozdump = f.readlines()

  lavozdump = [x.strip() for x in lavozdump]

  lavoz = " ".join(lavozdump)
  letters_only = re.findall(r'(\w+)', lavoz, re.UNICODE)
  # Convert to lower case, split into individual words
  # words = [x.lower() for x in letters_only]
  # Remove stop words
  # meaningful_words = [w for w in words if not w in spanish_stopwords]
  # Join the words back into one string separated by space,
  # and return the result.
  lavoz = " ".join(letters_only)
  # lavoz = " ".join(meaningful_words)
  with open("output.txt", "w") as f:
    f.write(lavoz)
  return lavoz

def generate_features(parsedData):
  '''
  Version 0.1, proximo paso es automatizar la creacion de este diccionario,
  usando las palabras claves que aparecen en por ejemplo token.tag.
  Ver tema de las palabras repetidas, como hacer para separar.
  '''
  final_features = []
  control_list = []
  puntuaction = ['¡', '!', '¿', '?', '.', ';', ':', ',', '"']
  previous_token = None
  for token in parsedData:
    if not token.orth_ in puntuaction:
      if not token.is_stop:
        features = {}
        features['lowercase'] = token.is_lower
        features['tag'] = token.tag_
        features['pos'] = token.pos
        # Save the previous and next token info
        if previous_token is not None:
          features['word-1'] = token.nbor(-1).orth_
          features['word-1-pos'] = token.nbor(-1).pos

        # Save the dependencie of the token and with whom is related
        features[token.dep_] = token.head.orth_
        # The pos tagging of the head token
        features['head-pos'] = token.head.pos
        
        try:
          features['word+1'] = token.nbor().orth_
          features['word+1-pos'] = token.nbor().pos
        except IndexError:
          pass

        final_features.append(features)
        control_list.append(token.orth_)
      previous_token = token

  return final_features, control_list


def test_spacy():
  lavoz = process_dump()
  example = "El niño juega con -la pelota amarilla. ¿El niño luego rompió la pelota amarilla, por lo que buscó la pelota azul."
  parser = spacy.load('es')
  parsedData = parser(lavoz)
  # Generate feature dict
  features, control_list = generate_features(parsedData)

  # Vectorize the feature dictionary
  v = DictVectorizer()
  X = v.fit_transform(features)
  
  print(v.get_feature_names())
  import ipdb; ipdb.set_trace()
  # Reduce dimensionality
  svd = TruncatedSVD(n_components=200000, n_iter=7, random_state=42)
  Y = svd.fit_transform(X)
  # Kmeans
  n = 40
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
  print ('----------- Cluster: 0 ----------------')
  val = 0
  counter = 0
  for i in range(sum(count)):
    if counter >= count[val]:
      val += 1
      counter = 0
      print('----------- Cluster: ' + str(val) + '----------------')
      print('\n')

    counter += 1
    print(clusters[i])
    print('\n')
 
  # print(clusters)
  return 0


test_spacy()



'''
TODO:
  Revisar preprocesamiento, sacar solo caracteres raros, no puntuacion.
  Reduccion de dimensionalidad.
  Ver de elegir features para distintas corridas.
  Analizar clusters
  

'''



