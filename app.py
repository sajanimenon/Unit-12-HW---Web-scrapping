from flask import Flask, render_template, redirect
import pymongo
import scrape_mars
#create an instancde of flask
app = Flask(__name__)
#use PyMongo to establish Mongo connection
conn = "mongodb://localhost:27017/mission_to_mars"
client = pymongo.MongoClient(conn)
# Route to render index.html template using data from Mongo
@app.route("/")
def home():
   mars = client.db.mars.find_one()
   return render_template("index.html", mars=mars)
@app.route("/scrape")
def scrape():
   mars = client.db.mars
   mars_data = scrape_mars.scrape()
   mars.update({}, mars_data, upsert=True)
   return redirect ("/", code=302)
if __name__ == "__main__":
   app.run(debug=True)
