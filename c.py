import sqlite3
import pandas as pd
import random
import dill as pickle


#create connection
conn = sqlite3.connect('restaurant_recommender.db')
cursor = conn.cursor()

#read from db table
df = pd.read_sql("SELECT * FROM restaurants", conn)
df['restaurant'] = df['name']

def default_recommendations(df):
    random_samples = df.sample(n = 10, replace = True)
    return random_samples


def search_location(df):
    locations = list(set(df['location']))
    random_locations = random.sample(locations, 4)
    return random_locations

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

def show_recomms(words):
    query = words
    recomms = hybrid_recommender(0,query)
    return recomms

print(show_recomms('tacos in Brooklyn'))
print(filtered_restaurant_df)
print('y')