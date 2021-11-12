import json
import couchdb


host = '172.26.131.188'
port = "5984"
admin_username = "admin"
admin_password = "admin"

def connect_server(server, port, u_name, u_pass):
        
    try:
        # local_server
        # couchclient = couchdb.Server()
        # secure_remote_server
        couchclient2 = couchdb.Server('http://' + u_name + ':' + u_pass + '@' + server + ':' + port)
        
    except:
        print( "Cannot find CouchDB Server ... Exiting\n")
    
    return couchclient2

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


def transfer_data(tweet_value, db = database):
    if str(tweet["id"]) not in db:
        tweet['_id'] = "%d" % int(tweet["id"])
        db.save(tweet)


data = open("finalTweet.json", 'r', encoding = 'utf-8')

for t_info in data:
    if t_info!= '\n' and len(t_info)>20:
        tweet = json.loads(t_info[:-2])
        #print(tweet['id'], tweet['place']['bounding_box']['coordinates'][0], end = ' ')
        #print(t_info)
        #print('\n')
        #print('\n')
        print(tweet)
        #transfer_data(tweet)
    
data.close()
