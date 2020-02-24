{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [
    {
     "ename": "NameError",
     "evalue": "name 'null' is not defined",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mNameError\u001b[0m                                 Traceback (most recent call last)",
      "\u001b[0;32m<ipython-input-3-20c1b6db6ade>\u001b[0m in \u001b[0;36m<module>\u001b[0;34m\u001b[0m\n\u001b[1;32m      1\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0mflask\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mFlask\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mrender_template\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mredirect\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      2\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0mflask_pymongo\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mPyMongo\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m----> 3\u001b[0;31m \u001b[0;32mimport\u001b[0m \u001b[0mscrape_mars\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m      4\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      5\u001b[0m \u001b[0mapp\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mFlask\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0m__name__\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;32m~/Desktop/unc-data-homework/web-scraping-challenge/scrape_mars.py\u001b[0m in \u001b[0;36m<module>\u001b[0;34m\u001b[0m\n\u001b[1;32m    196\u001b[0m   {\n\u001b[1;32m    197\u001b[0m    \u001b[0;34m\"cell_type\"\u001b[0m\u001b[0;34m:\u001b[0m \u001b[0;34m\"code\"\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 198\u001b[0;31m    \u001b[0;34m\"execution_count\"\u001b[0m\u001b[0;34m:\u001b[0m \u001b[0mnull\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    199\u001b[0m    \u001b[0;34m\"metadata\"\u001b[0m\u001b[0;34m:\u001b[0m \u001b[0;34m{\u001b[0m\u001b[0;34m}\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    200\u001b[0m    \u001b[0;34m\"outputs\"\u001b[0m\u001b[0;34m:\u001b[0m \u001b[0;34m[\u001b[0m\u001b[0;34m]\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;31mNameError\u001b[0m: name 'null' is not defined"
     ]
    }
   ],
   "source": [
    "from flask import Flask, render_template, redirect\n",
    "from flask_pymongo import PyMongo\n",
    "import scrape_mars\n",
    "\n",
    "app = Flask(__name__)\n",
    "\n",
    "# use flask_pymongo to set up mongo connection\n",
    "app.config[\"MONGO_URI\"] = \"mongodb://localhost:27017/marsdb\"\n",
    "mongo = PyMongo(app)\n",
    "\n",
    "@app.route(\"/\")\n",
    "def index():\n",
    "    \n",
    "    \n",
    "        scraped_facts = mongo.db.collection.find_one()\n",
    "        \n",
    "        # render index.html template and pass data retrieved from database\n",
    "        return render_template(\"index.html\", scraped_facts=scraped_facts)\n",
    "    \n",
    "@app.route(\"/scrape\")\n",
    "def scraper():\n",
    "    # run scrape function\n",
    "    news_facts = scrape_mars.scrape()\n",
    "    \n",
    "    # empty out collection\n",
    "    mongo.db.collection.drop()\n",
    "    \n",
    "    # insert new record into collection\n",
    "    mongo.db.colection.insert_one(news_facts)\n",
    "    \n",
    "    return redirect(\"http://localhost:5000/\", code=302)\n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "    app.run(debug=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.9"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
