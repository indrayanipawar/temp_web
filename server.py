from flask import Flask, request, Response
import jsonpickle
import numpy as np
import cv2

import pickle
from pickle import dump, load
from keras.applications.inception_v3 import InceptionV3
from keras.preprocessing import image
from keras.models import Model, load_model
from keras.applications.inception_v3 import preprocess_input
from keras.preprocessing.sequence import pad_sequences
import urllib.request

app = Flask(__name__)

@app.route('/home', methods=['GET'])
def hom_fun():
    return "Hello...!!!"

@app.route('/api/test', methods=['POST'])
def test():
    r = request
    nparr = np.fromstring(r.data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    cv2.imwrite("temp.jpg", img)
    
    cap = generate_caption()

    response = {'caption': cap}
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")


# functions...!!!
def load_doc(filename):
	file = open(filename, 'r')
	text = file.read()
	file.close()
	return text

def load_set(filename):
	doc = load_doc(filename)
	dataset = list()
	for line in doc.split('\n'):
		if len(line) < 1:
			continue
		identifier = line.split('.')[0]
		dataset.append(identifier)
	return set(dataset)

def load_clean_descriptions(filename, dataset):
	doc = load_doc(filename)
	descriptions = dict()
	for line in doc.split('\n'):
		tokens = line.split()
		image_id, image_desc = tokens[0], tokens[1:]
		if image_id in dataset:
			if image_id not in descriptions:
				descriptions[image_id] = list()
			desc = 'startseq ' + ' '.join(image_desc) + ' endseq'
			descriptions[image_id].append(desc)
	return descriptions

def preprocess(image_path):
    img = image.load_img(image_path, target_size=(299, 299))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return x

def to_lines(descriptions):
	all_desc = list()
	for key in descriptions.keys():
		[all_desc.append(d) for d in descriptions[key]]
	return all_desc


def max_length(descriptions):
	lines = to_lines(descriptions)
	return max(len(d.split()) for d in lines)

def url_to_image (url):
  resp=urllib.request.urlopen (url)
  image=np.asarray (bytearray (resp.read ()), dtype="uint8")
  image=cv2.imdecode (image, cv2.IMREAD_COLOR)
  return image

def encode(image):
    image = preprocess(image) 
    fea_vec = model_encode_new.predict(image) 
    fea_vec = np.reshape(fea_vec, fea_vec.shape[1])
    return fea_vec

def greedySearch(photo):
    in_text = 'startseq'
    for i in range(max_length):
        sequence = [wordtoix[w] for w in in_text.split() if w in wordtoix]
        sequence = pad_sequences([sequence], maxlen=max_length)
        yhat = model.predict([photo,sequence], verbose=0)
        yhat = np.argmax(yhat)
        word = ixtoword[yhat]
        in_text += ' ' + word
        if word == 'endseq':
            break
    final = in_text.split()
    final = final[1:-1]
    final = ' '.join(final)
    return final

def encode(image):
    image = preprocess(image) 
    fea_vec = model_encode_new.predict(image) 
    fea_vec = np.reshape(fea_vec, fea_vec.shape[1])
    return fea_vec

def greedySearch(photo):
    in_text = 'startseq'
    for i in range(max_length):
        sequence = [wordtoix[w] for w in in_text.split() if w in wordtoix]
        sequence = pad_sequences([sequence], maxlen=max_length)
        yhat = model.predict([photo,sequence], verbose=0)
        yhat = np.argmax(yhat)
        word = ixtoword[yhat]
        in_text += ' ' + word
        if word == 'endseq':
            break
    final = in_text.split()
    final = final[1:-1]
    final = ' '.join(final)
    return final

def generate_caption():
    data = encode("temp.jpg")
    ret = greedySearch(data.reshape(1,2048))
    print(ret)
    return ret



# init...!!!!

filename = "Text_Files/Flickr30k.token.txt"
doc = load_doc(filename)
print(doc[:500])
filename = "Text_Files/Flickr_30k.trainImages.txt"
train = load_set(filename)
test = load_set("Text_Files/Flickr_30k.testImages.txt")
print('Dataset_testing: %d' % len(train))
print('Dataset_traning: %d' % len(test))
train_descriptions = load_clean_descriptions('descriptions30k.txt', train)
model_encode = InceptionV3(weights='imagenet')
model_encode_new = Model(model_encode.input, model_encode.layers[-2].output)
all_train_captions = []
for key, val in train_descriptions.items():
    for cap in val:
        all_train_captions.append(cap)
len(all_train_captions)
word_count_threshold = 10
word_counts = {}
nsents = 0
for sent in all_train_captions:
    nsents += 1
    for w in sent.split(' '):
        word_counts[w] = word_counts.get(w, 0) + 1
vocab = [w for w in word_counts if word_counts[w] >= word_count_threshold]
print('preprocessed words %d -> %d' % (len(word_counts), len(vocab)))
ixtoword = {}
wordtoix = {}

ix = 1
for w in vocab:
    wordtoix[w] = ix
    ixtoword[ix] = w
    ix += 1
vocab_size = len(ixtoword) + 1 
vocab_size
max_length = max_length(train_descriptions)
print('Description Length: %d' % max_length)
model = load_model("model_weights30k/model_1.h5")
model.load_weights('model_weights30k/model_30.h5')


app.run(host="0.0.0.0", port=5000)