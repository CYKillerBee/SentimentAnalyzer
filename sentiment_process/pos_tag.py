
from nltk import word_tokenize
from nltk.corpus import wordnet, stopwords
from nltk.tag import pos_tag



def token_stop_pos(text):

    # POS tagger dictionary
    pos_dict = {'J': wordnet.ADJ, 'V': wordnet.VERB, 'N': wordnet.NOUN, 'R': wordnet.ADV}

    tags = pos_tag(word_tokenize(text))
    newlist = []
    for word, tag in tags:
        if word.lower() not in set(stopwords.words('english')):
            newlist.append(tuple([word, pos_dict.get(tag[0])]))
    return newlist

