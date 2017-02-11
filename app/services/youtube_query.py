from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

DEVELOPER_KEY = "AIzaSyAkvSkDeCD7e76Yrur2L3rfO6JoifPP4S0"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(query):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.

  channel = {}
  search_response = youtube.search().list(
    q=query,
    part="snippet",
    type="channel",
    maxResults=1
  ).execute()


  resultArray= search_response['items']

  channel['title'] = resultArray[0]['snippet']['channelTitle']
  channel['id'] = resultArray[0]['snippet']['channelId']
  channel['url'] = "https://www.youtube.com/channel/{}".format(channel['id'])

  channel_response = youtube.channels().list(
  	part='statistics',
  	id= channel['id'],
  	maxResults=1
  ).execute()

  channelResultArray = channel_response['items']

  channel['viewCount'] = channelResultArray[0]['statistics']['viewCount']
  channel['subCount'] = channelResultArray[0]['statistics']['subscriberCount']
  channel['videoCount'] = channelResultArray[0]['statistics']['videoCount']

  video_response = youtube.search().list(
  	part='snippet',
  	channelId=channel['id'],
  	order='viewCount',
  	type='video',
  	maxResults=5
  ).execute()

  videoResultArray = video_response['items']
  count = 1
  for video in videoResultArray:

  	channel['video' + str(count)] = video['id']['videoId']
  	channel['video' + str(count) + '-title'] = video['snippet']['title']
  	channel['video' + str(count) + '-description'] = video['snippet']['description']


  	videoid_response = youtube.videos().list(
  		part='statistics',
  		id=channel['video' + str(count)]
  	).execute()

  	videoIdResultArray = videoid_response['items']

  	channel['video' + str(count) + '-viewCount'] = videoIdResultArray[0]["statistics"]['viewCount']
  	if 'commentCount' in videoIdResultArray[0]["statistics"]:
  		channel['video' + str(count) + '-commentCount'] = videoIdResultArray[0]["statistics"]['commentCount'] 
  	else:
  		channel['video' + str(count) + '-commentCount'] = 0
  	#channel['video' + str(count) + 'likeCount'] = videoIdResultArray[0]["statistics"]['likeCount']

  	count += 1

  return channel

