import json
import re
import io
from shapely.geometry import Point, box
from textblob import TextBlob

keywords = {"left-wing": ['mark mcgowan', "Mark McGowan", "#scottyFromMarketing", "Scotty from Marketing", "How Good is Australia?", "#HowGoodisAustralia", "#coolAndNormal","#shitfuckery","Juice Media", "Honest government ads", "LNPfail", "#LNPfail", "Smirk ScoMo", "#empathyCoach", "Dutton potato" ,"#smirko", "slomo", "#sportsRorts", "#saveOurABC", "#freedomOfPress", "#mediaFreedom","#defendMediaFreedom","#IStandWithDan","#climateCrisis","#climateEmergency","#stopAdani","#ss4c","#extinctionrebellion","#xrwa","#climateaction","#fridaysforfuture","#climatestrike","#climatejustice","#gretathunberg","#blackLivesMatter","#blm","#metoo","#bringThemHere","#IhaveARoom","#gameOver","#PalmSunday","#freeTheRefugees","#justiceForRefugees","#justice4refugees","#hometoBilo","#animalRights","#mcGowanforPM","#scomo #hawaii","#scottyFromMarketing #hawaii","#auspol #hawaii"]}
boundbox = {
    "Brimbank": [144.7444,-37.8228,144.8559,-37.6629],
    "Hobson Bay": [144.7514,-37.9000,144.9155,-37.8138],
    "Maribyrnong": [144.8392,-37.8270,144.9165,-37.7558],
    "Melton - Bacchus Marsh": [144.3336,-37.8105,144.7682,-37.5464],
    "Wyndham": [144.4441,-38.0046,144.8274,-37.7810],
    "Keilor": [144.8016,-37.7761,144.9347,-37.6982],
    "Macedon Ranges": [144.4577,-37.5677,144.9212,-37.1751],
    "Moreland - North": [144.8862,-37.7360,144.9853,-37.6909],
    "Sunbury": [144.6236,-37.6649,144.8705,-37.4819],
    "Tullamarine - Broadmeadows": [144.7600,-37.7104,144.9778,-37.5021],
    "Bayside": [144.9834,-37.9964,145.0553,-37.8833],
    "Glen Eira": [144.9967,-37.9388,145.0882,-37.8602],
    "Kingston":[145.0344,-38.0850,145.1563,-37.9330],
    "Stonnington - East":[145.0277,-37.8930,145.0922,-37.8374],
    "Banyule": [145.0278,-37.7851,145.1437,-37.6826],
    "Darebin - North": [144.9703,-37.7557,145.0754,-37.6910],
    "Nillumbik - Kinglake": [145.0789,-37.7417,145.5800,-37.4093],
    "Whittlesea - Wallan": [144.8807,-37.7000,145.2658,-37.2629],
    "Cardinia": [145.3640,-38.3325,145.7651,-37.8577],
    "Casey - North": [145.2154,-38.2481,145.4306,-38.0170],
    "Casey - South": [145.2149,-38.2485,145.4307,-38.0170], 
    "Dandenong":[145.0795,-38.0777,145.2519,-37.9240],
    "Monash":[145.0825,-37.9401,145.2201,-37.8533],
    "Brunswick - Coburg": [144.9267,-37.7802,144.9869,-37.7325],
    "Darebin - South": [144.9792,-37.7856,145.0371,-37.7503],
    "Essendon": [144.8889,-37.7897,144.9404,-37.7346],
    "Melbourne City": [144.9027,-37.8507,144.9914,-37.7754],
    "Port Phillip": [144.8971,-37.8917,145.0105,-37.8200],
    "Stonnington - West": [144.9833,-37.8663,145.0327,-37.8296],
    "Yarra": [144.9588,-37.8345,145.0453,-37.7735],
    "Boroondara": [144.9993,-37.8759,145.1067,-37.7769],
    "Manningham - West": [145.0671,-37.8025,145.1841,-37.7339],
    "Whitehorse - West": [145.0951,-37.8620,145.1696,-37.7922],
    "Knox": [145.1909,-37.9649,145.3476,-37.8330],
    "Manningham - East": [145.1678,-37.8118,145.2970,-37.7024],
    "Maroondah": [145.2133,-37.8439,145.3187,-37.7618],
    "Whitehorse - East": [145.1569,-37.8652,145.2167,-37.8012],
    "Yarra Ranges": [145.2869,-37.9750,145.8784,-37.5260]
    
}

boundbox_shapes = {}
for name, coordinates in boundbox.items():
    boundbox_shapes[name] = box(coordinates[0], coordinates[1], coordinates[2], coordinates[3])

    data = open("/home/nandlalm/bigTwitter.json", 'r', encoding = 'utf-8')
    f = io.open("bigTweet.json", 'a', encoding='utf-8')

    def party(text):
        
        #text = re.sub('([^a-zA-Z])',' ',text )
        #print(text)
        for k, val in keywords.items():
            for term in val:
                if term in text:
                    return k
        return None

def main():
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
        shp = Point(bb)
        # Compare with the existing boundary box values to classify the tweet to a SA3 region
        for name, shapes in boundbox_shapes.items():
            if shapes.contains(shp):
                #print(name)
                return name
        return "RestOfAus"

    def processed_line(tweet):
        tweet = json.loads(tweet)
        #print(tweet['value']['properties']['text'])
        sentiment_val = sentiment(tweet['value']['properties']['text']) 
        tweet['sentiment'] = sentiment_val
        
        pol_party = party(tweet['value']['properties']['text'].lower())
        tweet['party'] = pol_party
        
        tweet['longitude'] = tweet['value']['geometry']['coordinates'][0]
        tweet['latitude'] = tweet['value']['geometry']['coordinates'][1]
        
        tweet["SA3"] = loc_classifier(tweet['value']["geometry"]["coordinates"])
        
        return tweet

    f.write('{"docs":[')
    f.write('\n')
    i = 0
    count1 = count2 = 0
    for t_info in data:
        if count1<300000:
            if len(t_info)>10 and count2!=0:
                if t_info[-2]==",":
                    line=t_info[:-2]
                else:
                    line=t_info
                #line = json.loads(line)
                #print(line)
                line_new = processed_line(line)
                #json.dumps(json_data["data"])
                if line_new["SA3"] != 'RestOfAus':
                    f.write(json.dumps(line_new))
                    f.write(',')
                    f.write("\n")
                    #print(line_new)
                    count1+=1
            count2+=1
        else:
            break
    print(count1)
    print(count2)
    f.write(']}')
    f.close()
    data.close()

if __name__ == '__main__':
    main()
