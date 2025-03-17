class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@34.87.71.212:5432/InnoAInsure'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BUCKET_NAME = "innoainsure-project-bucket" 
     # For local development, provide a key file; in production, you can set this to an empty string or None.
    #KEY_PATH = "C:\\Users\\Sithija\\Documents\\keyfiles\\innoainsure-project-531bfaa81104.json"
    KEY_PATH = ""  # Set to an empty string in production
    PROJECT_ID = "innoainsure-project"
    SECRET_KEY = 'your-very-secret-key'
