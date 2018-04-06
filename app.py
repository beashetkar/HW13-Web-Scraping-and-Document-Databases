# coding: utf-8

# Import necessary libraries
from flask import Flask, render_template, jsonify, redirect
import pymongo
import scrape_mars

app = Flask(__name__)

conn ="mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.mars

@app.route('/')
def index():
    mars = list(db.mars.find())[0]
    return render_template('index.html', mars = mars)

@app.route('/scrape')
def scrape():
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    db = client.mars
    db.mars.delete_many({})
    db.mars.insert_one(scrape())
    mars = list(db.mars.find())[0]    
    return render_template("index.html", mars = mars)

if __name__=="__main__":
    app.run()    




