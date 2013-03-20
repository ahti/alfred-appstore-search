# -*- coding: utf-8 -*-

import alp
import sys
import string
import requests
import json

def search_apps(search_string):
    prefs = alp.Settings()
    search_lang = prefs.get('lang', 'en')
    
    url = 'http://itunes.apple.com/{}/search'.format(search_lang)
    
    query = { 'entity' : 'macSoftware', 'term' : search_string } 
    r = requests.get(url, params=query)
    
    if r.status_code != 200:
        title = "Connection Error"
        sub = "Could not connect to App Store. HTTP Status: {}".format(r.status_code)
        item = alp.item(title = title,
                        subtitle = sub,
                        uid = "fail",
                        valid = False)
        alp.feedback([item])
        return
    
    items = []
    
    try:
        jsonarr = r.json()
        for app in jsonarr['results']:
            currentKey = 'averageUserRatingForCurrentVersion'
            allKey = 'averageUserRating'
            if currentKey in app:
                raiting = raiting_curr(app[currentKey])
            elif allKey in app:
                raiting = raiting_all(app[allKey])
            else:
                raiting = raiting_none()
            
            sub = u"{} · Version {} · by {} · {}".format(app['formattedPrice'],
                                                         app['version'],
                                                         app['sellerName'],
                                                         raiting)
            
            openUrl = app['trackViewUrl'].replace('https', 'macappstores', 1)
            item = alp.Item(title = app['trackName'],
                            subtitle = sub,
                            uid = app['bundleId'],
                            valid = True,
                            autocomplete = app['trackName'],
                            #icon = app['artworkUrl60'],
                            arg = openUrl)
            items.append(item)
    except (ValueError, KeyError):
        # either the response wasn't json, or some keys we rely on
        # were missing. Either way, feedback an error message.
        items = []
        
        subtitle = 'The API returned something unexpected. Maybe your lang setting ({}) isn\'t right?'.format(search_lang)
        item = alp.Item(title = 'Error: Unexpected response',
                        subtitle = subtitle,
                        uid = '',
                        valid = False,
                        autocomplete = search_string,
                        #icon = app['artworkUrl60'],
                        arg = '')
        items.append(item)
    
    alp.feedback(items)

def star_string(raiting):
    raiting = int(round(raiting, 0))
    string = u'★' * raiting + u'☆' * (5 - raiting)
    return string

def raiting_curr(raiting):
    return star_string(raiting) + " (Current Version)"

def raiting_all(raiting):
    return star_string(raiting) + " (All Versions)"

def raiting_none():
    return "No raiting available"


if __name__ == '__main__':
    search_apps(string.join(sys.argv[1:]))