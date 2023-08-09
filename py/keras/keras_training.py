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
import numpy
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
stop_words = stopwords.words('portuguese')

data = pd.read_csv(
    '/var/www/html/biblioml/py/data/Assuntos.tsv', delimiter='\t')
data['Data'] = data['Data'].apply(lambda x: ' '.join(
    [word for word in x.split() if word not in (stop_words)]))
texts = data['Data'].tolist()
labels = data['Label'].tolist()

# texts, labels = shuffle(texts, labels, random_state=42)

tokenizer = keras.preprocessing.text.Tokenizer()
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)

with open('tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

tokenizer_json = tokenizer.word_index
with io.open('tokenizer_dictionary.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(tokenizer_json, ensure_ascii=False))


max_sequence_length = 350

sequences_padded = pad_sequences(sequences, maxlen=max_sequence_length)

# vocab_size = len(tokenizer.word_index) + 1

vocab_size = 15000

label_encoder = LabelEncoder()
encoded_labels = label_encoder.fit_transform(labels)
num_classes = len(label_encoder.classes_)

# Converta o LabelEncoder em um dicionário
label_encoder_dict = {label: index for index,
                      label in enumerate(label_encoder.classes_)}

# Salve o dicionário em um arquivo JSON
with open('label_encoder.json', 'w') as file:
    json.dump(label_encoder_dict, file)

X_train, X_test, y_train, y_test = train_test_split(
    sequences_padded, encoded_labels, test_size=0.2, random_state=42)

model = keras.Sequential()
model.add(keras.layers.Embedding(vocab_size, 64,
                                 input_length=max_sequence_length, mask_zero=True))
model.add(keras.layers.LSTM(350, dropout=0.2, recurrent_dropout=0.2))
model.add(keras.layers.Dense(num_classes, activation='softmax'))

model.compile(loss='sparse_categorical_crossentropy',
              optimizer='adam', metrics=['accuracy'])
model.fit(X_train, y_train, batch_size=350, epochs=15,
          validation_data=(X_test, y_test), verbose=1, shuffle=True,
          use_multiprocessing=True, workers=8)

loss, accuracy = model.evaluate(X_test, y_test)
print(f"Loss: {loss:.4f}, Accuracy: {accuracy:.4f}")

# model.save('model_text_classifier.keras')
tf.keras.saving.save_model(
    model, 'model_text_classifier.keras', overwrite=True)

predictions = model.predict(X_test)
y_pred = predictions.argmax(axis=1)
y_test = y_test.astype('int')
print(y_pred)
print(y_test)
print(label_encoder.inverse_transform(y_pred))
print(label_encoder.inverse_transform(y_test))
