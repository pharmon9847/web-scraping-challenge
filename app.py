# In[ ]:


from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

@app.route("/")
def index():
    
    
        scraped_facts = mongo.db.collection.find_one()
        
        # render index.html template and pass data retrieved from database
        return render_template("index.html", scraped_facts=scraped_facts)
    
@app.route("/scrape")
def scrape():
    # run scrape function
    news_facts = scrape_mars.scrape()
    
    # empty out collection
    mongo.db.collection.drop()
    
    # insert new record into collection
    mongo.db.collection.insert_one(news_facts)
    
    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)


# In[ ]:





# In[ ]:




