import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
import pyodbc
import sqlite3


#csv with restaurant data
df = pd.read_csv('db_data/restaurant_data1.csv')

#cleaning the data
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))
def process_sentences(text):
    temp_sent =[]

    # Tokenize words
    words = nltk.word_tokenize(text)

    # Lemmatize each of the words based on their position in the sentence
    tags = nltk.pos_tag(words)
    for i, word in enumerate(words):
        # only verbs
        if tags[i][1] in ('VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'):
            lemmatized = lemmatizer.lemmatize(word, 'v')
        else:
            lemmatized = lemmatizer.lemmatize(word)
        
        # Remove stop words and non alphabet tokens
        if lemmatized not in stop_words and lemmatized.isalpha(): 
            temp_sent.append(lemmatized)

    # Some other clean-up
    full_sentence = ' '.join(temp_sent)
    full_sentence = full_sentence.replace("n't", " not")
    full_sentence = full_sentence.replace("'m", " am")
    full_sentence = full_sentence.replace("'s", " is")
    full_sentence = full_sentence.replace("'re", " are")
    full_sentence = full_sentence.replace("'ll", " will")
    full_sentence = full_sentence.replace("'ve", " have")
    full_sentence = full_sentence.replace("'d", " would")
    return full_sentence

df['reviews'] = df['Reviews'].apply(lambda x: process_sentences(x))
df['Location'] = df['Location'].apply(lambda x: x.split(',')[1].strip())
df.rename(columns = {'Number of Reviews': 'n_reviews'}, inplace = True)

df = df.drop(['Reviews', 'Review Count'], axis = 1)

#saving the new csv
df.to_csv('db_data/restaurants.csv', index = False)


#connect to sql server
sqliteConnection = sqlite3.connect('restaurant_recommender.db')
cursor = sqliteConnection.cursor()

# Create Table
cursor.execute('''
		CREATE TABLE IF NOT EXISTS restaurants (
        
			name TEXT,
			rating int,
            pricing nvarchar(50),
            location nvarchar(50),
            cuisine nvarchar(50),
            number_of_reviews int,
            reviews TEXT,
            image TEXT)''')
sqliteConnection.commit()
#new df
df = pd.read_csv('db_data/restaurants.csv')

# Insert DataFrame to Table
for row in df.itertuples():
    cursor.execute("""
         INSERT INTO restaurants (name, rating, pricing, location, cuisine, number_of_reviews, reviews, image)
                VALUES (?,?,?,?,?,?,?,?)""",
                (row.Name,
                row.Rating,
                row.Pricing,
                row.Location,
                row.Cuisine,
                row.n_reviews,
                row.reviews,
                row.image_url))
               
sqliteConnection.commit()

