import nltk
import numpy as np
import re
import pickle
from nltk.corpus import stopwords
from sklearn.datasets import load_files


reviews = load_files('Functionalties')

x,y = reviews.data , reviews.target

with open('x.pickle','wb') as f:
    pickle.dump(x,f)
    
with open('y.pickle','wb') as f:
    pickle.dump(y,f)
    
corpus = []
for i in range(0, len(x)):
    review = re.sub(r'\W',' ',str(x[i]))
    review = review.lower()
    review = re.sub(r'\s+[a-z]\s+',' ',review)
    review = re.sub(r'^[a-z]\s+','', review)
    review = re.sub(r'\s+', ' ', review)
  
    corpus.append(review)
    
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(max_features=300, min_df=3,max_df=0.6,stop_words=stopwords.words('english'))
X=vectorizer.fit_transform(corpus).toarray()

from sklearn.model_selection import train_test_split
text_train,text_test,sent_train,sent_test=train_test_split(X,y,test_size=0.2,random_state=0)

from sklearn.ensemble import AdaBoostClassifier
from sklearn.linear_model import LogisticRegression
clf = LogisticRegression(random_state=0, solver='lbfgs',multi_class='multinomial').fit(X, y)
classifier = AdaBoostClassifier()
classifier.fit(text_train,sent_train)

with open('Tfidfmodel.pickle','wb') as f:
    pickle.dump(vectorizer,f)
    
#dumping the classifier
with open('classifier.pickle','wb') as f:
    pickle.dump(classifier,f)
