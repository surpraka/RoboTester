# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 10:38:16 2020

@author: surpraka
"""


import pandas as pd
import re
from nltk.corpus import stopwords
from sklearn.datasets import load_files
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

df = pd.read_excel(r"Regression.xlsx", sheet_name= "RunTest") # can index sheet by name 
mylist = df['Actions'].tolist()

# =============================================================================
# Read the scenario names as well for extent report beautification
# =============================================================================
sc = df['Scenario'].to_list()
scnames = [ a for a in sc if isinstance(a,str) ]
print(scnames)

reviews = load_files('Functionalties')
x,y = reviews.data , reviews.target

corpus = []
for i in range(0, len(x)):
    review = re.sub(r'\W',' ',str(x[i]))
    review = review.lower()
    review = re.sub(r'\s+[a-z]\s+',' ',review)
    review = re.sub(r'^[a-z]\s+','', review)
    review = re.sub(r'\s+', ' ', review)

    corpus.append(review)


# =============================================================================
# Initialize a tfidf vectorizer which converts a string into array of floating number 
# =============================================================================
vectorizer = TfidfVectorizer(max_features=100, min_df=3,max_df=0.8,stop_words=stopwords.words('english'))

# =============================================================================
# split the sample data into training set and test set
# =============================================================================
X_train, X_test, Y_train, Y_test = train_test_split(corpus, y, test_size=0.3, random_state=42)

# converts to array
X_train = vectorizer.fit_transform(X_train).toarray()
X_test = vectorizer.transform(X_test).toarray()

#initialize and train the model
classifier = LogisticRegression(random_state=42, solver='newton-cg', max_iter=1000, multi_class='multinomial', n_jobs=-1)
classifier.fit(X_train, Y_train)


sample = mylist

for sen in sample:
    print(sen)
    testcase = [sen]
    testcase = vectorizer.transform(testcase).toarray()
    print(classifier.predict(testcase))