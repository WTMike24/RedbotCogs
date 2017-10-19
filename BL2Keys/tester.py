import tweepy, re, datetime
from tweepy import OAuthHandler
from time import sleep
from oauth import *

#Secret keys
# Keys are now imported from oauth.py stored next to this file. oauth.py is included, but keys are not provided

#Create our authentication
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token,access_secret)
api = tweepy.API(auth)

#Create regex stuff
dateRegex = re.compile("\d{4}-(\d{2})-(\d{2}) \d{2}:\d{2}:\d{2}\.\d+")
keyRegex = re.compile(".*Mac: (([A-Z0-9]{5}-*){5}).*XBOne: (([A-Z0-9]{5}-*){5}).*PS Vita: (([A-Z0-9]{5}-*){5})'")
expireRegex = re.compile("Active through (\d+\/\d+)")

#Begin
print("BEGIN\n")

raw_tweets = api.user_timeline(screen_name = 'Borderlands', count=250)
#2D array taken from https://gist.github.com/yanofsky/5436496
tweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in raw_tweets]
index = 0
#Go through the tweets and print the code tweets and the expirey tweets for BL2
for tweet in tweets:
	sleep(0.01)
	if "BL2" in str(tweet[2]):
		if "Unlock" not in str(tweets[index+1][2]):
			#This is if the expiration code tweet isn't where we expect it to be, TODO: search for tweet within 2 tweets on either side, if not found, expirey unknown
			print("------------------ERROR------------------")
			# for c in range(9):
			# 	q = c-4
			# 	print("# " + str(index+q) + " -- " + str(tweets[index+q][2]))
			print("-------------------END-------------------")
		else:
			keyResults = keyRegex.search(str(tweet[2]))
			if keyResults:
				keyResults = keyResults.groups()
				list = []
				for c in range(len(keyResults)):
					if c % 2 == 0:
						list.append(str(keyResults[c]));
				print(list)
			else:
				print(tweet[2])	#Code tweet
				print(tweets[index + 1][2])	#expirey tweet
	index += 1
#print('\nEND', end='')
