import json
import pymongo
import re
import requests
import urllib3

from bs4 import BeautifulSoup
from datetime import datetime
from html.parser import HTMLParser
from pymongo import MongoClient

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def connection():
    client=MongoClient("mongodb://localhost:27017/")
    db=client["proyectospy"]
    return db

def proyectos():
    try:
        soup=json.loads(
            requests.get(
                "http://datos.congreso.gov.py/opendata/api/data/proyecto",
                timeout=5,
            ).text
        )

        for i in soup:
            i['tweet']=False
            i['urls']=adjuntos(i['appURL'])

        return soup
        
    except requests.ConnectionError:
        print("error al conectar")
    except Exception as e:
        print(e)   

def adjuntos(link):
    adj=[]
    try:
        soup = BeautifulSoup(
            requests.get(link, timeout=10,
            headers={'user-agent': 'Mozilla/5.0'}, verify=False).text, "html.parser")

        btn_onlclick_list = [a.get('onclick') for a in soup.find_all('button')]
        urls = list(dict.fromkeys(btn_onlclick_list))
        for s in urls:
            url=re.sub("[\\\\()']", '', s)
            url=url.replace("window.open","").replace(",_blank","")
            adj.append(url)
        
        return adj
    except Exception as e:
        print(e)

def write_output():
    db=connection()
    sorted_list = sorted(proyectos(), key=lambda i: i['idProyecto'])
    for i in sorted_list:
        try:
            db.proyectos.insert_one(i)
            db.proyectos.create_index("idProyecto", unique=True)
        except pymongo.errors.DuplicateKeyError:
            pass

write_output()