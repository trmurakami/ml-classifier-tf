from nltk.corpus import stopwords
import pandas as pd
from sklearn.utils import shuffle
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
from keras_preprocessing.sequence import pad_sequences
import pickle
import json
import io
import nltk
nltk.download('stopwords')

stop_words = stopwords.words('english')
data = pd.read_csv(
    '/var/www/html/ml/py/data/Test_Scopus_SDG.tsv', delimiter='\t')
data['Data'] = data['Data'].apply(lambda x: ' '.join(
    [word for word in x.split() if word not in (stop_words)]))
texts = data['Data'].tolist()
labels = data['Label'].tolist()

tokenizer = keras.preprocessing.text.Tokenizer()
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)

print(sequences)
