import nltk
import re
from sklearn.feature_extraction import DictVectorizer
from sklearn.cluster import KMeans
import spacy


# Load the spanish lemma dictionary
lemma_dict = {}
with open("lemmatization-es.txt") as f:
  for line in f:
     (key, val) = line.split()
     lemma_dict[key] = val


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
        #features['tag'] = token.tag
        features['pos'] = token.pos
        # Save the previous and next token info
        if previous_token is None:
          features['word-1'] = 'start'
        else:
          features['word-1'] = previous_token.orth_
          features['word-1-pos'] = previous_token.pos

        # Save the dependencie of the token and with whom is related
        features['dep'] = token.dep
        features['dep-head'] = token.head.orth_

        features['word+1'] = token.nbor().orth_
        features['word+1-pos'] = token.nbor().pos
        final_features.append(features)
        control_list.append(token.orth_)
      previous_token = token

  return final_features, control_list


def test_spacy():
  # lavoz = process_dump()
  parser = spacy.load('es')
  example = 'El niño juega con la pelota amarilla en la playa. Luego la pelota se rompió.'
  parsedData = parser(example)
  # Generate feature dict
  features, control_list = generate_features(parsedData)
  print (features)
  print ("------------")
  print (control_list)

  # Vectorize the feature dictionary
  v = DictVectorizer()
  X = v.fit_transform(features)
  print(X)
  # Kmeans
  kmeans = KMeans(n_clusters=30, random_state=0).fit(X)
  labels = kmeans.labels_
  print (labels)
  return 0


test_spacy()


