import nltk
import re
from nltk.stem import SnowballStemmer
from nltk import word_tokenize
from nltk.data import load
from string import punctuation
from sklearn.feature_extraction.text import CountVectorizer       

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
  with open("xab") as f:
      lavozdump = f.readlines()

  lavozdump = [x.strip() for x in lavozdump]

  lavoz = " ".join(lavozdump)

  letters_only = re.findall(r'(\w+)', lavoz, re.UNICODE)
  # Convert to lower case, split into individual words
  words = [x.lower() for x in letters_only]
  # Remove stop words
  meaningful_words = [w for w in words if not w in stops]
  # Join the words back into one string separated by space,
  # and return the result.
  lavoz = " ".join(meaningful_words)
  with open("output.txt", "w") as f:
    f.write(lavoz)
  return 0

def stem_tokens(tokens, stemmer):
  stemmed = []
  for item in tokens:
    stemmed.append(stemmer.stem(item))
  return stemmed


def tokenize(text):
  text = ''.join([c for c in text if c not in non_words])
  tokens =  word_tokenize(text)

  # lemmatize
  try:
    stems = stem_tokens(tokens, stemmer)
  except Exception as e:
    print(e)
    print(text)
    stems = ['']
  return stems


vectorizer = CountVectorizer(
                input = 'output.txt',
                analyzer = 'word',
                tokenizer = tokenize,
                lowercase = True,
                stop_words = spanish_stopwords)

'''
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


