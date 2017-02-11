def allowed_file_ext(filename,ext):
	return '.' in filename and filename.rsplit('.',1)[1].lower() in ext