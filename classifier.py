"""
/**********************************************************************
* RoboTester Version 1.0
* PUBLICIS SAPIENT PROPRIETARY/CONFIDENTIAL
* Use is subject to Organization terms
* @author Varun Sharma,Ashok Yadav & Suraj Prakash
* @since version 1.0
************************************************************************/
"""

import re
import pandas as pd
from nltk.corpus import stopwords
from sklearn.datasets import load_files
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression


classifier = None
vectorizer = None


df = pd.read_excel(r"Regression.xlsx", sheet_name= "RunTest") # can index sheet by name 
mylist = df['Actions'].tolist()

# =============================================================================
# Load the training data for the classifier and store the train data in x and
# target(labels) values in y
# =============================================================================
reviews = load_files('Functionalties')
x,y = reviews.data , reviews.target

# =============================================================================
# data pre-processing to remove all the insignificant words from each string
# =============================================================================
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
#split the sample data into training set and test set
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
    testcase = [sen]
    testcase = vectorizer.transform(testcase).toarray()
    print(classifier.predict(testcase))