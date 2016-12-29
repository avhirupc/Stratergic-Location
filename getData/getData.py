import json
import facebook
import requests as r
from bs4 import  BeautifulSoup

token = ''#add token here
graph = facebook.GraphAPI(access_token=token)
places = {
}
catToRemove = ['Train Station','Region','Neighborhood','City','Locality','Other','Bridge','Real Estate','Residence']
placeIDS = []

s = r.Session()
def searchPlaces(url):
    res = s.get(url)
    return str(res.text)

def getPlaces(center,dist):
    url = 'https://graph.facebook.com/v2.8/search?access_token='+token+'&type=place&center='+center+'&debug=all&distance='+dist+'&format=json&method=get&pretty=1&suppress_http_code=1'
    visit = url
    after = True
    while after:
        response = searchPlaces(visit)
        jsonObj = json.loads(response)
        print(jsonObj)
        for place in jsonObj["data"]:
            if place["id"] not in places:
                id = place["id"]
                name = place["name"]
                places[id] = {}
                places[id]["name"] = name
                placeIDS.append(id)
        if "paging" in jsonObj and "cursors" in jsonObj["paging"] and "after" in jsonObj["paging"]["cursors"]:
            visit = url + '&after='+jsonObj["paging"]["cursors"]["after"]
        else:
            after = False


def getPlaceDetails(placeID):
    place = graph.get_object(str(placeID))
    newPlace = places[placeID]
    newPlace["checkins"] = int(place["checkins"])
    newPlace["likes"] = int(place["likes"])
    newPlace["latitude"] = float(place["location"]["latitude"])
    newPlace["longitude"] = float(place["location"]["longitude"])
    newPlace["categories"] = []
    for category in place["category_list"]:
        if category["name"] not in catToRemove:
            newPlace["categories"].append(category["name"])
        else:
            del places[placeID]
            return
    return

def exportData(file):
    jdata = json.dumps(places,indent=4)
    file = open(file+'.json','w')
    file.write(jdata)
    file.close()

def getData(center,dist):
    getPlaces(center,dist)
    for placeID in placeIDS:
        getPlaceDetails(placeID)
    exportData('cityName')


center = '12.985966,77.580084'
dist = '40000'
getData(center,dist)






