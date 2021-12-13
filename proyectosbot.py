import tweepy, time, sys, json
from proyectos import connection, write_output
from datetime import date, datetime
from config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

def maketweet():
    write_output()
    db=connection()
    if db.proyectos.count_documents({"tweet":False})!=0:
        tweet=db.proyectos.find({"tweet":False})
        for i in tweet:
            text = "%s \nIngreso: %s \n"%(i['acapite'], i['fechaIngresoExpediente'])
            if i['urls'] != None:
                whatsHappening(text, 0, '\n'.join(i['urls']))
            else:
                whatsHappening(text, 0, '')
            db.proyectos.update_one(i, {"$set": { "tweet": True}})
    else:
        tweet=db.proyectos.find().sort("_id",-1).limit(5)
        for i in tweet:
            text = "%s \nIngreso: %s \n"%(i['acapite'], i['fechaIngresoExpediente'])
            if i['urls'] != None:
                whatsHappening(text, 0, '\n'.join(i['urls']))
            else:
                whatsHappening(text, 0, '')


def whatsHappening(text, id, urls):
    try:
        if len(text)>280:
            index=text[:280].rfind(" ")
            if id==0:
                tuit = api.update_status(text[:index].title())
                whatsHappening(text[index+1:], tuit.id, urls)
            else:
                tuit = api.update_status(text[:index].title(), id)
                whatsHappening(text[index+1:], tuit.id, urls)
        else:
            tuit=api.update_status(text.title(), id)
            if len(urls):
                api.update_status("Documentos: \n %s"%(urls), tuit.id)

    except tweepy.TweepError as error:
        if error.api_code != 187:
            raise error

maketweet()