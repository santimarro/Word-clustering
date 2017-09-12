import nltk
import re

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

  stops = set(nltk.corpus.stopwords.words('spanish'))

  letters_only = re.findall(r'(\w+)', lavoz, re.UNICODE)
  
  # Convert to lower case, split into individual words
  words = [x.lower() for x in letters_only]
  print words

  # Remove stop words
  meaningful_words = [w for w in words if not w in stops]
  # Join the words back into one string separated by space,
  # and return the result.
  lavoz = " ".join(meaningful_words)
  
  return lavoz


def tokenize_only(text):
  # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
  tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
  filtered_tokens = []
  # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
  for token in tokens:
    if re.search(r'(\w+)', token, re.UNICODE):
        filtered_tokens.append(token)
  return filtered_tokens


def test():
  process_dump()
  #Open text dump
  print("------Comienzo-------")
  with open("output.txt") as f:
    lavozdump = f.readlines()
  totalvocab_stemmed = []
  totalvocab_tokenized = []

  for i in lavozdump:
    allwords_stemmed = tokenize_and_stem(i) #for each item in 'synopses', tokenize/stem
    totalvocab_stemmed.extend(allwords_stemmed) #extend the 'totalvocab_stemmed' list
    
    allwords_tokenized = tokenize_only(i)
    totalvocab_tokenized.extend(allwords_tokenized)

  vocab_frame = pd.DataFrame({'words': totalvocab_tokenized}, index = totalvocab_stemmed)
  print ('there are ' + str(vocab_frame.shape[0]) + ' items in vocab_frame')
  print (vocab_frame.head())
  
test()

