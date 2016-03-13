#!/usr/bin/python
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import json
import redis

# Establish the connection with Redis first to avoid multiple connections.
global conn
conn = redis.Redis()
conn.flushall()


def main():
    # Authentication information for Twitter API
    consumer_key = ""
    consumer_secret = ""
    access_token = ""
    access_key = ""

    # Setup the authentication handler of Twitter API
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_key)

    # Start the real_time streaming from twitter, which calls the modified Listener Class at the bottom
    twitter_stream = Stream(auth, Listener())

    # This filter limits the tweets from the following location, a rectangle that covers the whole world
    twitter_stream.filter(locations=[-180, -90, 180, 90], async=False)


class Listener(StreamListener):
    # This methods overrides the existing one, which will be run once a new tweet is captured.
    def on_data(self, data):
        # Utilizing global variables to avoid multiple connections to Redis
        global conn

        # Use JSON to parse received data, which contains multiple information of the tweet.
        received_data = json.loads(data)

        # Use "try" to filter the data with geo-locations only
        try:
            # Latitude and Longitude of the current tweet
            lat = float(received_data['geo']['coordinates'][0])
            lng = float(received_data['geo']['coordinates'][1])

            # Count the tweets in different regions
            # North America
            if 8 <= lat <= 85 and -167 <= lng <= -30:
                conn.incr("North America", 1)
            # South America
            elif -58 <= lat < 8 and -95 <= lng <= -30:
                conn.incr("South America", 1)
            # Europe
            elif 36 <= lat <= 85 and -30 <= lng <= 40:
                conn.incr("Europe", 1)
            # Africa
            elif (-38 <= lat < 36 and -20 <= lng <= 32.3) or (-38 <= lat < 12.6 and 32.2 <= lng <= 55):
                conn.incr("Africa", 1)
            # Oceania
            elif 116 <= lat <= 180 and -50 <= lat <= -10.5:
                conn.incr("Oceania", 1)
            # Asia (including P.R.China and others)
            elif (12.6 <= lat < 36 and 32.3 < lng <= 40) or (-10.5 <= lat < 85 and -40 < lng <= 180):
                # P.R.China
                if (42 <= lat <= 50 and 115.5 <= lng <= 130) or (28 <= lat < 42 and 80 <= lng <= 124) or (
                            23 <= lat < 28 and 99 <= lng <= 120) or (18 <= lat < 23 and 108 <= lng <= 118):

                    # Excluding Hongkong and Macau, because they are not under censorship
                    if (21.8 <= lat <= 22.5 and 113.6 <= lng <= 114.4) or (
                                22 <= lat <= 22.22 and 113.43 <= lng <= 113.6):
                        conn.incr("Asia", 1)
                    else:
                        conn.incr("China", 1)
                # Rest of Asia
                else:
                    conn.incr("Asia", 1)
        except:
            pass
        return True

    def on_error(self, status):
        print status


if __name__ == "__main__":
    main()
