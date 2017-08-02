def allowed_file_ext(filename,ext):
	return '.' in filename and filename.rsplit('.',1)[1].lower() in ext

def structure_data(dataArray):
	resultArray = []
	count = 0
	for obj in dataArray:
		if count == 0:
			columnHeaders = sorted(obj.keys())
			resultArray.append(columnHeaders)	
			count = 1
		rowData = []
		for key in columnHeaders:
			if key in obj:
				rowData.append(obj[key])
			else:
				rowData.append('N/A')
		resultArray.append(rowData)
	return resultArray
