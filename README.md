

TubesTrends
========================
This was an UCB I School Spring 2014 290 Data Mining Final Project

This project collects information about internet “trending” data from major web platforms and social networks hopes to the following purposes:

-to create an nosql/mongo db of world-trends that give gives a way to both see trends occur inreal time (instantaneous) and think about trends in the long-term (over a course of a week, month, year, etc)
-map internet trending data to the geographical coordinates of latitude and longitude how the data pieces geographically relate to each other;
-provide a way for users to compare and contrast what's “trending” on different search platforms and social networks to see if there are common themes
-show the duration of time that items/topics/people/ideas/places/stories are popular/trending on the Internet
-to illuminate a potential “zeitgeist” that may or may not exist on the internet or in the world.

General Design: 
To gather the data, mentioned above, I wrote ruby scripts that collected the trend data, parsed the trend
data, and then dumb the data into a mongo db database. From an amazon ec2, server, I deployed these the
ruby scripts to run at regular intervals using the cron-tab. Below, I list a few details about how I
implemented of my database system. Additionally, all the scripts for this project included in the classes dir, in case you'd like to see how they were exactly implemented.

Data Sources:

Twitter → http://www.twitter.com → social networking platform
API resource, GET trends/available
Returns the locations that Twitter has trending topic information for.
API resource, GET trends/place
Each API call returns the top 10 trending topics for a a specific yahoo WOEID that trending data is available for.

Google Hot Trends → http://www.google.com/trends/hottrends → search engine site
Google releases the number of people that searching for different topics I was able to get the trend data for the other 7 countries by writing a ruby script that scraped the Google hot trend web site.

Youtube → http://www.youtube.com → video search engine
API resource, GET Most Popular
API returns the feed of the most popular videos for the past day
Also can return the most popular videos for a particular geographical region for the past day; Data for 39 countries is availible

Instagram → http://www.instagram.com → photo sharing social networking platform
API resource, GET Most Popular
This API gets a list of what media is most popular at the moment. Can return mix of image and video types. API will also return the latitude and longitude coordinates of popular item when availible.

Yahoo Where On Earth Id → Geographical/Mapping Data Source →
http://developer.yahoo.com/geo/geoplanet/guide/concepts.html
A yahoo Where On Earth ID (WOEID). Is a unique identifier that is assigned geographical entities on earth; this id is never changed; it acts as unique identifier for a specific place on earth.

Results: 
This ETL tool will gather internet trending data and dump it into a mongodb nosql database. 
The database can be use to do such things as:

1. Show, in the past 5 days, what and in what countries have Google and twitter had similar trend items
2. Find the 35 highest trending/most talked items in the database
3.Get Twitter Trending Data, google hot trends, data, youtube trend data and instragram popular data for specific days/times for specific geographic locations


