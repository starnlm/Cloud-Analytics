# Group 53, Melbourne, Perth, Uttar Pradesh
# Team Members: Aditi Basu 1178282, Kevin Van 995203, Linan Jia 806003, Nand Lal Mishra 1245159, Zhirui Liang 1255971

# Import dependencies
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

# Define Database connection creds
config = configparser.ConfigParser(allow_no_value = True)
config.read('applications.ini')
host = config.items('harvesters')[0][0]
port = "5984"
admin_username = "admin"
admin_password = "admin"

# Define Twitter API creds
conumer_key = 'lfzvw3SQzTaxc1hIwL8H3kGds'
consumer_secret = 'gPy9qd94zPiULmrYw46x33nILaRkC7M1iwcnO6Y1g4LlhhQnLh'
auth = tweepy.OAuthHandler(conumer_key, consumer_secret)

access_key = '1382216544873189376-9UGxFVOWjogUgCLzhDnxGYg3tSk7wF'
access_secret = 'hQyjF6TQ3TLv2cjS1fVrNUFT3ue2Uq8tSGsgrBkHSm0Sa'
auth.set_access_token(access_key, access_secret)

# Create boxes for each SA3 region (imported from dictionaries.py)
boundbox_shapes = {}
for name, coordinates in boundbox.items():
    boundbox_shapes[name] = box(coordinates[0], coordinates[1], coordinates[2], coordinates[3])

# Main function
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
    
    # Connect to server
    server = connect_server(host, port, admin_username, admin_password)
    # Connect to database
    database = connect_database('finaltweets', server)

    # Function for political party classification
    def party(text):
        for k, val in keywords.items():
            for term in val:
                if term in text:
                    return k
        return None
    
    # Function for sentiment classification
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
    
    # Function for SA3 classification and longitude, latitude retrieval
    def loc_classifier(bb):
    # Convert the tweet coordinate to polygon format.
        shp = Polygon(bb)
        
        # Compare with the existing boundary box values to classify the tweet to a city.
        for name, shapes in boundbox_shapes.items():
            if shapes.contains(shp.centroid):
                return (name, list(shp.centroid.coords)[0])
        return ("RestOfAus", list(shp.centroid.coords)[0])
    

    # Define search api function. We try to collect 1000 tweets from Melbourne.
    def searchAPi():
        
        # write the tweets to a .json file
        f = io.open("test.json", 'a', encoding='utf-8') 
        kolkata = '22.572645,88.363892,10km' #### for trial purpose
        melb = '-37.840935,144.946457,100mi' #### to be used
        syd = '-33.8688,151.2093,20mi' #### for trial purpose
        
        # geocode is in (latitude,longitude,radius) format
        for status in tweepy.Cursor(api.search, q = '*', geocode = melb, tweet_mode="extended").items(1000):

            jdata = json.dumps(status._json)
            jdata2 = json.loads(jdata)
            city = jdata2['place'] # only if place value is present in the tweet we consider it.
            if city: 
                f.write(jdata)
                f.write("\n")
        f.close()
    
    # Function to transfer tweets from the .json file to couchdb database.
    def transfer_data(tweet_value, db = database):
        if str(tweet["id"]) not in db:
            # change the document id to tweet id for duplication detection.
            tweet['_id'] = "%d" % tweet["id"]
            
            # Get the full text and get rid of truncated text.
            try: 
                if tweet["retweeted_status"]:
                    #print("has")
        
                    tweet["text"] = tweet["retweeted_status"]["full_text"]
            
            except KeyError:
                try:
                    tweet["text"] = tweet["full_text"]
                except KeyError:
                    pass

            del tweet["full_text"]
            
            
            try:
                tweet["geo_location"] = loc_classifier(tweet['place']["bounding_box"]["coordinates"][0])
            except TypeError:
                tweet["geo_location"] = "None"
            
            # add sentiment to tweet
            tweet['sentiment'] = sentiment(tweet['text'])
            
            # add political party to tweet
            tweet['party'] = party(tweet['text'].lower())
            
            # add SA3, latitude, longitude to tweet 
            SA, coords = loc_classifier(tweet['place']["bounding_box"]["coordinates"][0])
            tweet['longitude'] = coords[0]
            tweet['latitude'] = coords[1]
            tweet["SA3"] = SA
            
            # save tweet to database as a document
            db.save(tweet)


            # print('process completed')
    
    # Define tweepy API
    api = tweepy.API(auth, wait_on_rate_limit=True)
    
    # Call the search api function
    searchAPi()

    # read the file where tweets are saved
    data = open("test.json", 'r', encoding = 'utf-8')
    
    for t_info in data:
        if t_info!='\n':
            tweet = json.loads(t_info)
            #print(tweet['id'], tweet['place']['bounding_box']['coordinates'][0], end = ' ')
            
            # transfer tweets to database
            transfer_data(tweet)


if __name__ == '__main__':
    main()
