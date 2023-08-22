import pandas as pd
import os
import pickle
import joblib
import re
import string
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from core.config import settings
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

class Predictor:

    wl = WordNetLemmatizer()

    def predict(self, input: [], keywords: str, version: str):

        wd = os.getcwd()

        model_path = wd + settings.MLMODEL_PATH + \
            '/' + version + '/'

        input[0] = self.cleantext(input[0], keywords)

        pred_prob1 = self.all_field_predict(input, model_path)

        pred_prob2 = self.text_only_prediction(input[0], model_path)

        avg_prob = sum([pred_prob1, pred_prob2]) / 2
        avg_prob_per = round((avg_prob*100), 2)

        return avg_prob_per

    # Text only prediction
    def text_only_prediction(self, input_text: str, model_path: str):
        with open(model_path + settings.MLMODEL_TEXTONLY_NAME, 'rb') as file:
            model_textonly = pickle.load(file)

        with open(model_path + settings.MLMODEL_TEXTONLY_VECTOR_NAME, 'rb') as file:
            model_textonly_vector = joblib.load(file)

        X_test = [input_text]

        X_vector = model_textonly_vector.transform(X_test)
        y_prob = model_textonly.predict_proba(X_vector)[:, 1]

        return y_prob[0]

    # All fields prediction
    def all_field_predict(self, input_list: [], model_path: str):
        with open(model_path + settings.MLMODEL_ALLFIELDS_NAME, 'rb') as file:
            model_allfields = pickle.load(file)

        with open(model_path + settings.MLMODEL_ALLFIELDS_VECTOR_NAME, 'rb') as file:
            model_allfields_vector = joblib.load(file)

        X_test = pd.DataFrame(columns=['clean_text', 'iso_language', 'species_name',
                                       'has_geo', 'source_name', 'source_country',
                                       'source_region', 'source_subject'])

        X_test.loc[0] = input_list

        X_test_encoded = model_allfields_vector.transform(X_test)

        y_prob = model_allfields.predict_proba(X_test_encoded)[:, 1]

        return y_prob[0]

    def preprocess(self, text):
        text = text.lower()
        text = text.strip()
        text = re.compile('<.*?>').sub('', text)
        text = re.compile('[%s]' % re.escape(
            string.punctuation)).sub(' ', text)
        text = re.sub('\s+', ' ', text)
        text = re.sub(r'\[[0-9]*\]', ' ', text)
        text = re.sub(r'[^\w\s]', '', str(text).lower().strip())
        text = re.sub(r'\d', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text

    def stopword(self, string):
        a = [i for i in string.split() if i not in stopwords.words('english')]
        return ' '.join(a)

    def get_wordnet_pos(self, tag):
        if tag.startswith('J'):
            return wordnet.ADJ
        elif tag.startswith('V'):
            return wordnet.VERB
        elif tag.startswith('N'):
            return wordnet.NOUN
        elif tag.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN

    def lemmatizer(self, string):
        word_pos_tags = nltk.pos_tag(word_tokenize(string))

        a = [self.wl.lemmatize(tag[0], self.get_wordnet_pos(tag[1])) for idx, tag in enumerate(
            word_pos_tags)]
        
        return " ".join(a)

    def finalpreprocess(self, string):
        return self.lemmatizer(self.stopword(self.preprocess(string)))

    def cleantext(self, title, keywords):
        clean_title = self.finalpreprocess(title)
        clean_keywords = self.finalpreprocess(keywords)
    
        list_merged = clean_title.split(' ') + clean_keywords.split(' ')
        clean_text = ' '.join(list(dict.fromkeys(list_merged)))

        clean_text = re.sub(r'[^\x00-\x7F]+', '', clean_text)

        return clean_text

predictor = Predictor()
