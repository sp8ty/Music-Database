"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

import requests
import urllib.request
from urllib.parse import urljoin
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app


@app.route('/')
def index():
    """Renders a sample page."""
    return render_template("index.html")

@app.route("/search", methods=["GET", "POST"])
def search():
    '''Display search results'''

    if request.method == "GET":
        return render_template("/search.html")

    else:
        # initialise the variable with the users input
        search = request.form.get("search")

        # Authorization header to be embedded into the url
        headers = {
            'Authorization': 'Discogs token=mqjXUBBzjnqrjUkKFIrOPAmlEZsGoDXjkRZgnRIR'
        }

        # search the databse
        response = requests.get("https://api.discogs.com/database/search?q=%s&{?type=all}" % search, headers=headers)

        # return query into a JSON list variable
        query = response.json()

        # filtering out useful data
        data = query["results"]

        return render_template("search.html", data=data)

@app.route('/artist', methods=["GET", "POST"])
def artist():
    """Renders an artists page."""

    if request.method == "GET":
        return render_template("/artist.html")

    else:
        # initialise the variables from the hidden html form input
        type = request.form.get("type")
        id = request.form.get("id")
        thumb = request.form.get("thumb")

        # Authorization header to be embedded into the url 
        headers = {
        'Authorization': 'Discogs token=mqjXUBBzjnqrjUkKFIrOPAmlEZsGoDXjkRZgnRIR'
        }

        # search the database for artist information
        artists = requests.get("https://api.discogs.com/artists/%s" % id, headers=headers)

        artist = artists.json()
        #sites = artist["urls"]
        #namevar = artist["namevariations"]

        # search the database for artists releases
        releases = requests.get("https://api.discogs.com/artists/%s/releases?per_page=100" % id, headers=headers)

        release = releases.json()
        data = release["releases"]
        pagination = release["pagination"]
        pages = pagination["pages"]
        page = pagination["page"]
        

        return render_template("/artist.html",artist=artist, data=data, artistThumb=thumb,)




if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
