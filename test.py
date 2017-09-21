import nltk
import re
from nltk.stem import SnowballStemmer
from nltk import word_tokenize
from nltk.data import load
from string import punctuation
from sklearn.feature_extraction.text import CountVectorizer
import spacy

stemmer = SnowballStemmer('spanish')
spanish_stopwords = set(nltk.corpus.stopwords.words('spanish'))
non_words = list(punctuation)
non_words.extend(['¿', '¡'])
non_words.extend(map(str,range(10)))
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

def stem_tokens(tokens, stemmer):
  stemmed = []
  for item in tokens:
    stemmed.append(stemmer.stem(item))
  return stemmed


def tokenize(text):
  text = ' '.join([c for c in text if c not in non_words])
  tokens =  word_tokenize(text)

  # lemmatize
  try:
    stems = stem_tokens(tokens, stemmer)
  except Exception as e:
    print(e)
    print(text)
    stems = ['']
  return stems


def test_spacy():
  # lavoz = process_dump()
  example = "El niño jugaba con el perro blanco en la playa. Luego el perro murió"
  parser = spacy.load('es')
  parsedData = parser(example)
  for i, token in enumerate(parsedData):
    print("original:", token.orth, token.orth_)
    print("lowercased:", token.lower, token.lower_)
    print("lemma:", token.lemma, token.lemma_)
    print("shape:", token.shape, token.shape_)
    print("prefix:", token.prefix, token.prefix_)
    print("suffix:", token.suffix, token.suffix_)
    print("log probability:", token.prob)
    print("Brown cluster id:", token.cluster)
    print("----------------------------------------")
    if i > 1:
        break
        
  for token in parsedData:
    print(token.orth_, token.dep_, token.head.orth_, [t.orth_ for t in token.lefts], [t.orth_ for t in token.rights])
        
  # Let's look at the sentences
  sents = []
  # the "sents" property returns spans
  # spans have indices into the original string
  # where each index value represents a token

  # Let's look at the part of speech tags of the first sentence
  for span in parsedData.sents:
      sent = [parsedData[i] for i in range(span.start, span.end)]
      break

  for token in sent:
      print(token.orth_, token.pos_)
  
  return 0


test_spacy()
'''

vectorizer = CountVectorizer(
                input = 'output.txt',
                analyzer = 'word',
                tokenizer = tokenize,
                lowercase = True,
                stop_words = spanish_stopwords)

def test():
  process_dump()
  #Open text dump
  print("------Comienzo-------")
  with open("output.txt") as f:
    lavozdump = f.readlines()
  totalvocab_lemmatized = []
  totalvocab_tokenized = []

  for i in lavozdump:
    allwords_lemmatized = tokenize_and_lemmatize(i) #for each item in 'synopses', tokenize/lemmatize
    totalvocab_stemmed.extend(allwords_lemmatized) #extend the 'totalvocab_stemmed' list
    
    allwords_tokenized = tokenize_only(i)
    totalvocab_tokenized.extend(allwords_tokenized)

  vocab_frame = pd.DataFrame({'words': totalvocab_tokenized}, index = totalvocab_stemmed)
  print ('there are ' + str(vocab_frame.shape[0]) + ' items in vocab_frame')
  print (vocab_frame.head())
  
test()
'''


