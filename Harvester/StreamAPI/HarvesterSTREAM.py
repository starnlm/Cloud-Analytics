# Group 53, Melbourne, Perth, Uttar Pradesh
# Team Members: Aditi Basu 1178282, Kevin Van 995203, Linan Jia 806003, Nand Lal Mishra 1245159, Zhirui Liang 1255971

import io
import tweepy
import couchdb
import json
import re
import time
from shapely.geometry import Polygon, box
import configparser
from textblob import TextBlob
from dictionaries import boundbox, keywords
from urllib3.exceptions import ProtocolError

#Define Database connection creds

config = configparser.ConfigParser(allow_no_value = True)
config.read('applications.ini')
host = config.items('harvesters')[0][0]
port = "5984"
admin_username = "admin"
admin_password = "admin"

conumer_key = '7z2T7cmoBWtPqTKE1O62fE1bb'
consumer_secret = 'z2Lcf1nzCtyKsWg7fu84HtkwffCagueQZgwgeMdBvdK3rs7yhO'
auth = tweepy.OAuthHandler(conumer_key, consumer_secret)


access_key = '1383663647797374980-8Uh16uDZvOEbAnRCVHodX82V91Yi81'
access_secret = 'ZBnQpqUh66l2w48yq2A4ObFIFG9Gu1zFjr8vLbh9ysn7T'
auth.set_access_token(access_key, access_secret)

# Bounding Box estimated from AURIN

boundbox_shapes = {}
for name, coordinates in boundbox.items():
    boundbox_shapes[name] = box(coordinates[0], coordinates[1], coordinates[2], coordinates[3])

def main():

    def connect_server(server, port, u_name, u_pass):
        
        try:
            # local_server
            # couchclient = couchdb.Server()
            # secure_remote_server
            couchclient = couchdb.Server('http://' + u_name + ':' + u_pass + '@' + server + ':' + port)
        except:
            print( "Cannot find CouchDB Server ... Exiting\n")
        
        return couchclient

    def connect_database(db, couchserver):
    #Try to use the passed bucket or else create the bucket
        try:
            dbfound = couchserver[db]
            print("Database found! Using the given bucket.")
            return dbfound
        except:
            print( "Cannot find CouchDB Database\n")
            print( "Creating New Database\n")
            return couchserver.create(db)

    server = connect_server(host, port, admin_username, admin_password)
    database = connect_database('finaltweets', server)

            
    def party(text):
        for k, val in keywords.items():
            for term in val:
                if term in text:
                    return k
        return None

    def sentiment(text):
        text = re.sub('([#])|([^a-zA-Z])',' ',text )
        analysis = TextBlob(text)
        # set sentiment 
        if analysis.sentiment.polarity > 0: 
            return 'positive'

        elif analysis.sentiment.polarity == 0: 
            return 'neutral'

        else:
            return 'negative'
        
    def loc_classifier(bb):
    # Convert the tweet coordinate to polygon format
        shp = Polygon(bb)
        
        # Compare with the existing boundary box values to classify the tweet to a city
        for name, shapes in boundbox_shapes.items():
            if shapes.contains(shp.centroid):
                return (name, list(shp.centroid.coords)[0])
        return ("RestOfAus", list(shp.centroid.coords)[0])
    
    def transfer_data(tweet, db = database):
        if str(tweet["id"]) not in db:
            tweet['_id'] = "%d" % tweet["id"]
            
            if hasattr(tweet, "retweeted_status"):
                try:
                    tweet["text"] = tweet["retweeted_status"]["extended_tweet"]["full_text"]
                except AttributeError:
                    tweet["text"] = tweet["retweeted_status"]["text"]
            else:
                try:
                    tweet["text"] = tweet["extended_tweet"]["full_text"]
                except KeyError:
                    pass 
            tweet['sentiment'] = sentiment(tweet['text'])
            tweet['party'] = party(tweet['text'].lower())
            SA, coords = loc_classifier(tweet['place']["bounding_box"]["coordinates"][0])
            tweet['longitude'] = coords[0]
            tweet['latitude'] = coords[1]
            tweet["SA3"] = SA
            
            db.save(tweet)

    class StreamListener(tweepy.StreamListener):
        
        def on_status(self, tweet):
            print('Ran on_status')

        def on_error(self, status_code):
            print(status_code)
            
            if status_code == 429:
                print("App's rate limit having been exhausted for the resource. Waiting.....")
                time.sleep(15*60) # Waiting 15 minutes 
                
            if status_code == 420:
                print("App is being rate limited for making too many requests. Waiting.....")
                time.sleep(60) # Waiting 1 minute
            else:
                print("An unexpected error has occured. Retrying in 15 s")
                time.sleep(15)

        
        def on_data(self, data):
            if data[0].isdigit():
                pass
            else:
                city = json.loads(data)['place']
                if city: 
                    transfer_data(json.loads(data))
            return True
            
    # 144.2997, -38.9436, 145.9806, -36.9999 Melbourne
    # 100.7169, -44.7444, 159.8783, -11.5462 Aus
    # 73.1302, 10.8048, 83.6442, 28.4628 India
    # -130.7760, 32.8182, -80.8871, 57.4231 USA
    loc = [100.7169, -44.7444, 159.8783, -11.5462] #longitude latitude

    l = StreamListener() #Set the time seconds*minutes*hours
    streamer = tweepy.Stream(auth=auth, listener=l)
    while True:    
        try:
         # load the streamer
    #streamer.filter(locations=loc, languages = ['en'],  is_async = True)
            streamer.filter(locations=loc, languages = ['en'], stall_warnings=True)
        except (ProtocolError, AttributeError):
            continue


if __name__ == '__main__':
    main()
