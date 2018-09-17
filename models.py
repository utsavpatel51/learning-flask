from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
import geocoder
import requests
import json
db = SQLAlchemy()
class User(db.Model):
    __tablename__='users'
    uid=db.Column(db.Integer,primary_key=True)
    f_name=db.Column(db.String(100))
    l_name=db.Column(db.String(100))
    email=db.Column(db.String(120),unique=True)
    pwdhash=db.Column(db.String(54))

    def __init__(self,f_name,l_name,email,passwd):
        self.f_name=f_name.title()
        self.l_name=l_name.title()
        self.email=email.lower()
        self.set_passwd(passwd)
    
    def set_passwd(self,passwd):
        self.pwdhash=generate_password_hash(passwd)
    def check_passwd(self,pwd):
        return check_password_hash(self.pwdhash,pwd)

class Place:
    def met_to_time(self,length):
        return int(length/80)
    def wiki_src(self,title):
        title=title.replace(' ','_')
        url="https://en.wikipedia.org/wiki/"+title
        return url
    def address_to_lat_lon(self,address):
        g=geocoder.google(address)
        return (g.lat,g.lng)
    def query(self,address):
        lat,lng=self.address_to_lat_lon(address)

        url="https://en.wikipedia.org/w/api.php?action=query&list=geosearch&gsradius=5000&gscoord={}%7C{}&gslimit=20&format=json".format(lat,lng)
        r=requests.get(url)
        data=json.loads(r.text)
        places=[]
        for place in data['query']['geosearch']:
            name=place['title']
            lat=place['lat']
            lng=place['lon']
            meters=place['dist']
            wiki_url=self.wiki_src(name)
            walking_time=self.met_to_time(meters)

            d={
                'name':name,
                'url':wiki_url,
                'time':walking_time,
                'lat':lat,
                'lng':lng
            }
            places.append(d)
        return places