
import requests
import urllib.request

from urllib.parse import urlparse, parse_qs
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from helpers import get_yt_video_id

# Configure application
app = Flask(__name__)

#custom functions
app.jinja_env.globals.update(get_yt_video_id=get_yt_video_id)

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


        # set variable if user is selecting pagination
        goto = request.form.get("goto")

        # Authorization header to be embedded into the url
        headers = {
            'Authorization': 'Discogs token=mqjXUBBzjnqrjUkKFIrOPAmlEZsGoDXjkRZgnRIR'
        }

        if goto == None:
            # search the databse
            response = requests.get("https://api.discogs.com/database/search?q=%s&{?type=all}" % search, headers=headers)

            # return query into a JSON list variable
            query = response.json()

            # retreiving useful data
            data = query["results"]
            pagination = query["pagination"]
            pages = pagination["pages"]
            page = pagination["page"]

            return render_template("search.html", data=data, pagination=pagination, pages=pages, page=page)

        else:
            # search the databse
            response = requests.get("%s" % goto, headers=headers)

            # return query into a JSON list variable
            query = response.json()

            # retreiving useful data
            data = query["results"]
            pagination = query["pagination"]
            pages = pagination["pages"]
            page = pagination["page"]

            return render_template("search.html", data=data, pagination=pagination, pages=pages, page=page)

@app.route('/artist', methods=["GET", "POST"])
def artist():
    """Renders an artists page."""

    if request.method == "GET":
        return render_template("/artist.html")

    else:
        # initialise the variables from the hidden html form input
        type = request.form.get("type")
        url = request.form.get("url")
        thumb = request.form.get("thumb")

        # Authorization header to be embedded into the url 
        headers = {
        'Authorization': 'Discogs token=mqjXUBBzjnqrjUkKFIrOPAmlEZsGoDXjkRZgnRIR'
        }

        # search the database for artist information
        artists = requests.get("%s" % url, headers=headers)
        artist = artists.json()

        # set variable if user is selecting pagination
        goto = request.form.get("goto")

        if goto == None:

            # search the database for artists releases
            releases = requests.get("%s/releases?per_page=50" % url, headers=headers)
            release = releases.json()

            # retreiving useful data
            data = release["releases"]
            pagination = release["pagination"]
            pages = pagination["pages"]
            page = pagination["page"]
        

            return render_template("/artist.html",artist=artist, data=data, artistThumb=thumb, page=page, pages=pages, pagination=pagination, type=type, url=url, thumb=thumb)

        else:

            # search the database for artists releases goto page
            releases = requests.get("%s" % goto, headers=headers)
            release = releases.json()

            # retreiving useful data
            data = release["releases"]
            pagination = release["pagination"]
            pages = pagination["pages"]
            page = pagination["page"]
        

            return render_template("/artist.html",artist=artist, data=data, artistThumb=thumb, page=page, pages=pages, pagination=pagination, type=type, url=url, thumb=thumb)

@app.route("/release", methods=["GET", "POST"])
def release():
    '''Display release results'''

    if request.method == "GET":
        return render_template("/release.html")

    else:
        # initialise the variables from the hidden html form input
        type = request.form.get("type")
        url = request.form.get("url")
        thumb = request.form.get("thumb")

        # Authorization header to be embedded into the url 
        headers = {
        'Authorization': 'Discogs token=mqjXUBBzjnqrjUkKFIrOPAmlEZsGoDXjkRZgnRIR'
        }

        # search the database for release information
        releases = requests.get("%s" % url, headers=headers)
        release = releases.json()

        #initailising list of youtube videos and filtering out just the urls and removing all but the video id then adding them to a list
        #videos = release["videos"]

        #videoIds = []
        #for row in videos:
            #link = row["uri"]
            #videoId = get_yt_video_id(link)
            #videoIds.append(videoId)

        #embed = "https://www.youtube.com/embed/"

        
        return render_template("/release.html", get_yt_video_id=get_yt_video_id, release=release, thumb=thumb)


@app.route("/master", methods=["GET", "POST"])
def master():
    '''Display release results'''

    if request.method == "GET":
        return render_template("/release.html")

    else:
        # initialise the variables from the hidden html form input
        type = request.form.get("type")
        url = request.form.get("url")
        thumb = request.form.get("thumb")

        # Authorization header to be embedded into the url 
        headers = {
        'Authorization': 'Discogs token=mqjXUBBzjnqrjUkKFIrOPAmlEZsGoDXjkRZgnRIR'
        }

        # search the database for release information
        releases = requests.get("%s" % url, headers=headers)
        release = releases.json()

        #initailising list of youtube videos and filtering out just the urls and removing all but the video id then adding them to a list
        #videos = release["videos"]
        #videoIds = []
        #for row in videos:
            #link = row["uri"]
            #videoId = get_yt_video_id(link)
            #videoIds.append(videoId)

        #embed = "https://www.youtube.com/embed/"

        
        return render_template("/release.html", get_yt_video_id=get_yt_video_id, release=release, thumb=thumb)

@app.route('/label', methods=["GET", "POST"])
def label():
    """Renders an label page."""

    if request.method == "GET":
        return render_template("/label.html")

    else:
        # initialise the variables from the hidden html form input
        type = request.form.get("type")
        url = request.form.get("url")
        thumb = request.form.get("thumb")

        # Authorization header to be embedded into the url 
        headers = {
        'Authorization': 'Discogs token=mqjXUBBzjnqrjUkKFIrOPAmlEZsGoDXjkRZgnRIR'
        }

        # search the database for label information
        labels = requests.get("%s" % url, headers=headers)
        label = labels.json()

        # set variable if user is selecting pagination
        goto = request.form.get("goto")

        if goto == None:

            # search the database for labels releases
            releases = requests.get("%s/releases?per_page=50" % url, headers=headers)
            release = releases.json()

            # retreiving useful data
            data = release["releases"]
            pagination = release["pagination"]
            pages = pagination["pages"]
            page = pagination["page"]
        

            return render_template("/label.html", label=label, data=data, labelThumb=thumb, page=page, pages=pages, pagination=pagination, type=type, url=url, thumb=thumb)

        else:

            # search the database for artists releases goto page
            releases = requests.get("%s" % goto, headers=headers)
            release = releases.json()

            # retreiving useful data
            data = release["releases"]
            pagination = release["pagination"]
            pages = pagination["pages"]
            page = pagination["page"]
        

            return render_template("/label.html", label=label, data=data, labelThumb=thumb, page=page, pages=pages, pagination=pagination, type=type, url=url, thumb=thumb)




if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
