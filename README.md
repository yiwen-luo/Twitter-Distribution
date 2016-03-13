# TwitterDistribution

### Introduction
The censorship in Mainland China has been established since late 1990s and nowadays there are many websites not accessible from Mainland China, like Google, Facebook and Twitter. This application will tell whether the sensorship is relaxed a little by monitoring ratio of Tweet from Mainland China.

The application consists of four main parts, the data streaming part, the decrement part, the API part, and data visualization and alerting part, where the data steaming part retrieves and parses the data in real-time, the decrement part keeps decrementing counts at a constant rate to normalize the data, the API part provides the distribution, entropy and probability preception of the data, and .

Main technology involved are: Tweepy API, Redis, Python, Flask, JavaScript, HTML5, CanvasJS.


### Components of Application
#### Distribution of Data
This part is done by "tweet_continent_insert.py"
- The data streaming part retrieves tweets all around the world with geographic locations from Twitter in realtime. By precisely selecting the location of the tweets, the tweets are categorized into the following locations: North America, South America, Europe, Africa, Asia (except Mainland China), Mainland China. After that, the counter of that area will be incremented by 1 in Redis server. The message stored in Redis includes two informaiton, the area name and the tweets count in that area.

This part is done by "tweet_continent_decrement.py"
- Another decrement file decrement the each of the count for areas by 1 every two seconds. This is to ensure the count will be normalized and for a better distribution.


#### API
This part is done by "tweet_continent_api.py"
- The API part runs Python Flask on port 5000. It retrieves tuples from Redis and calculate the distrubtion of each of the area's tweets ratio by providing API at "/". Also, it calculates the entropy of the distribution and provids API at "/entropy". In addtion, it provides the probability API at "/probability" where the request parameter should be the area name and the return value will be the probability of the tweet posts in that area.


#### Alerting
This part is with the front end

#### Web




