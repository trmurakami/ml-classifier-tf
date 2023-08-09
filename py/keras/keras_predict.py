import sys
import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from tensorflow import keras
from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences
import pickle
from pathlib import Path
path_file = Path(sys.path[0])
print(path_file)

labels = ['SDG01', 'SDG02', 'SDG03', 'SDG04',
          'SDG05', 'SDG06', 'SDG07', 'SDG08',
          'SDG09', 'SDG10', 'SDG11', 'SDG12',
          'SDG13', 'SDG14', 'SDG15', 'SDG16',
          'SDG17']

# Carregar o modelo tokenizador
with open(path_file / 'tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

# Carregar o modelo treinado
model = load_model(path_file / 'model_text_classifier.keras')

# Tamanho máximo das sequências (ajuste conforme necessário)
max_sequence_length = 350

# Converter as etiquetas em números (opcional, dependendo do formato das etiquetas)

label_encoder = LabelEncoder()
encoded_labels = label_encoder.fit_transform(labels)
num_classes = len(label_encoder.classes_)

query_texts = [sys.argv[1]]
sequences = tokenizer.texts_to_sequences(query_texts)
sequences_padded = pad_sequences(sequences, maxlen=max_sequence_length)

prediction = model.predict(sequences_padded)
# print(prediction)
print(label_encoder.inverse_transform(prediction.argmax(axis=1))[0])
