from tkinter import *
from tkinter import ttk
import threading
import sys
import tweepy
import csv
import logging
import json
from pymongo import MongoClient
from tweepy import Stream
from tweepy.streaming import StreamListener
root = Tk()
mainframe = ttk.Frame(root, padding="3 3 12 12")
streamcount1=0
streamcount2=0
client1 = MongoClient()
client2 = MongoClient()
client3 = MongoClient()
client4 = MongoClient()
db1 = client1.tweets_database  # use a database called "tweets_database"
db2 = client2.tweets_database
db3 = client3.tweets_database
db4 = client4.tweets_database

csvFile = open('tweets.csv', 'a')
csvWriter = csv.writer(csvFile)

LOG_FILENAME = 'debug_log.out'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,)

class MyListener(StreamListener):
    def on_data(self, data):
        global streamcount1
        str1=json.loads(data)
        collection2 = db1.tweets_keyword
        try:
            if streamcount1<50:
                streamcount1+=1
                print(str1['text'])
                tx2.insert(END,str1['text']+"\n")
                text_file_doc = {"ID": str(str1['id']), "USERNAME" : str(str1['user']['screen_name']),"TWEET": str(str1['text']), "LOCATION":str(str1['coordinates']) }
                collection2.insert(text_file_doc)
                return True
            else:
                return False

        except BaseException as e:
            print("Error on_data: %s" % str(e))
            logging.exception('Got exception on main handler')
        return True

    def on_error(self, status):
        print(status)
        logging.exception(status+'error on main handler')
        return True

class CustomStreamListener(StreamListener):
    def __init__(self):
        try:
            super(StreamListener, self).__init__()
        except Exception as e:
            print(e)

    def on_data(self, data):
        global streamcount2
        str1=json.loads(data)
        collection1 = db2.tweets_location
        #5.0770049095, 47.2982950435, 15.0403900146, 54.9039819757 example location
        try:
            if streamcount2<50:
                streamcount2+=1
                print(str1['text'])
                tx1.insert(END,str1['text'])
                text_file_doc = {"ID": str(str1['id']), "USERNAME" : str(str1['user']['screen_name']),"TWEET": str(str1['text']), "LOCATION":str(str1['coordinates']) }
                collection1.insert(text_file_doc)
                return True
            else:
                return False
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            logging.exception('Got exception on main handler')
        return True

    def on_error(self, status_code):
        print(sys.stderr, 'Encountered error with status code:', status_code)
        logging.exception('error on main handler')
        return True

    def on_timeout(self):
        print(sys.stderr, 'Timeout...')
        logging.exception('Time out on main handler')
        return True



def search_keyword(str):
    collection3 = db3.search_tweets_keyword
    for tweet in tweepy.Cursor(api.search, q=str, lang="en", since_id=2015-12-31).items(50):
        try:
            print(tweet.text)
            tx1.insert(END,tweet.text+"\n")
            text_file_doc = {"ID": tweet.id, "USERNAME" : tweet.user.screen_name,"TWEET": tweet.text, "LOCATION":tweet.coordinates }
            collection3.insert(text_file_doc)
        except Exception as e:
            print(e)
            logging.exception('Got exception on main handler')
    #'44,34,9333km' example location
    return
def search_location(str):
   # coordinates=str.split(",")
    collection4 = db4.search_tweets_location
    for tweet in tweepy.Cursor(api.search, geocode=str, lang="en", since_id=2015-12-31).items(50):
        try:
            print(tweet.text)
            tx2.insert(END,tweet.text+"\n")
            text_file_doc = {"ID": tweet.id, "USERNAME" : tweet.user.screen_name,"TWEET": tweet.text, "LOCATION":tweet.coordinates }
            collection4.insert(text_file_doc)
        except:
            logging.exception('Got exception on main handler')
    return

def locate(arg):
    global streamcount1
    global streamcount2
    streamcount2=0
    streamcount1=0
    coordinates=arg.split(",")
    sapi = Stream(auth, CustomStreamListener())
    sapi.filter(locations=[float(coordinates[0]),float(coordinates[1]),float(coordinates[2]),float(coordinates[3])])
    #78, 10, 79, 11 local example location
    return
def key_search(arg):
    global streamcount1
    global streamcount2
    streamcount1=0
    streamcount2=0
    twitter_stream = Stream(auth, MyListener())
  # given_keyword=keyword_entry.get()
    twitter_stream.filter(track=[arg])
    return

def fetch():
    str=keyword_entry.get()
    str2=location_entry.get()
    ttk.Label(mainframe, text="Keyword: "+str+" \nLocation: "+str2).grid(column=1, row=5, sticky=E)
    ttk.Label(mainframe, text="Fetching data...").grid(column=2, row=5, sticky=E)
    p = ttk.Progressbar(mainframe, orient=HORIZONTAL, length=200, mode='determinate')
    p.grid(row=5,column=3)
    p.start(10)
    ttk.Button(mainframe, text="Update",command=process).grid(column=3, row=8, sticky=W)
    return

def process():
    str=keyword_entry.get()
    str2=location_entry.get()
    if var2.get():
        print("Twitter Streaming is selected")
    if var5.get():
        print("Location filter selected")
        t1 = threading.Thread(name='my_service2', target=locate(str2))
        t1.daemon=True
        t1.start()
    if var4.get():
        print("Keyword filter selected")
        t2 = threading.Thread(name='my_service', target=key_search(str))
        t2.daemon=True
        t2.start()

    if var1.get():
        print("Twitter Search is selected")
    if var4.get():
        print("Keyword filter selected")
        t2 = threading.Thread(name='my_service', target=search_keyword(str))
        t2.start()
    if var5.get():
        print("Location filter selected")
        t2 = threading.Thread(name='my_service', target=search_location(str2))
        t2.start()
    #root.quit()
    return

keyword = StringVar()
location = StringVar()
var1=IntVar()
var2=IntVar()
var3=IntVar()
var4=IntVar()
var5=IntVar()

tx1=Text(mainframe,width=30,height=10)
tx2=Text(mainframe,width=30,height=10)
keyword_entry = ttk.Entry(mainframe, width=7, textvariable=keyword)
location_entry = ttk.Entry(mainframe, width=7, textvariable=location)
# Consumer keys and access tokens, used for OAuth
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''
# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
print("Authentication done")
root.title(" Module #1 ")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)
tx1.grid(column=4,row=7,sticky=(W,E))
tx2.grid(column=2,row=7,sticky=(W,E))
Checkbutton(mainframe, text="Twitter Search API", variable=var1).grid(row=1,column=2, sticky=W)
Checkbutton(mainframe, text="Twitter Streaming API", variable=var2).grid(row=1,column=3, sticky=W)
Checkbutton(mainframe, text=" ", variable=var4).grid(row=2,column=4, sticky=W)
Checkbutton(mainframe, text=" ", variable=var5).grid(row=3,column=4, sticky=W)
keyword_entry.grid(column=3, row=2, sticky=(W, E))
location_entry.grid(column=3, row=3,sticky=(W, E))
ttk.Label(mainframe, textvariable=location).grid(column=2, row=3, sticky=(W, E))
ttk.Label(mainframe, text="Target Keyword").grid(column=2, row=2, sticky=W)
ttk.Label(mainframe, text="Crawler Module").grid(column=1, row=1, sticky=E)
ttk.Label(mainframe, text="Target Location").grid(column=2, row=3, sticky=W)
ttk.Label(mainframe, text="Keyword based results:").grid(column=2, row=6, sticky=W)
ttk.Label(mainframe, text="Location based results:").grid(column=4, row=6, sticky=W)
keyword_entry.focus()
ttk.Button(mainframe, text="Crawl",command=fetch).grid(column=3, row=4, sticky=W)
for child in mainframe.winfo_children(): child.grid_configure(padx=20, pady=5)
root.bind('<Return>', fetch)
root.mainloop()
