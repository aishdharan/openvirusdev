from nltk.probability import FreqDist
import matplotlib.pyplot as plt

from sklearn.cluster import MiniBatchKMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

import amifiles as af
import amiwords as aw

def analyze_frequencies_all(project):

    for section in af.get_glob_dict_all():
        analyze_frequencies_section(project, section)
        
def analyze_frequencies_section(project, section):
    glob_expr = af.get_glob_dict_all()[section][1]
    print("glob " + glob_expr)
    files = af.get_globbed_files(project, glob_expr)
    analyze_frequencies(files, section)
    print("files " + str(len(files)))

def analyze_frequencies(files, title):
    text_contents = aw.read_text_contents(files)
    words = aw.remove_xml_punkt_tokenize_stopwords(text_contents)
    plot_frequency(words, title)
	
def plot_frequency(words, title="title"):
    fdist = FreqDist(words)
    print(fdist.most_common(30))
    fdist.plot(30, title=title)
    
def count_vectorize():
    """
    not tested
    """
    from sklearn.feature_extraction.text import CountVectorizer
    from nltk.tokenize import RegexpTokenizer
    #tokenizer to remove unwanted elements from out data like symbols and numbers
    token = RegexpTokenizer(r'[a-zA-Z0-9]+')
    cv = CountVectorizer(lowercase=True,stop_words='english',ngram_range = (1,1),tokenizer = token.tokenize)

def tfidfVector():
    """
    not tested
    """
    from sklearn.feature_extraction.text import TfidfVectorizer
    tf=TfidfVectorizer()
    # text_tf= tf.fit_transform(data['Phrase'])
    text_tf= tf.fit_transform(phrases)
    
def tfidf():
    """
    not tested
    """
    import pandas as pd 
    from sklearn.feature_extraction.text import TfidfTransformer
    from sklearn.feature_extraction.text import CountVectorizer
    cv=CountVectorizer() 
    word_count_vector=cv.fit_transform(sentences)
    tfidf_transformer=TfidfTransformer(smooth_idf=True,use_idf=True) 
    tfidf_transformer.fit(word_count_vector)
    # print idf values 
    df_idf = pd.DataFrame(tfidf_transformer.idf_, index=cv.get_feature_names(),columns=["idf_weights"]) 

    # sort ascending 
    df_idf.sort_values(by=['idf_weights'])

def find_optimal_clusters(data, max_k):
    iters = range(2, max_k+1, 2)
    
    sse = []
    for k in iters:
        sse.append(MiniBatchKMeans(n_clusters=k, init_size=1024, batch_size=2048, random_state=20).fit(data).inertia_)
        print('Fit {} clusters'.format(k))
        
    f, ax = plt.subplots(1, 1)
    ax.plot(iters, sse, marker='o')
    ax.set_xlabel('Cluster Centers')
    ax.set_xticks(iters)
    ax.set_xticklabels(iters)
    ax.set_ylabel('SSE')
    ax.set_title('SSE by Cluster Center Plot')
   
