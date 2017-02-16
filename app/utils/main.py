intial_row = [
	"channel_id",
	"channel_title",
	"channel_url",
	"channel_subCount",
	"channel_videoCount",
	"channel_viewCount",
	"video1",
	"video1_commentCount",
	"video1_description",
	"video1_title",
	"video1_url",
	"video1_viewCount",
	"video2",
	"video2_commentCount",
	"video2_description",
	"video2_title",
	"video2_url",
	"video2_viewCount",
	"video3",
	"video3_commentCount",
	"video3_description",
	"video3_title",
	"video3_url",
	"video3_viewCount",
	"video4",
	"video4_commentCount",
	"video4_description",
	"video4_title",
	"video4_url",
	"video4_viewCount",
	"video5",
	"video5_commentCount",
	"video5_description",
	"video5_title",
	"video5_url",
	"video5_viewCount"
]

def allowed_file_ext(filename,ext):
	return '.' in filename and filename.rsplit('.',1)[1].lower() in ext

def structure_data(dataArray):
	resultArray = []
	count = 0
	for obj in dataArray:
		if count == 0:
			resultArray.append(intial_row)	
			count = 1
		rowData = []
		for key in intial_row:
			if key in obj:
				rowData.append(obj[key])
			else:
				rowData.append('N/A')
		resultArray.append(rowData)
	return resultArray
