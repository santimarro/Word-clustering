import re
import spacy
import _pickle as cPickle
from nltk.corpus import stopwords
from sklearn.feature_extraction import DictVectorizer

WORD = 0
LEMMA = 1
POS = 2
SYNSET = 3


def vectorize(features):
  # Vectorize the feature dictionary
  v = DictVectorizer()
  X = v.fit_transform(features)
  return X


def generate_features(parsedData):

  final_features = []
  control_list = []
  puntuaction = ['¡', '!', '¿', '?', '.', ';', ':', ',', '"']
  previous_token = None
  for token in parsedData:
    if not token.orth_ in puntuaction:
      if not token.is_stop:
        features = {}
        features['lowercase'] = token.is_lower
        # features['tag'] = token.tag_
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


def generate_features_supervised(parsedData):
  stop_words = set(stopwords.words('spanish'))
  final_features = []
  control_list = []
  target_vector = []
  puntuaction = ['¡', '!', '¿', '?', '.', ';', ':', ',', '"']
  for i, token in enumerate(parsedData):
    if not token[WORD] in puntuaction:
      if not token[WORD] in stop_words:
        if token[SYNSET] != '0' and token[SYNSET].isdigit():
          features = {}
          features['lemma'] = token[LEMMA]
          features['pos'] = token[POS]
          # features['synset'] = token[SYNSET]
          # Save the previous and next token info
          try:
            features['word+1'] = parsedData[i+1][LEMMA]
            features['word+1-pos'] = parsedData[i+1][POS]
            features['word-1'] = parsedData[i-1][LEMMA]
            features['word-1-pos'] = parsedData[i-1][POS]
          except IndexError:
            pass
        
          # Save the synset as the target vector
          target_vector.append(token[SYNSET])
          final_features.append(features)
          control_list.append(token[WORD])
  return final_features, control_list, target_vector


def process_dump_supervised():
  with open("xaa") as f:
      corpus = f.readlines()

  exceptions = [[], ['</doc>']]
  corpus_ = [x.split() for x in corpus]
  corpus_ = [x for x in corpus_ if x not in exceptions and len(x) == 4]

  # Generate feature dict
  features, control_list, target_vector = generate_features_supervised(corpus_)
  with open(r"features.pickle", "wb") as output_file:
    cPickle.dump(features, output_file)
  
  with open(r"control_list.pickle", "wb") as output_file:
    cPickle.dump(control_list, output_file)
    
  with open(r"target_vector.pickle", "wb") as output_file:
    cPickle.dump(target_vector, output_file)
  
  X = vectorize(features)
  with open(r"X.pickle", "wb") as output_file:
    cPickle.dump(X, output_file)
  print('Done processing')
  return 0


def process_dump_unsupervised():
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
  
  parser = spacy.load('es')
  parsedData = parser(lavoz)
  # Generate feature dict
  features, control_list = generate_features(parsedData)
  with open(r"features.pickle", "wb") as output_file:
    cPickle.dump(features, output_file)
  
  with open(r"control_list.pickle", "wb") as output_file:
    cPickle.dump(control_list, output_file)
 
  X = vectorize(features)
  with open(r"X.pickle", "wb") as output_file:
    cPickle.dump(X, output_file)

  return 0

process_dump_supervised()  

