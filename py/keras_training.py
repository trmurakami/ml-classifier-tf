import os
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
from keras.callbacks import TensorBoard
stop_words = ["de", "a", "o", "que", "e", "do", "da", "em", "um", "para", "é", "com", "não", "uma", "os", "no", "se", "na", "por", "mais", "as", "dos", "como", "mas", "foi",
              "ao", "ele", "das", "tem", "à", "seu", "sua", "ou", "ser", "quando", "muito", "há", "nos", "já", "está", "eu", "também", "só", "pelo", "pela", "até", "isso",
              "ela", "entre", "era", "depois", "sem", "mesmo", "aos", "ter", "seus", "quem", "nas", "me", "esse", "eles", "estão", "você", "tinha", "foram", "essa", "num",
              "nem", "suas", "meu", "às", "minha", "têm", "numa", "pelos", "elas", "havia", "seja", "qual", "será", "nós", "tenho", "lhe", "deles", "essas", "esses", "pelas",
              "este", "fosse", "dele", "tu", "te", "vocês", "vos", "lhes", "meus", "minhas", "teu", "tua", "teus", "tuas", "nosso", "nossa", "nossos", "nossas", "dela",
              "delas", "esta", "estes", "estas", "aquele", "aquela", "aqueles", "aquelas", "isto", "aquilo", "estou", "está", "estamos", "estão", "estive", "esteve",
              "estivemos", "estiveram", "estava", "estávamos", "estavam", "estivera", "estivéramos", "esteja", "estejamos", "estejam", "estivesse", "estivéssemos",
              "estivessem", "estiver", "estivermos", "estiverem", "hei", "há", "havemos", "hão", "houve", "houvemos", "houveram", "houvera", "houvéramos", "haja", "hajamos",
              "hajam", "houvesse", "houvéssemos", "houvessem", "houver", "houvermos", "houverem", "houverei", "houverá", "houveremos", "houverão", "houveria", "houveríamos",
              "houveriam", "sou", "somos", "são", "era", "éramos", "eram", "fui", "foi", "fomos", "foram", "fora", "fôramos", "seja", "sejamos", "sejam", "fosse", "fôssemos",
              "fossem", "for", "formos", "forem", "serei", "será", "seremos", "serão", "seria", "seríamos", "seriam", "tenho", "tem", "temos", "tém", "tinha", "tínhamos",
              "tinham", "tive", "teve", "tivemos", "tiveram", "tivera", "tivéramos", "tenha", "tenhamos", "tenham", "tivesse", "tivéssemos", "tivessem", "tiver", "tivermos", "tiverem", "terei", "terá", "teremos", "terão", "teria", "teríamos",
              "teriam", "DE", "A", "O", "QUE", "E", "DO", "DA", "EM", "UM", "PARA", "É", "COM", "NÃO", "UMA", "OS", "NO", "SE", "NA", "POR", "MAIS", "AS", "DOS", "COMO",
              "MAS", "FOI", "AO", "ELE", "DAS", "TEM", "À", "SEU", "SUA", "OU", "SER", "QUANDO", "MUITO", "HÁ", "NOS", "JÁ", "ESTÁ", "EU", "TAMBÉM", "SÓ", "PELO", "PELA",
              "ATÉ", "ISSO", "ELA", "ENTRE", "ERA", "DEPOIS", "SEM", "MESMO", "AOS", "TER", "SEUS", "QUEM", "NAS", "ME", "ESSE", "ELES", "ESTÃO", "VOCÊ", "TINHA", "FORAM",
              "ESSA", "NUM", "NEM", "SUAS", "MEU", "ÀS", "MINHA", "TÊM", "NUMA", "PELOS", "ELAS", "HAVIA", "SEJA", "QUAL", "SERÁ", "NÓS", "TENHO", "LHE", "DELES", "ESSAS",
              "ESSES", "PELAS", "ESTE", "FOSSE", "DELE", "TU", "TE", "VOCÊS", "VOS", "LHES", "MEUS", "MINHAS", "TEU", "TUA", "TEUS", "TUAS", "NOSSO", "NOSSA", "NOSSOS",
              "NOSSAS", "DELA", "DELAS", "ESTA", "ESTES", "ESTAS", "AQUELE", "AQUELA", "AQUELES", "AQUELAS", "ISTO", "AQUILO", "ESTOU", "ESTÁ", "ESTAMOS", "ESTÃO", "ESTIVE",
              "ESTEVE", "ESTIVEMOS", "ESTIVERAM", "ESTAVA", "ESTÁVAMOS", "ESTAVAM", "ESTIVERA", "ESTIVÉRAMOS", "ESTEJA", "ESTEJAMOS", "ESTEJAM", "ESTIVESSE", "ESTIVÉSSEMOS",
              "ESTIVESSEM", "ESTIVER", "ESTIVERMOS", "ESTIVEREM", "HEI", "HÁ", "HAVEMOS", "HÃO", "HOUVE", "HOUVEMOS", "HOUVERAM", "HOUVERA", "HOUVÉRAMOS", "HAJA", "HAJAMOS",
              "HAJAM", "HOUVESSE", "HOUVÉSSEMOS", "HOUVESSEM", "HOUVER", "HOUVERMOS", "HOUVEREM", "HOUVEREI", "HOUVERÁ", "HOUVEREMOS", "HOUVERÃO", "HOUVERIA", "HOUVERÍAMOS",
              "HOUVERIAM", "SOU", "SOMOS", "SÃO", "ERA", "ÉRAMOS", "ERAM", "FUI", "FOI", "FOMOS", "FORAM", "FORA", "FÔRAMOS", "SEJA", "SEJAMOS", "SEJAM", "FOSSE", "FÔSSEMOS",
              "FOSSEM", "FOR", "FORMOS", "FOREM", "SEREI", "SERÁ", "SEREMOS", "SERÃO", "SERIA", "SERÍAMOS", "SERIAM", "TENHO", "TEM", "TEMOS", "TÉM", "TINHA", "TÍNHAMOS",
              "TINHAM", "TIVE", "TEVE", "TIVEMOS", "TIVERAM", "TIVERA", "TIVÉRAMOS", "TENHA", "TENHAMOS", "TENHAM", "TIVESSE", "TIVÉSSEMOS", "TIVESSEM", "TIVER", "TIVERMOS",
              "TIVEREM", "TEREI", "TERÁ", "TEREMOS", "TERÃO", "TERIA", "TERÍAMOS", "TERIAM"]

# Delete all previous created files
# checking if file exist or not
if (os.path.isfile("gen_helpers/tokenizer.pickle")):
    os.remove("gen_helpers/tokenizer.pickle")
    print("File Deleted successfully")
else:
    print("File does not exist")

if (os.path.isfile("gen_helpers/tokenizer_dictionary.json")):
    os.remove("gen_helpers/tokenizer_dictionary.json")
    print("File Deleted successfully")
else:
    print("File does not exist")

if (os.path.isfile("gen_helpers/label_encoder.json")):
    os.remove("gen_helpers/label_encoder.json")
    print("File Deleted successfully")
else:
    print("File does not exist")

if (os.path.isfile("gen_helpers/model_text_classifier.keras")):
    os.remove("gen_helpers/model_text_classifier.keras")
    print("File Deleted successfully")
else:
    print("File does not exist")

# Delete all files in logs train folder
folder = 'logs/train'
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)

    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

# Delete all files in logs validation folder
folder = 'logs/validation'
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)

    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))


# replace_terms_with_no_spaces: replaces terms with no spaces with terms with spaces
# text: the text to replace terms in
# terms: list of terms to replace
# returns: the text with the terms replaced

def replace_terms_with_no_spaces(text, terms):
    for term in terms:
        term_without_spaces = term.replace(" ", "")
        text = text.replace(term, term_without_spaces)
    return text


# Ler termos compostos de um arquivo
with open("data/termos.txt", "r") as file:
    compound_terms = [line.strip() for line in file]

# Ordenar os termos compostos por tamanho de string
compound_terms.sort(key=len, reverse=True)


# Read data
data = pd.read_csv(
    'data/ProdmaisPPGCI.tsv', delimiter='\t')
# lowercase
data['Data'] = data['Data'].apply(lambda x: x.lower())
# converter termos compostos
data['Data'] = data['Data'].apply(
    lambda x: replace_terms_with_no_spaces(x, compound_terms))
data['Data'] = data['Data'].apply(lambda x: ' '.join(
    [word for word in x.split() if word not in (stop_words)]))
texts = data['Data'].tolist()
labels = data['Label'].tolist()

# texts, labels = shuffle(texts, labels, random_state=42)

# Create a tokenizer
tokenizer = keras.preprocessing.text.Tokenizer()

# Build the word index
tokenizer.fit_on_texts(texts)

# Turn strings into lists of integer indices
sequences = tokenizer.texts_to_sequences(texts)

with open('gen_helpers/tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

tokenizer_json = tokenizer.word_index
with io.open('gen_helpers/tokenizer_dictionary.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(tokenizer_json, ensure_ascii=False))


max_sequence_length = 256

# Sequences is a list of lists of integers
# sequences_padded is a list of lists of integers
#   Each list of integers is the input to a neural network
#   Each list is a different length
#   Each list has been padded with 0s to be the same length
sequences_padded = pad_sequences(sequences, maxlen=max_sequence_length)

# vocab_size = len(tokenizer.word_index) + 1

vocab_size = 8000

# Encode labels with value between 0 and n_classes-1
label_encoder = LabelEncoder()
# Fit label encoder and return encoded labels
encoded_labels = label_encoder.fit_transform(labels)
# Return number of unique classes
num_classes = len(label_encoder.classes_)

# Converta o LabelEncoder em um dicionário
label_encoder_dict = {label: index for index,
                      label in enumerate(label_encoder.classes_)}

# Salve o dicionário em um arquivo JSON
with open('gen_helpers/label_encoder.json', 'w') as file:
    json.dump(label_encoder_dict, file)

# This code creates a model that takes in the sequences and encoded_labels and trains the model on the training data.
# The model is then evaluated on the testing data.

# Split the dataset into training and test dataset
X_train, X_test, y_train, y_test = train_test_split(
    sequences_padded, encoded_labels, test_size=0.2, random_state=42)

# Build the model
model = keras.Sequential()
model.add(keras.layers.Embedding(vocab_size, 64,
          input_length=max_sequence_length, mask_zero=True))
model.add(keras.layers.LSTM(256, dropout=0.2,
          recurrent_dropout=0.2, return_sequences=True))
model.add(keras.layers.GlobalMaxPooling1D())
model.add(keras.layers.Dense(num_classes, activation='softmax'))
model.add(keras.layers.Dropout(0.2))


# Configure o callback TensorBoard
tensorboard_callback = TensorBoard(log_dir='./logs', histogram_freq=1)

# Compile the model
model.compile(loss='sparse_categorical_crossentropy',
              optimizer='adam', metrics=['accuracy'])

# Fit the model
model.fit(X_train, y_train, batch_size=256, epochs=30,
          validation_data=(X_test, y_test), verbose=1, shuffle=True, callbacks=[tensorboard_callback])

# Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Loss: {loss:.4f}, Accuracy: {accuracy:.4f}")

# model.save('model_text_classifier.keras')
tf.keras.saving.save_model(
    model, 'gen_helpers/model_text_classifier.keras', overwrite=True)

# Make predictions for the test data
predictions = model.predict(X_test)

# Get the index of the largest probability
y_pred = predictions.argmax(axis=1)

# Convert to int
y_test = y_test.astype('int')

# Print the predictions
print(y_pred)
print(y_test)

# Convert the predictions into the actual class names
print(label_encoder.inverse_transform(y_pred))
print(label_encoder.inverse_transform(y_test))
