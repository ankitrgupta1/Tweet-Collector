
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import time
import MySQLdb
import csv
import random
from datetime import date
import json

# Go to http://dev.twitter.com and create an app. 
# The consumer key and secret as well as the access_token and secret will be generated for you
# after you register with Twitter Developers

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

# Create your MySQL schema and connect to database, ex: mysql> SET PASSWORD FOR 'root'@'localhost' = PASSWORD('newpwd');
# db = MySQLdb.connect(host='localhost', user='root', passwd='', db='tweet')
# db.set_character_set('utf8')

Coords = dict()
XY = []


# curr = db.cursor()

# per request, write output to csv, rather than mysql. Be aware of limited rows to csv.
# The streaming API will return millions of rows per day.
# csvfile = open('geopy_results.csv','wb')
# csvwriter = csv.writer(csvfile)
# csvwriter.writerow(['UserID', 'Date', 'Lat', 'Long', 'Text'])


class StdOutListener(StreamListener):
    """ A listener handles tweets that are the received from the stream.
                This is a basic listener that inserts tweets into MySQLdb.
                """

    def on_status(self, status):
        # print "Tweet Text: ",status.text
        text = status.text
        # print "Time Stamp: ",status.created_at
        try:
            Coords.update(status.coordinates)
            XY = (Coords.get('coordinates'))  # Place the coordinates values into a list 'XY'
            # print "X: ", XY[0]
            # print "Y: ", XY[1]
        except:
            # Often times users opt into 'place' which is neighborhood size polygon
            # Calculate center of polygon
            Box = status.place.bounding_box.coordinates[0]
            XY = [(Box[0][0] + Box[2][0]) / 2, (Box[0][1] + Box[2][1]) / 2]
            # print "X: ", XY[0]
            # print "Y: ", XY[1]
            pass
        # Comment out next 4 lines to avoid MySQLdb to simply read stream at console
        today = str(date.today())
        try:
            with open('tweets_' + today + '.json', 'a') as f:
                f.write(json.dumps(status._json))
                f.write('\n')
        except BaseException as e:
            print("Error on_data: %s" % str(e))

        print(XY[1])
        print(XY[0])
        print(text)
        # curr.execute("""INSERT INTO tweets (UserID, Tweet_Date, Lat, Lng, Text) VALUES
        # (%s, %s, %s, %s, %s);""",(status.id_str,status.created_at,XY[1],XY[0],text))
        # db.commit()

        # Alternatively write to CSV. CSV's. limited
        # csvwriter.writerow([unicode(status.id_str).encode("utf-8"),unicode(status.created_at).encode("utf-8"),XY[1],XY[0],unicode(status.text).encode("utf-8")])


def main():
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l, timeout=30.0)
    # Only records 'locations' OR 'tracks', NOT 'tracks (keywords) with locations'
    while True:
        try:
            # Call tweepy's userstream method 
            # Use either locations or track, not both
            # stream.filter(locations=[-125,25,-65,48])##These coordinates are approximate bounding box around USA
            # "41.1863288879395", "42.8867149353027", "-73.5081481933594", "-69.8615341186523"
            # stream.filter(locations=[42.3902, -71.1293, 42.3312, -71.0228])
            stream.filter(locations=[-73.5081, 41.2381, -69.9282, 42.8868])
            # stream.filter(track=['obama'])## This will feed the stream all mentions of 'keyword'
            break
        except Exception as e:

            # Abnormal exit: Reconnect
            nsecs = random.randint(60, 63)
            time.sleep(nsecs)


if __name__ == '__main__':
    main()
