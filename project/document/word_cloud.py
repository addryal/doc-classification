import re                                  # library for regular expression operations
import string                              # for string operations
from nltk.corpus import stopwords          # module for stop words that come with NLTK
from nltk.stem import PorterStemmer        # module for stemming
from nltk.tokenize import TweetTokenizer   # module for tokenizing strings
import nltk
import glob
import os
#nltk.download("stopwords")
from nltk.probability import FreqDist
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Agg')
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})


def word_frequency_analysis(upload_folder):

    file_list = glob.glob(os.path.join(upload_folder, "*.txt"))

    corpus = []
    tokenized_word =[]

    for file_path in file_list:
        head_tail = os.path.split(file_path)
        # print(head_tail[1])
        with open(file_path, encoding="utf8",errors='ignore') as f_input:
            corpus.append(f_input.read())

    #print(corpus)
    #print(type(corpus))
    separator = " "
    tokenized_word = pre_process(separator.join(corpus))
    fdist = FreqDist(tokenized_word)
    # print(fdist)
    #print(fdist.most_common(10))
    most_common_list = fdist.most_common(10)

    plt.barh(*zip(*most_common_list))
    plt.xlabel("Word Frequency")
    plt.ylabel("Common words")
    plt.title("Top 10 commonly occuring words in the corpus")
    ## Static path need to re-code dynamically
    #os.remove('D:/flask/upload/project/static/images/word_freq.png')
    plt.savefig('D:/flask/upload/project/static/images/word_freq.png')
    plt.clf()
    most_common_list=""



def pre_process(data):


    ## Preprocessing Starts - Removing URLs, terms within brackets
    pattern = r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
    data = re.sub(pattern,"",data)

    pattern = r"\(.{1,3}\)"
    data = re.sub(pattern,"",data)

    pattern = r"\(.{1,3}\)"
    data = re.sub(pattern,"",data)

    pattern =r"\\d+(?:\\.\\d+)?%"
    data = re.sub(pattern,"",data)

    ## Tokenizing the document
    tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True,reduce_len=True)
    csa_tokens = tokenizer.tokenize(data)

    # Removing stopwords and punctuations
    stopwords_english = stopwords.words('english')
    csa_clean = []

    for word in csa_tokens: # Go through every word in your tokens list
        if (word not in stopwords_english and  # remove stopwords
            word not in string.punctuation and
            word.isalpha()):  # remove punctuation
            csa_clean.append(word)

    # ## Stemming the document
    # # Instantiate stemming class
    # stemmer = PorterStemmer()
    #
    # # Create an empty list to store the stems
    # csa_stem = []
    #
    # for word in csa_clean:
    #     stem_word = stemmer.stem(word)  # stemming word
    #     csa_stem.append(stem_word)  # append to the list
    data=""
    return csa_clean

# upload_folder = 'C:/Users/Computer/Desktop/upload_folder/'
#
# word_frequency_analysis(upload_folder)
