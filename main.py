from flask import Flask,render_template, redirect, url_for,request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_ckeditor import CKEditor, CKEditorField
from wtforms import StringField, SubmitField, FileField
from wtforms.fields.simple import EmailField, PasswordField
from wtforms.validators import DataRequired, URL,Email
import sqlite3
import pandas as pd
#from flask_login import UserMixin,LoginManager,login_user,logout_user,current_user
from werkzeug.security import generate_password_hash, check_password_hash
import random
import dill as pickle
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import operator
#nltk.download('stopwords')
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')
#nltk.download('wordnet')



#load models
with open('content_based.pkl' , 'rb') as f:
    contentB_recommend = pickle.load(f)

filtered_restaurant_df = pd.read_pickle('restaurants.pkl')

with open('constituents_list.pkl' , 'rb') as f:
    constituents_list = pd.read_pickle(f)

with open('prices.pkl' , 'rb') as f:
    price_map = pd.read_pickle(f)

with open('sentence_processor.pkl' , 'rb') as f:
    process_sentences = pickle.load(f)

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)


#create connection
conn = sqlite3.connect('restaurant_recommender.db')
cursor = conn.cursor()

#read from db table
df = pd.read_sql("SELECT * FROM restaurants", conn)
df['restaurant'] = df['name']

#default recommendations on home page
def default_recommendations(df):
    random_samples = df.sample(n = 10, replace = True)
    return random_samples

#random 4 cusines from db on search bar
def search_cuisines(df):
    cuisines = list(df['cuisine'])
    random_cusines = random.sample(cuisines, 4)
    return random_cusines

#random locations on search bar
def search_location(df):
    locations = ['Brooklyn', 'New York', 'Manhattan']
    return locations

#Registration form
class RegisterNewUserForm(FlaskForm):
    name=StringField('Name',validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField("Register")

#Login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

@app.route('/',methods = ["GET", "POST"])
def home():
    return render_template("index.html", recomms = default_recommendations(df), cuisines = search_cuisines(df), locations = search_location(df))

@app.route('/login',methods=['POST','GET'])
def login():
    form = LoginForm()
    if request.method =='POST':
        username = request.form.get('Username')
        password = request.form.get('Password')
    return render_template('login.html',form = form)

@app.route('/register',methods=['POST','GET'])
def register():
    form = RegisterNewUserForm()
    if request.method =='POST':
        username = request.form.get('Name')
        password = request.form.get('Password')
    return render_template('register.html', form = form)

@app.route('/view-restaurant/<int:rest_id>',methods=['GET','POST'])
def view_restaurant(rest_id):
    rest_index = rest_id
    for index, row in df.iterrows():
        if index == rest_index:
            name = df.at[index, 'restaurant']
            image = df.at[index, 'image']
            rating = df.at[index, 'rating']
            reviews = df.at[index, 'reviews']
            pricing = df.at[index, 'pricing']
            location = df.at[index, 'location']
            cuisine = df.at[index, 'cuisine']
    return render_template('restaurant.html', image = image,name = name, rating = rating, reviews = reviews, pricing = pricing, location = location, cuisine = cuisine)


@app.route('/recommendations',methods=['GET','POST'])
def show_recomms():
    r_df = pd.DataFrame(columns = df.columns)
    query = request.form['search']
    recomms = contentB_recommend(str(query))
    recomms['restaurant'] = recomms['name']

    #find match in db table
    for index, row in recomms.iterrows():
        name =  row.restaurant.title()
        for index, row in df.iterrows():
            if name == row.restaurant.title():
                r_df = r_df.append(row, ignore_index = False)
    return render_template('recommendations.html', recs_df = r_df)

@app.route('/specific-cuisine/<cuis>',methods=['GET','POST'])
def specific_cuisine(cuis):
    cuisine = cuis
    results = df.loc[df['cuisine'] == cuisine]
    return render_template('recommendations.html', recs_df = results)

@app.route('/specific-location/<loc>',methods=['GET','POST'])
def specific_location(loc):
    location = " ' " + loc
    results = df.loc[df['cuisine'] == location]
    return render_template('recommendations.html', recs_df = results)

if __name__ == "__main__":
    app.run(debug=True)



