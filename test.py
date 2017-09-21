import nltk
import re
from nltk.stem import SnowballStemmer
from nltk import word_tokenize
from nltk.data import load
from string import punctuation
from sklearn.feature_extraction.text import CountVectorizer
import spacy

'''
stemmer = SnowballStemmer('spanish')
spanish_stopwords = set(nltk.corpus.stopwords.words('spanish'))
non_words = list(punctuation)
non_words.extend(['¿', '¡'])
non_words.extend(map(str,range(10)))

'''

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


def generate_features():
  features = {}
  i = 0
  if not token.is_stop():
    for token in parsedData:
      # features['lemma'] = lema sacado del lexiconer
      features['lowercase'] = token.orth_.islower()
      features['tag'] = token.tag
      features['tag'] = token.pos
      features['left_word'] = [t.orth_ for t in token.lefts]
      features['left_tag'] = [t.tag for t in token.lefts]
      features['right_word'] = [t.orth_ for t in token.rights]
      features['right_tag'] = [t.tag for t in token.lefts]
      features['dep'] = token.dep
      control_list[i] = token.orth_
      i+=1

  return features, control_list


def test_spacy():
  lavoz = process_dump()
  parser = spacy.load('es')
  parsedData = parser(lavoz)
  # Generate feature dict
  features, control_list = generate_features()
  # Vectorize the feature dictionary
  
  return 0


test_spacy()


