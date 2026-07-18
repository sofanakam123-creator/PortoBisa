import cloudinary.uploader
from werkzeug.utils import secure_filename

def upload_image(file):
    if not file:
        return None
    try:
        # Uploads file to Cloudinary and returns the URL
        result = cloudinary.uploader.upload(file)
        return result.get('secure_url')
    except Exception as e:
        print(f"Error uploading to cloudinary: {e}")
        return None
