import os
import requests
from urllib.parse import urljoin

from flask import redirect, render_template, request, session
from functools import wraps

headers = {
    'Authorization': 'Discogs token=mqjXUBBzjnqrjUkKFIrOPAmlEZsGoDXjkRZgnRIR'
}

search = 'interscope'

response = requests.get("https://api.discogs.com/database/search?q=%s&{?type,title,release_title,credit,artist,anv,label,genre,style,country,year,format,catno,barcode,track,submitter,contributor}" % search,headers=headers)

query = response.json()
data = query["results"]

for row in data:
    result = row["type"]
    print(row["type"])
    print('')
    print('')
    #print(row["master_url"])

    #response = requests.get("%s" % result, headers=headers)
    #query = response.json()
    #print(query)

