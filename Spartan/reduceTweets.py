import tweepy
import json
import re
import couchdb
import time
import io
from shapely.geometry import Point, box
from textblob import TextBlob

# Define number of tweets we want from each region
dic1={'Wyndham': 632,
    'Bayside': 199,
    'Kingston': 525,
    'Dandenong': 383,
    'Casey - North': 7445,
    'Casey - South': 429,
    'Cardinia': 165,
    'Yarra Ranges': 24,
    'Melton - Bacchus Marsh': 68,
    'Hobson Bay': 280,
    'Brimbank': 92,
    'Moreland - North': 355,
    'Banyule': 386,
    'Darebin - North': 411,
    'Whittlesea - Wallan': 414,
    'Darebin - South': 417,
    'Brunswick - Coburg': 913,
    'Monash': 1101,
    'Stonnington - East': 679,
    'Knox': 162,
    'Whitehorse - West': 443,
    'Manningham - West': 1126,
    'Whitehorse - East': 171,
    'Manningham - East': 93,
    'Essendon': 409,
    'Stonnington - West': 986,
    'Boroondara': 223,
    'Yarra': 1204,
    'Maribyrnong': 466,
    'Keilor': 112,
    'Tullamarine - Broadmeadows': 166,
    'Sunbury': 127,
    'Macedon Ranges': 108,
    'Port Phillip': 483,
    'Glen Eira': 278,
    'Melbourne City': 1123,
    'Nillumbik - Kinglake': 107,
    'Maroondah': 73
 }

data = open("bigTweet.json", 'r', encoding = 'utf-8')
f = io.open("finalTweet.json", 'a', encoding='utf-8')

# For each SA3 region, add tweet to finalTweet.json until we get the desired number of tweets from that region.

count = [0]*38
for line in data:
    if len(line)>10:
        tweet = json.loads(line[:-2])
        if tweet['SA3'] == 'Melton - Bacchus Marsh' and count[0]<68:
            f.write(json.dumps(tweet))
            f.write("\n")
            count[0]+=1
        elif tweet['SA3'] == 'Yarra Ranges' and count[1]<25:
            f.write(json.dumps(tweet))
            f.write("\n")
            count[1]+=1
        elif tweet['SA3'] == 'Monash' and count[2]<1101:
            f.write(json.dumps(tweet))
            f.write("\n")
            count[2]+=1
        elif tweet['SA3'] == 'Stonnington - East' and count[3]<679:
            f.write(json.dumps(tweet))
            f.write("\n")
            count[3]+=1
        elif tweet['SA3'] == 'Knox' and count[4]<162:
            f.write(json.dumps(tweet))
            f.write("\n")
            count[4]+=1
        elif tweet['SA3'] == 'Whitehorse - West' and count[5]<443:
            f.write(json.dumps(tweet))
            f.write("\n")
            count[5]+=1
        elif tweet['SA3'] == 'Manningham - West' and count[6]<1126:
            f.write(json.dumps(tweet))
            f.write("\n")
            count[6]+=1
        elif tweet['SA3'] == 'Whitehorse - East' and count[7]<171:
            f.write(json.dumps(tweet))
            f.write("\n")
            count[7]+=1
        elif tweet['SA3'] == 'Manningham - East' and count[8]<93:
            f.write(json.dumps(tweet))
            f.write("\n")
            count[8]+=1
        elif tweet['SA3'] == 'Essendon' and count[9]<409:
            f.write(json.dumps(tweet))
            f.write("\n")
            count[9]+=1
        elif tweet['SA3'] == 'Maribyrnong' and count[10]<466:
            f.write(json.dumps(tweet))
            f.write("\n")
            count[10]+=1
        elif tweet['SA3'] == 'Tullamarine - Broadmeadows' and count[11]<116:
            f.write(json.dumps(tweet))
            f.write("\n")
            count[11]+=1
        elif tweet['SA3'] == 'Sunbury' and count[12]<127:
            f.write(json.dumps(tweet))
            f.write("\n")
            count[12]+=1
        elif tweet['SA3'] == 'Macedon Ranges' and count[13]<108:
            f.write(json.dumps(tweet))
            f.write("\n")
            count[13]+=1
        elif tweet['SA3'] == 'Port Phillip' and count[14]<483:
            f.write(json.dumps(tweet))
            f.write("\n")
            count[14]+=1
        elif tweet['SA3'] == 'Keilor' and count[15]<112:
            f.write(json.dumps(tweet))
            f.write("\n")
            count[15]+=1
        elif tweet['SA3'] == 'Glen Eira' and count[17]<278:
            f.write(json.dumps(tweet))
            f.write("\n")
            count[17]+=1
        elif tweet['SA3'] == 'Melbourne City' and count[18]<1123:
            f.write(json.dumps(tweet))
            f.write("\n")
            count[18]+=1
        elif tweet['SA3'] == 'Wyndham' and count[19]<632:
            f.write(json.dumps(tweet))
            f.write("\n")
            count[19]+=1
        elif tweet['SA3'] == 'Bayside' and count[20]<199:
            f.write(json.dumps(tweet))
            f.write("\n")
            count[20]+=1
        elif tweet['SA3'] == 'Dandenong' and count[21]<383:
            f.write(json.dumps(tweet))
            f.write("\n")
            count[21]+=1
        elif tweet['SA3'] == 'Casey - North' and count[22]<429:
            f.write(json.dumps(tweet))
            f.write("\n")
            count[22]+=1
        elif tweet['SA3'] == 'Casey - South' and count[23]<417:
            f.write(json.dumps(tweet))
            f.write("\n")
            count[23]+=1
        elif tweet['SA3'] == 'Cardinia' and count[24]<165:
            f.write(json.dumps(tweet))
            f.write("\n")
            count[24]+=1
        elif tweet['SA3'] == 'Yarra Ranges' and count[25]<25:
            f.write(json.dumps(tweet))
            f.write("\n")
            count[25]+=1
        elif tweet['SA3'] == 'Melton - Bacchus Marsh' and count[26]<68:
            f.write(json.dumps(tweet))
            f.write("\n")
            count[27]+=1
        elif tweet['SA3'] == 'Hobson Bay' and count[28]<280:
            f.write(json.dumps(tweet))
            f.write("\n")
            count[28]+=1
        elif tweet['SA3'] == 'Brimbank' and count[29]<92:
            f.write(json.dumps(tweet))
            f.write("\n")
            count[29]+=1
        elif tweet['SA3'] == 'Kingston' and count[30]<525:
            f.write(json.dumps(tweet))
            f.write("\n")
            count[30]+=1
        elif count1<200000:
            f.write(json.dumps(tweet))
            f.write("\n")
            count1+=1
