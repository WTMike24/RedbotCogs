import tweepy, re, datetime, os, sys
from tweepy import OAuthHandler
from time import sleep
from oauth import *
from constants import *

#Kinda want this to also be a standalone version, so if you're on linux, you get colors!
if ((os.name == 'nt' or '--nocolor' in sys.argv) and '--forcecolor' not in sys.argv):
	none, bold, underline = '', '', ''
	red, yellow, green, cyan, blue, purple, white, reset = '', '', '', '', '', '', '', ''
else:
	none, bold, underline = '\x1b[0;', '\x1b[1;', '\x1b[4;'
	red, green, yellow, blue, purple, cyan, white, reset = '31m', '32m', '33m', '34m', '35m', '36m', '37m', '\x1b[0m'
	#Hijack the OS check to disable the cursor on linux systems
	if '--debug' in sys.argv:
		os.system('setterm -cursor off')

#Global variables
#Basic variables for processing
keys, ids, expires, tweets = [], [], [], []
today = dateRegex.search(str(datetime.datetime.now())).groups()
showAll, printLine, latest, last = 0, 0, 0, 0
printData = ''
newOnly = 1 if '--new' in sys.argv else 0
#For storing/accessing data
fileData = 'data/borderlands/'

#-----Function calls because they have to go before the executed code :(-----
def getTweets():
	global tweets
	log('Downloading tweets...\t\t\t')
	#If we request anything above 200, we only get 200, so why bother trying
	raw_tweets = api.user_timeline(screen_name = 'Borderlands', count=200)
	#2D array taken from https://gist.github.com/yanofsky/5436496
	tweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in raw_tweets]

def extractTweets(keyTweet, expireyTweet):
	global keys
	global expires
	#Attempt to extract the key from the tweet
	keyResults = keyRegex.search(str(keyTweet))
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
		expireResults = expireRegex.search(str(expireyTweet))
		#Make sure the regex worked (it should)
		if expireResults:
			expireResults = expireResults.groups()
			expires.append(expireResults)
		else:
			print(bold+red+"Something broke with the expiration regex, pls fix"+reset)
			print(none+red+"regex: " + str(expireRegex)+reset)
			print(none+red+"tweet: " + str(tweets[index+1][2])+reset)
	#regex broke, what's our data
	else:
		print(bold+red+"Something broke with the key regex, pls fix"+reset)
		print(none+red+"regex: " + str(keyRegex)+reset)
		print(none+red+"tweet: " + str(tweet[2])+reset)

#This function will handle neatening up the output
def printer(data, working):
	log('Displaying tweets...\t\t\t')
	#Gotta use global variables or we won't actually get anything done
	global printData
	global keyMode
	barColor = none+blue
	headerColor = bold+blue
	#Set up the top 3 lines of the table
	printData += reset
	if keyMode == 1 or keyMode == 2 or keyMode == 4:
		printData += barColor + barColor + str(bars['top'][0]) + '\n' + reset
		printData += barColor + str(bars['left']) + reset + headerColor + (str(headers['pc']) if keyMode == 1 else str(headers['xbone']) if keyMode == 2 else str(headers['ps4'])) + barColor + str(bars['right']) + '\n' + reset
		printData += barColor + str(bars['center'][0]) + '\n' + reset
	elif keyMode == 3 or keyMode == 5 or keyMode == 6:
		printData += barColor + str(bars['top'][1]) + '\n' + reset
		if keyMode == 3:
			printData += barColor + str(bars['left']) + headerColor + str(headers['pc']) + barColor + str(bars['middle']) + headerColor + str(headers['xbone']) + barColor + str(bars['right']) + '\n' + reset
		if keyMode == 5:
			printData += barColor + str(bars['left']) + headerColor + str(headers['pc']) + barColor + str(bars['middle']) + headerColor + str(headers['ps4']) + barColor + str(bars['right']) + '\n' + reset
		if keyMode == 6:
			printData += barColor + str(bars['left']) + headerColor + str(headers['xbone']) + barColor + str(bars['middle']) + headerColor + str(headers['ps4']) + barColor + str(bars['right']) + '\n' + reset
		printData += barColor + str(bars['center'][1]) + '\n' + reset
	elif keyMode == 7:
		printData += barColor + str(bars['top'][2]) + '\n' + reset
		printData += barColor + str(bars['left']) + headerColor + str(headers['pc']) + barColor + str(bars['middle']) + headerColor + str(headers['xbone']) + barColor + str(bars['middle']) + headerColor + str(headers['ps4']) + barColor + str(bars['right']) + '\n' + reset
		printData += barColor + str(bars['center'][2]) + '\n' + reset
	printData += reset

	#Loop through the keys we got and display them
	keyCount = 0
	for c in range(len(data)):
		if not showAll and not working[c]:
			continue
		elif int(tweets[c][0]) < latest and newOnly:
			continue
		else:
			keyCount += 1
			if keyMode == 1 or keyMode == 2 or keyMode == 4:
				printData += reset + barColor + str(bars['left']) + printerColor(working[c]) + (str(data[c][0]) if keyMode == 1 else str(data[c][1]) if keyMode == 2 else str(data[c][2])) + reset + barColor + str(bars['right']) + '\n' + reset
			elif keyMode == 3:
				printData += reset + barColor + str(bars['left']) + printerColor(working[c]) + str(data[c][0]) + reset + barColor + str(bars['middle']) + printerColor(working[c]) + str(data[c][1]) + reset + barColor + str(bars['right']) + '\n' + reset
			elif keyMode == 5:
				printData += reset + barColor + str(bars['left']) + printerColor(working[c]) + str(data[c][0]) + reset + barColor + str(bars['middle']) + printerColor(working[c]) + str(data[c][2]) + reset + barColor + str(bars['right']) + '\n' + reset
			elif keyMode == 6:
				printData += reset + barColor + str(bars['left']) + printerColor(working[c]) + str(data[c][1]) + reset + barColor + str(bars['middle']) + printerColor(working[c]) + str(data[c][2]) + reset + barColor + str(bars['right']) + '\n' + reset
			elif keyMode == 7:
				printData += reset + barColor + str(bars['left']) + printerColor(working[c]) + str(data[c][0]) + reset + barColor + str(bars['middle']) + printerColor(working[c]) + str(data[c][1]) + reset + barColor + str(bars['middle']) + printerColor(working[c]) + str(data[c][2]) + reset + barColor + str(bars['right']) + '\n' + reset

	if (keyCount == 0):
		if keyMode == 1 or keyMode == 2 or keyMode == 4:
			printData += reset + barColor + str(bars['left']) + none + red + str(headers['none']) + reset + barColor + str(bars['right']) + '\n' + reset
		elif keyMode == 3 or keyMode == 5 or keyMode == 6:
			printData += reset + barColor + str(bars['left']) + none + red + str(headers['none']) + reset + barColor + str(bars['middle']) + none + red +str(headers['none']) + reset + barColor + str(bars['right']) + '\n' + reset
		elif keyMode == 7:
			printData += reset + barColor + str(bars['left']) + none + red +str(headers['none']) + reset + barColor + str(bars['middle']) + none + red +str(headers['none']) + reset + barColor + str(bars['middle']) + none + red +str(headers['none']) + reset + barColor + str(bars['right']) + '\n' + reset

	#Stick the bottom of the table on
	printData += reset + barColor + (str(bars['bottom'][0]) if (keyMode == 1 or keyMode == 2 or keyMode == 4) else str(bars['bottom'][1]) if (keyMode == 3 or keyMode == 5 or keyMode == 6) else str(bars['bottom'][2])) + reset

	print(printData)

def printerColor(data):
	return none + (yellow if data and data == 2 else green if data else red)

def debug(data):
	if '--debug' in sys.argv:
		print(bold+purple+str(data)+reset, end='')

def log(text):
	print(none+purple+text+reset, end='\r')

def _writeFile(data, filename='tester.dat'):
	dataFile = open(filename, 'w')
	dataFile.write(str(data))
	dataFile.close()

def _readFile(filename='tester.dat'):
	dataFile = open(filename, 'r')
	data = int(dataFile.read())
	dataFile.close()
	return data
#Cheesy way to see if the file exists (try to open it, if we can't, it's not there)
def _fileExists(filename='tester.dat'):
	data = 0
	try:
		dataFile = open(filename,'r')
		data = int(dataFile.read())
		dataFile.close()
		ex=1
	except:
		ex=0
	return (ex,data)
#-----No more functions :D-----

#Everything needs help text!
if '--help' in sys.argv:
	helptext = ''
	helptext += '\n'+bold+yellow+'Welcome to a key reader for Borderlands 2 Golden Crate Keys!'
	helptext += '\nThis program searches the Borderlands twitter and pulls down'
	helptext += '\nGolden Crate keys for Borderlands 2.'+reset+none+yellow
	helptext += '\n\nThere are a few options you can use to change how this runs:'
	helptext += '\n\n--help\t\tDisplays this help message and exits'
	helptext += '\n--all\t\tDisplays all keys, expired or not, and specifies activeness'
	helptext += '\n--new\t\tDisplays only new keys since this was last run'
	helptext += '\n--nocolor\tDisables the use of colors in the output.'
	helptext += '\n--forcecolor\tForces the use of ansi color codes in the output'
	helptext += '\n\n--pc\tDisplays keys only for PC   \\'
	helptext += '\n--ps4\tDisplays keys only for PS4   }Can be combined to show multiple consoles'
	helptext += '\n--xbox\tDisplays keys only for XBox /'
	helptext += bold+yellow+'\n\nThe default settings are as follows:'
	helptext += '\n\nDisplay only active keys (not --all)\nDisplay only PC keys\t (--pc)\nUse colors on Linux\nAll active keys\t\t (not --new)'

	print(none+yellow+helptext+reset)
	sys.exit()

#Do we display all or just the valid ones? Valid only is default
if ('--all' in sys.argv or '-a' in sys.argv):
	showAll = 1
#We're gonna use numbers like unix rwx to check pc/xbone/ps, PC is default
keyMode = 1
if ('--pc' not in sys.argv and ('--ps4' in sys.argv or '--xbox' in sys.argv)):
	keyMode = 0
if '--ps4' in sys.argv:
	keyMode += 4
if '--xbox' in sys.argv:
	keyMode += 2

#Create our authentication
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token,access_secret)
api = tweepy.API(auth)

#Begin
debug("BEGIN\n\n")
log('Loading...\t\t\t')
getTweets()

latest = _fileExists()[1]
last = int(tweets[len(tweets)-1][0])
if (last > latest):
	_writeFile(last)

log('Searching tweets...\t\t\t')
#Go through the tweets and print the code tweets and the expirey tweets for BL2
index = 0
for tweet in tweets:
	if "BL2" in str(tweet[2]):
		#If index+1 is equal to the length of the array, we're done. An index at the length is 1 beyond the last index
		if index+1 == len(tweets):
			#Break out of the for loop, there's no point in going further
			break
		if "Unlock" not in str(tweets[index+1][2]):
			#This is if the expiration code tweet isn't where we expect it to be
			#Search 9 tweets (4 under, 4 above, code is the 1 in the center)
			for c in range(9):
				q = c-4
				if "Unlock" in str(tweets[index-q][2]) and "Borderlands 2" in str(tweets[index-q][2]):
					extractTweets(tweet[2], tweets[index-q][2])
					break
		else:
			#Pass the tweets required to a function that parses and stores the data we need
			extractTweets(tweet[2], tweets[index+1][2])
	index += 1
	debug(str(index)+"\r")
#Go through and display them, red for dead (only show if --all), yellow for dieing today, green for good
working = []
log('Sorting tweets...\t\t\t')
for c in range(len(keys)):
	expire = expires[c]
	if ((today[0] > expire[0] and today[1] > expire[1]) or (today[0] > expire[0])):
		working.append(0)
	elif (today[0] == expire[0] and today[1] > expire[1]):
		working.append(0)
	elif (today[0] == expire[0] and today[1] == expire[1]):
		working.append(2)
	else:
		working.append(1)
printer(keys, working)

#Don't print a newline at the end for windows, print a newline for linux
if 'nt' not in os.name:
	debug('\nEND\n')
	#Enable the cursor again so we don't get in trouble
	os.system('setterm -cursor on')
else:
	debug('\nEND')
