# import dependencies
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scrape_mars
#for grader?
try:
    import config

    print("Running on MongoDB Atlas")
    conn = config.db_string
except ImportError:
    print("Running on local")
    conn = 'mongodb://localhost:27017'



#Initiating the flask app
app = Flask(__name__)
# Use flask_pymongo to set up mongo connection ( one way to do it...)
app.config["MONGO_URI"] = conn
mongo = PyMongo(app)
# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape_all()
    mars.update({}, mars_data, upsert=True)
    return redirect('/', code=302)

if __name__ == "__main__":
    app.run(debug=True)