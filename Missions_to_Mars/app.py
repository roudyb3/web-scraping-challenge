#import flask library
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# @TODO Initiatlize the FLASK
app = Flask(__name__)

# @TODO Add in the PyMongo app config
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# @TODO create a route to scrape the info and render it through Flask
collection = mongo.db.mars 

@app.route('/')
def index():
    mongo_dictionary = collection.find_one()
    print(mongo_dictionary)
    return render_template('index.html', mongo_dictionary = mongo_dictionary)

@app.route('/scrape')
def scraper():
    mongo_dictionary = scrape_mars.scrape()
    #print(mongo_dictionary)
    collection.update({}, mongo_dictionary, upsert = True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)