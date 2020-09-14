# -*- coding: utf-8 -*-
"""spam_detector.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZGo7qmjiwrgmIyJcAUbkW54jy6U9lWoO
"""

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
df = pd.read_csv('/content/drive/My Drive/spam_detection/spam.csv')
df.head()

df.shape

df['Category'] = df['Label']
df['Message'] = df['EmailText']
df.head()

df = df.drop(['Label','EmailText'],axis=1)
df.groupby('Category').describe()

df['spam'] = df['Category'].apply(lambda x: 1 if x=='spam' else 0)
df.head()

import matplotlib.pyplot as plt
df['Category'].value_counts().plot(kind = 'pie', explode=[0,0.1], figsize=(6,6), autopct='%1.2f%%')
plt.ylabel('Ham vs Spam')
plt.legend(["Ham", "Spam"])
plt.show()

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(df.Message, df.spam, test_size=0.25)
from sklearn.utils import shuffle
X_train, y_train = shuffle(X_train, y_train)
X_test, y_test = shuffle(X_test, y_test)
X_train

from sklearn.feature_extraction.text import CountVectorizer
v = CountVectorizer()
X_train_count = v.fit_transform(X_train.values)
X_train_count.toarray()[:3]
X_train_count.shape

X = v.fit_transform(df['Message']).toarray()
X

from sklearn.naive_bayes import MultinomialNB
model = MultinomialNB()
model.fit(X_train_count, y_train)
X_test_count = v.transform(X_test)
y_pred = model.predict(X_test_count)

from sklearn.metrics import accuracy_score
score = accuracy_score(y_test, y_pred, normalize=True)
score*100

from sklearn.metrics import fbeta_score, classification_report
fbeta_score(y_test, y_pred, beta=0.5)

from sklearn.pipeline import Pipeline
clf = Pipeline([
    ('vectorizer', CountVectorizer()),
    ('nb', MultinomialNB())
])
clf.fit(X_train, y_train)
clf.score(X_test, y_test)

import pickle
saved_model = pickle.dumps(model)
modelfrom_pickle = pickle.loads(saved_model)
y_pred = modelfrom_pickle.predict(X_test_count)
accuracy_score(y_test, y_pred)

import joblib
joblib.dump(model, 'spam_detector')