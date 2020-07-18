from sklearn.feature_extraction.text import TfidfVectorizer
import os
import glob
import numpy as np
import pandas as pd
from project.models import DocumentSample


def check_doc_with_class(upload_folder):
    documents = DocumentSample.query.all()
    distinct_class = []
    for document in documents:
        if document.doc_class not in distinct_class:
            distinct_class.append(document.doc_class)

    corpus_base = []
    corpus_keys = []
    df_correlation = pd.DataFrame(columns=['Class', 'Base Similarity', 'Similarity to new file'])

    for class_value in distinct_class:
        filter_data = DocumentSample.query.filter_by(doc_class=class_value)
        for item in filter_data:
            corpus_base.append(item.doc_content)
            corpus_keys.append(item.doc_name)
        vectorizer = TfidfVectorizer(token_pattern=r'(?u)\b[A-Za-z]+\b')
        tfidf = vectorizer.fit_transform(corpus_base)
        pairwise_similarity = tfidf * tfidf.T
        df = pd.DataFrame(pairwise_similarity.toarray())
        avg_correlation = df.values[np.triu_indices_from(df.values, 1)].mean()
        file_list = glob.glob(os.path.join(upload_folder, "*.txt"))
        for sing_file in file_list:
            with open(sing_file, encoding="utf8", errors='ignore') as f_input:
                corpus_base.append(f_input.read())
        tfidf = vectorizer.fit_transform(corpus_base)
        pairwise_similarity = tfidf * tfidf.T
        df = pd.DataFrame(pairwise_similarity.toarray())
        new_file_mean = df.iloc[0:-1, -1].mean()
        new_entry = {'Class': class_value, 'Base Similarity': avg_correlation, 'Similarity to new file': new_file_mean}
        df_correlation = df_correlation.append(new_entry, ignore_index=True)
        corpus_base = []

    df_correlation['Difference'] = abs(df_correlation['Base Similarity'] - df_correlation['Similarity to new file'])
    most_correlated_class = df_correlation.iloc[int(df_correlation[['Difference']].idxmin()),0]
    return df_correlation,most_correlated_class






