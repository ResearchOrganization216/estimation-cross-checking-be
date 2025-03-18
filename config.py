class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@34.142.175.163:5432/InnoAInsure'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BUCKET_NAME = "innoainsure-bucket"
    KEY_PATH = ""  # Set to an empty string in production
    PROJECT_ID = "innoainsure-project"
    SECRET_KEY = 'your-very-secret-key'
