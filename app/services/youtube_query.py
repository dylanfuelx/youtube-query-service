from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

DEVELOPER_KEY = "AIzaSyDoc2019UguyagSyPpaMKCu3fHLTjT6a4g"
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

	channel['channel_title'] = resultArray[0]['snippet']['channelTitle']
	channel['channel_id'] = resultArray[0]['snippet']['channelId']
	channel['channel_url'] = "https://www.youtube.com/channel/{}".format(channel['channel_id'])

	channel_response = youtube.channels().list(
		part='statistics',
		id= channel['channel_id'],
		maxResults=1
	).execute()

	channelResultArray = channel_response['items']

	channel['channel_viewCount'] = channelResultArray[0]['statistics']['viewCount']
	channel['channel_subCount'] = channelResultArray[0]['statistics']['subscriberCount']
	channel['channel_videoCount'] = channelResultArray[0]['statistics']['videoCount']

	video_response = youtube.search().list(
		part='snippet',
		channelId=channel['channel_id'],
		order='viewCount',
		type='video',
		maxResults=5,
		videoDuration='short'
	).execute()

	videoResultArray = video_response['items']
	count = 1
	for video in videoResultArray:

		videoNum = 'video' + str(count)

		videoid_response = youtube.videos().list(
			part='statistics,contentDetails',
			id=video['id']['videoId']
		).execute()

		videoIdResultArray = videoid_response['items'][0]

		channel[videoNum + '_url'] = "https://www.youtube.com/watch?v={}".format(video['id']['videoId'])
		channel[videoNum] = video['id']['videoId']
		channel[videoNum + '_title'] = video['snippet']['title']
		channel[videoNum + '_description'] = video['snippet']['description']
		channel[videoNum + '_viewCount'] = videoIdResultArray["statistics"]['viewCount']
		channel[videoNum + '_duration'] = videoIdResultArray['contentDetails']['duration']

		if 'commentCount' in videoIdResultArray["statistics"]:
			channel[videoNum + '_commentCount'] = videoIdResultArray["statistics"]['commentCount'] 
		else:
			channel[videoNum + '_commentCount'] = 0
		#channel[videoNum + 'likeCount'] = videoIdResultArray["statistics"]['likeCount']

		count += 1

	return channel


