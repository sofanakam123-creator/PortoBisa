import os
from dotenv import load_dotenv
import cloudinary

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    
    # TiDB Connection Details
    TIDB_HOST = os.getenv('TIDB_HOST')
    TIDB_PORT = int(os.getenv('TIDB_PORT', 4000))
    TIDB_USER = os.getenv('TIDB_USER')
    TIDB_PASSWORD = os.getenv('TIDB_PASSWORD')
    TIDB_DB_NAME = os.getenv('TIDB_DB_NAME', 'portofolio_db')

    # Cloudinary configuration
    cloudinary.config( 
        cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME'), 
        api_key = os.getenv('CLOUDINARY_API_KEY'), 
        api_secret = os.getenv('CLOUDINARY_API_SECRET'),
        secure=True
    )
    
    # Resend configuration
    RESEND_API_KEY = os.getenv('RESEND_API_KEY')
