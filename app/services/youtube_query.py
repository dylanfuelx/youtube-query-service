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

	# This first call to youtube brings back details about the channel matching the company name being queried

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

	# Second Youtube query pulls down a list of videos for a given channel.
	# For whatever reason, the video list does not contain the meta data for the videos returned.
	# the API's videoDuration filter only takes three parameters, and, at the shortest, filter videos < 4 min

	video_response = youtube.search().list(
		part='snippet',
		channelId=channel['channel_id'],
		order='viewCount',
		type='video',
		maxResults=15,
		videoDuration='short'
	).execute()

	videoResultArray = video_response['items']
	count = 1
	for video in videoResultArray:
		if count > 5:
			continue

		videoNum = 'video' + str(count)

		# Here's where we finally get the specific data for each video

		videoid_response = youtube.videos().list(
			part='statistics,contentDetails',
			id=video['id']['videoId']
		).execute()

		videoIdResultArray = videoid_response['items'][0]
		videoDuration = videoIdResultArray['contentDetails']['duration']

		# Video duration has an odd format from Youtube: PT#H#M#S
		# If the video is less than 1 minute in length, this becomes: PT#S

		if len(videoDuration) > 5:
			continue

		channel[videoNum + '_url'] = "https://www.youtube.com/watch?v={}".format(video['id']['videoId'])
		channel[videoNum] = video['id']['videoId']
		channel[videoNum + '_title'] = video['snippet']['title']
		channel[videoNum + '_description'] = video['snippet']['description']
		channel[videoNum + '_published_at'] = video['snippet']['publishedAt']
		channel[videoNum + '_viewCount'] = videoIdResultArray["statistics"]['viewCount']
		channel[videoNum + '_duration (seconds)'] = int(videoDuration[2:4])

		if 'commentCount' in videoIdResultArray["statistics"]:
			channel[videoNum + '_commentCount'] = videoIdResultArray["statistics"]['commentCount'] 
		else:
			channel[videoNum + '_commentCount'] = 0
		#channel[videoNum + 'likeCount'] = videoIdResultArray["statistics"]['likeCount']

		count += 1

	return channel


