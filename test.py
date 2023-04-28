import sqlite3
import pandas as pd
import random
import dill as pickle
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import operator
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

#create connection
conn = sqlite3.connect('restaurant_recommender.db')
cursor = conn.cursor()

#read from db table
df = pd.read_sql("SELECT * FROM restaurants", conn)
df['restaurant'] = df['name']

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

with open('content_base_r.pkl' , 'rb') as f:
    contentB_recommend = pickle.load(f)

with open('model_pkl' , 'rb') as f:
    hybrid_recommender = pickle.load(f)

with open('restaurants.pkl' , 'rb') as f:
    filtered_restaurant_df = pd.read_pickle(f)

with open('sentence_processor.pkl' , 'rb') as f:
    process_sentences = pickle.load(f)
    
with open('wards.pkl' , 'rb') as f:
    constituents_list = pickle.load(f)

with open('prices.pkl' , 'rb') as f:
    price_map = pickle.load(f)

pd.read_pickle('restaurants.pkl')
def show_recomms(words):
    query = words
    recomms = contentB_recommend(query)
    return recomms

print(show_recomms('tacos in Brooklyn'))
pd.read_pickle('restaurants.pkl')

