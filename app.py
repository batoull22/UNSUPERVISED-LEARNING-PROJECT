
import pandas as pd
import numpy as np
from flask import Flask,render_template,request
import pickle
import re 
import flask
from sklearn.feature_extraction.text import TfidfVectorizer



stopwords_ = pd.read_csv("data/stopword.csv")
stop_ls=stopwords_['0'].tolist()

def clean_text(text):
    # remove all tashkeel
    
    text = re.sub("[ًٌٍَُِّّْْٰۡۨـٖۗۗۖ]", "", text)
    #remove URLs
    text = re.sub(r"http\S+", "", text,flags=re.U)    

    # Remove user @ references and '#' from tweet
    text = re.sub(r'\@\w+|\#\w+','', text)
    text = re.sub("\n", " ", text)
    text = re.sub("[^ضصثقفغعهخحجدطكمنتالبيسشئءؤرلاىةوزظٱإأآذ]", " ", text)
    text = re.sub("سكس", " ", re.sub("نيك", " ", re.sub("قحبه", " ", re.sub("فحل", " ", re.sub("ديوث", " ", text)))))
    text = re.sub(' +', ' ', text)  # removing unnecessary spaces

    return text.strip()

def remove_repeated_letters(text):
    
    text = re.sub(r'(.)\1+', r'\1\1', text)  
   # text = re.sub(r'(.)\1+', r'\1', text) 

    return text

def correct(text):

    text = re.sub(" ف ", " في ", text)
    text = re.sub(" ع ", " على ", text)

    return text

def simplify(text):

    text = re.sub("[أإٱآ]", "ا", text)
    text = re.sub("ة", "ه", text)

    return text

def remove_stopwords(text):
     #Read a csv file containing 750 stopwords 
    stopwords = pd.read_csv("Data/Arabic-Stopword.csv")
    stop=stopwords['text'].tolist()

    text_list = text.split(' ')  # to remove stopwords easily  
    new_text_list = []
   
    for s in text_list:
        if not (s in stop) and not(s in stop_ls): #Checks two lists
            new_text_list.append(s)
        
    text = ' '.join(e for e in new_text_list)  # gather text together again

    return text
    
def preprocess_text(text):
    # clean text
    text = clean_text(text)
  
    # remove repeated letters
    text = remove_repeated_letters(text)

    # correct misspelling
    text = correct(text)
   
    # simplify
    text = simplify(text)
  
    # remove stopwords
    text = remove_stopwords(text)

    return text





app = Flask(__name__) #Initialize the flask App

model = pickle.load(open('model.pkl', 'rb')) # loading the trained model
vectorizer = pickle.load(open("vectorizer.pickle", "rb"))


@app.route('/') # Homepage
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])

def predict():
    if request.method == 'POST':
        usr_input = str(request.form.get('usr'))
        tweet=preprocess_text(usr_input)
        print(tweet)
        data = [tweet]
        vect = vectorizer.transform(data).toarray()
        label = model.predict(vect)
        print(label)
    
        
        return render_template('index.html',val=label[0])
    return render_template('index.html')

 
if __name__ == "__main__":
    app.run(debug=True)
    