import re
import spacy
import _pickle as cPickle

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
  
  parser = spacy.load('es')
  parsedData = parser(lavoz)
  # Generate feature dict
  features, control_list = generate_features(parsedData)
  with open(r"features.pickle", "wb") as output_file:
    cPickle.dump(features, output_file)
  
  with open(r"control_list.pickle", "wb") as output_file:
    cPickle.dump(control_list, output_file)

  return 0

process_dump()  

