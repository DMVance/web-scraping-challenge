
from flask import Flask, render_template, abort
from scrape_mars import scrape, get_mongo_dict

app = Flask(__name__)

@app.errorhandler(500)
def page_not_found(e):
    # note that we set the 500 status explicitly
    return render_template('500.html', e=e), 500

@app.route("/")
def index():
    mongo_dict = get_mongo_dict()
    if not mongo_dict:
        abort(500, description="Scrape found no results. Please try again.")
    return render_template("index.html", mongo_dict=mongo_dict)

@app.route("/scraper")
def scraper():
    mars_dict = scrape()
    return render_template("scraper.html", mars_dict=mars_dict)


if __name__ == "__main__":
    app.run(debug=True)