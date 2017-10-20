import tweepy, re, datetime, os, sys
from tweepy import OAuthHandler
from time import sleep
from oauth import *

#Secret keys
#Keys are now stored in oauth.py

#Kinda want this to also be a standalone version, so if you're on linux, you get colors!
if (os.name == 'nt'):
	none = ''
	bold = ''
	underline = ''

	red = ''
	green = ''
	yellow = ''
	blue = ''
	purple = ''
	cyan = ''
	white = ''
	reset = ''
else:
	none = '\x1b[0;'
	bold = '\x1b[1;'
	underline = '\x1b[4;'

	red = '31;40m'
	green = '32;40m'
	yellow = '33;40m'
	blue = '34;40m'
	purple = '35;40m'
	cyan = '36;40m'
	white = '37;40m'
	reset = '\x1b[0m'

#Create regex stuff
dateRegex = re.compile("\d{4}-(\d{2})-(\d{2}) \d{2}:\d{2}:\d{2}\.\d+")
keyRegex = re.compile(".*Mac: (([A-Z0-9]{5}-*){5}).*XBOne: (([A-Z0-9]{5}-*){5}).*PS Vita: (([A-Z0-9]{5}-*){5})'")
expireRegex = re.compile("Active through (\d+)\/(\d+)")

#Global variables
keys = []
expire = []
mode = 0
today = dateRegex.search(str(datetime.datetime.now())).groups()

#Do we display all or just the valid ones? Valid only is default
if ("--all" in sys.argv or '-a' in sys.argv):
	mode = 1

#Create our authentication
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token,access_secret)
api = tweepy.API(auth)

#Begin
print(none+green+"BEGIN\n"+reset)
raw_tweets = api.user_timeline(screen_name = 'Borderlands', count=250)

#2D array taken from https://gist.github.com/yanofsky/5436496
tweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in raw_tweets]

#Go through the tweets and print the code tweets and the expirey tweets for BL2
index = 0
for tweet in tweets:
	sleep(0.01)
	if "BL2" in str(tweet[2]):
		if "Unlock" not in str(tweets[index+1][2]):
			#This is if the expiration code tweet isn't where we expect it to be, TODO: search for tweet within 2 tweets on either side, if not found, expirey unknown
			# print("------------------ERROR------------------")
			# for c in range(9):
			# 	q = c-4
			# 	print("# " + str(index+q) + " -- " + str(tweets[index+q][2]))
			# print("-------------------END-------------------")
			continue
		else:
			#Attempt to extract the key from the tweet
			keyResults = keyRegex.search(str(tweet[2]))
			#Check to see if we can extract the keys from the tweet
			#keyResults == None if we can't
			if keyResults:
				#We got it! make groups so we can extract the keys
				keyResults = keyResults.groups()
				list = []
				for c in range(len(keyResults)):
					#Because of my regex string, only the even ones are the full keys
					if c % 2 == 0:
						list.append(str(keyResults[c]));
				keys.append(list)
				#Now we gotta get the expiration date
				expireResults = expireRegex.search(str(tweets[index+1][2]))
				#Make sure the regex worked (it should)
				if expireResults:
					expireResults = expireResults.groups()

				else:
					print(bold+red+"Something broke with the expiration regex, pls help"+reset)
					print(none+red+"regex: " + str(expireRegex)+reset)
					print(none+red+"tweet: " + str(tweets[index+1][2])+reset)
			#regex broke, what's our data
			else:
				print(bold+red+"Something broke with the key regex, pls help"+reset)
				print(none+red+"regex: " + str(keyRegex)+reset)
				print(none+red+"tweet: " + str(tweet[2])+reset)
	index += 1
#Don't print a newline at the end for windows, print a newline for linux
if 'nt' not in os.name:
	print(none+green+'\nEND'+reset)
else:
	print(none+green+'\nEND'+reset, end='')
