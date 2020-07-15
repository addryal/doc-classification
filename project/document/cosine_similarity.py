from sklearn.feature_extraction.text import TfidfVectorizer
import os
import glob
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
import shutil


def correlation_plot():
    file_list = glob.glob(os.path.join(os.getcwd(), "text_files", "*.txt"))

    corpus = []

    for file_path in file_list:
        head_tail = os.path.split(file_path)
        # print(head_tail[1])
        with open(file_path, encoding="utf8",errors="ignore") as f_input:
            corpus.append(f_input.read())

    doc_num = len(corpus)

    doc_ids = [os.path.split(file_path)[1] for file_path in file_list]
    vectorizer = TfidfVectorizer(token_pattern=r'(?u)\b[A-Za-z]+\b')
    tfidf = vectorizer.fit_transform(corpus)
    feature_names = vectorizer.get_feature_names()
    print(feature_names)
    print(len(feature_names))
    # no need to normalize, since Vectorizer will return normalized tf-idf
    pairwise_similarity = tfidf * tfidf.T
    psim_array = pairwise_similarity.toarray()

    sns.set(style="white")

    # Set up the matplotlib figure
    # (to enlarge the cells, increase the figure size)
    f, ax = plt.subplots(figsize=(20, 20))

    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(220, 20, as_cmap=True)

    # Generate a mask for the upper triangle
    mask = np.zeros_like(psim_array, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True

    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(psim_array, mask=mask, cmap=cmap, center=0.5,
                square=True, linewidths=.5, fmt='.2f',
                annot=True, cbar_kws={"shrink": .5}, vmax=1, annot_kws={"fontsize": 10})

    ax.set_xticklabels(labels=doc_ids, rotation=90, fontsize=8)
    ax.set_yticklabels(labels=doc_ids, rotation=0)
    ax.set_xlabel('')
    ax.set_ylabel("")
    plt.subplots_adjust(bottom=0.25)
    # bytes_image = io.BytesIO()
    #plt.savefig(bytes_image, format='png')
    plt.savefig('figure.png', format='png')
    plt.show()


    # bytes_image.seek(0)
    # return bytes_image


def setup_base_csa(upload_folder):

    file_list = glob.glob(os.path.join(upload_folder, "*.txt"))

    corpus = []

    for file_path in file_list:
        head_tail = os.path.split(file_path)
        # print(head_tail[1])
        with open(file_path, encoding="utf8",errors='ignore') as f_input:
            corpus.append(f_input.read())

    doc_num = len(corpus)

    doc_ids = [os.path.split(file_path)[1] for file_path in file_list]
    vectorizer = TfidfVectorizer(token_pattern=r'(?u)\b[A-Za-z]+\b')
    tfidf = vectorizer.fit_transform(corpus)
    feature_names = vectorizer.get_feature_names()
    # no need to normalize, since Vectorizer will return normalized tf-idf
    pairwise_similarity = tfidf * tfidf.T
    psim_array = pairwise_similarity.toarray()
    df = pd.DataFrame(pairwise_similarity.toarray())
    df.index = doc_ids
    df.columns = doc_ids
    avg_csa_correlation = df.values[np.triu_indices_from(df.values,1)].mean()
    return avg_csa_correlation,feature_names
# print(pairwise_similarity)
# print(psim_array)
#print(pairwise_similarity)

def check_new_doc(new_file_path):
    #Upload it to the folder
    #new_file_path = "C:/Users/Computer/Desktop/text_archive/Trump.txt"
    #dest_new_file = shutil.copy( new_file_path , os.path.join(os.getcwd(), "text_files"))
    new_file_name = os.path.split(new_file_path)[1]
    file_orig_path = os.path.split(new_file_path)[0]

    #Re-run the correlation
    file_list = glob.glob(os.path.join(file_orig_path, "*.txt"))
    corpus = []

    for file_path in file_list:
        head_tail = os.path.split(file_path)
        # print(head_tail[1])
        with open(file_path, encoding="utf8", errors='ignore') as f_input:
            corpus.append(f_input.read())

    doc_num = len(corpus)

    doc_ids = [os.path.split(file_path)[1] for file_path in file_list]
    vectorizer = TfidfVectorizer(token_pattern=r'(?u)\b[A-Za-z]+\b')
    tfidf = vectorizer.fit_transform(corpus)
    feature_names = vectorizer.get_feature_names()
    # no need to normalize, since Vectorizer will return normalized tf-idf
    pairwise_similarity = tfidf * tfidf.T
    psim_array = pairwise_similarity.toarray()
    df = pd.DataFrame(pairwise_similarity.toarray())
    df.index = doc_ids
    df.columns = doc_ids

    #From the correlation dataframe I select the row of the new file and compute the average
    new_file_mean = df.iloc[0:-1,-1].mean()

    # Delete the file from the folder
    os.remove(new_file_path)
    return new_file_mean


