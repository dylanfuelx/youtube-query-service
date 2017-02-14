def allowed_file_ext(filename,ext):
	return '.' in filename and filename.rsplit('.',1)[1].lower() in ext

def structure_data(dataArray):
	resultArray = []
	count = 0
	for obj in dataArray:
		if count == 0:
			rowData = []
			count = 1
			for key in obj:
				rowData.append(key)
			resultArray.append(rowData)	
		rowData = []
		for key in obj:
			rowData.append(obj[key])
		resultArray.append(rowData)
	return resultArray