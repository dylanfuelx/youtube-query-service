from app import app
import uuid
	
app.secret_key = str(uuid.uuid4())

if __name__ == '__main__':
	app.run()