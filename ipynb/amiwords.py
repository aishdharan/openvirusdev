import nltk
from nltk.tokenize import word_tokenize
from nltk import ne_chunk
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, LancasterStemmer, WordNetLemmatizer 
import os

import string
import re


def get_filtered_words_list(text_contents):
    content_words_list = []
    for text_content in text_contents:
        words = tokenize_clean_words(text_content)
        content_words_list.append(words)
    return content_words_list

def remove_xml_punkt_tokenize_stopwords(text_contents, minlen=2, lang='english'):
    nltk.download('stopwords')

    # filter words
    content_words_list = []
    for text_content in text_contents:
        words = tokenize_clean_words(text_content, 'english', 2)
        content_words_list.append(words)

    content_words = [word for lizt in content_words_list for word in lizt]
    return content_words


def tokenize_clean_words(text, lang='english', minlen=2):
    stop_lang = set(stopwords.words(lang))
    stop_sci = get_stopwords_sci();
    
    # remove (most) XML markup
    text_content1 = re.sub('</?[^>]*>', '', text)
    words = word_tokenize(text_content1)
    # remove stopwords, punctuation, and short words
    words = [w for w in words \
              if w.lower() not in stop_lang \
              and w not in stop_sci\
              and w not in string.punctuation\
              and not matches_noise(w)\
              and len(w) >= minlen
             ]
    return words

def matches_noise(word):
    return matches("\-?\d+|[A-Z]\.|et|al", word)
    
def matches(regex_str, word):
    regex = re.compile(regex_str)
    match = regex.fullmatch(word)
#    print("noise " + word +", "+str(match))
    return not match == None

def get_stopwords_sci():
    words =['et', 'al', 'J.']
    return set(words)

def read_text_contents(text_files):
    text_contents = []
    for text_file in text_files:
        text = read_file_contents(text_file)
        text_contents.append(text)

    return text_contents
    
def read_file_contents(text_file):
    text_filex = open(text_file,mode='r')
    text = text_filex.read()
    text_filex.close()
    return text

def extract_filtered_word_lists(files, lang='english', minlen=2):
    words_list = []
    for file in files:
        text = read_file_contents(file)
        words = tokenize_clean_words(text)
        words_list.append(words)
    return words_list
        

def stem_lemmatize(words, stemmer=PorterStemmer(), lemmatizer=WordNetLemmatizer()):

    stemmed = []
    for word in words :
        if (stemmer != None):
            word1 = stemmer.stem(word)
        elif (lemmatizer != None):
            word1 = lemmatizer.lemmatize(word)
        stemmed.append(word1)
    return stemmed

def chunk(text):    
    nltk.download('maxent_ne_chunker')
    nltk.download('words')
    # tokenize and POS Tagging before doing chunk
    tokens = word_tokenize(text)
    tags = nltk.pos_tag(tokens)
    chunk = ne_chunk(tags)
    return chunk

def noun_phrase(text):
    tokens = word_tokenize(text)
    tags = nltk.pos_tag(tokens)
    reg = "NP: {<DT>?<JJ>*<NN>}" 
    parser = nltk.RegexpParser(reg)
    np_tree = parser.parse(tags)
    return np_tree

def sentence_tokenizer(text):
    from nltk.tokenize import sent_tokenize
    sentences=sent_tokenize(text)
    print("sentences: "+str(len(sentences)))
    for sentence in sentences:
        print(">> "+sentence+"\n..")
        phrases = sentence.split("\n")
        print("??"+str(len(phrases)))
