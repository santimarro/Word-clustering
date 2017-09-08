import nltk
import pandas as pd
import re

# load nltk's SnowballStemmer as variabled 'stemmer'
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("spanish")

def process_dump():
  with open("lavoztextodump.txt") as f:
      lavozdump = f.readlines()

  lavozdump = [x.strip() for x in lavozdump]

  lavoz = " ".join(lavozdump)

  stops = set(nltk.corpus.stopwords.words('spanish'))

  letters_only = re.sub("[^a-zA-Z]", " ", lavoz) 
  #
  # 3. Convert to lower case, split into individual words
  words = letters_only.lower().split()                                          
  # 
  # 5. Remove stop words
  meaningful_words = [w for w in words if not w in stops]   
  #
  # 6. Join the words back into one string separated by space, 
  # and return the result.
  lavoz = " ".join(meaningful_words)  
  with open("output.txt", "w") as text_file:
    text_file.write(lavoz)
  
  return 0


def tokenize_and_stem(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems


def tokenize_only(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    return filtered_tokens

def test():
  # process_dump()
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

