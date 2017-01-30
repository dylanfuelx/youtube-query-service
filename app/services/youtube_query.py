from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

DEVELOPER_KEY = "AIzaSyAkvSkDeCD7e76Yrur2L3rfO6JoifPP4S0"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search():
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.

  channel = {}

  search_response = youtube.search().list(
    q='oracle',
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

  channelResultArray= channel_response['items']

  channel['viewCount'] = channelResultArray[0]['statistics']['viewCount']
  channel['subCount'] = channelResultArray[0]['statistics']['subscriberCount']
  channel['videoCount'] = channelResultArray[0]['statistics']['videoCount']

  return channel

