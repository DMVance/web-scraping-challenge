
from flask import Flask, render_template
from scrape_mars import scrape, get_mongo_dict

app = Flask(__name__)

@app.route("/")
def index():
    mongo_dict = get_mongo_dict()
    return render_template("index.html", mongo_dict=mongo_dict)

@app.route("/scraper")
def scraper():
    mars_dict = scrape()
    return render_template("scraper.html", mars_dict=mars_dict)


if __name__ == "__main__":
    app.run(debug=True)