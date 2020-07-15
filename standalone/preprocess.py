import re                                  # library for regular expression operations
import string                              # for string operations

from nltk.corpus import stopwords          # module for stop words that come with NLTK
from nltk.stem import PorterStemmer        # module for stemming
from nltk.tokenize import TweetTokenizer   # module for tokenizing strings
import nltk
nltk.download("stopwords")



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

    ## Stemming the document
    # Instantiate stemming class
    stemmer = PorterStemmer()

    # Create an empty list to store the stems
    csa_stem = []

    for word in csa_clean:
        stem_word = stemmer.stem(word)  # stemming word
        csa_stem.append(stem_word)  # append to the list

    return csa_stem
