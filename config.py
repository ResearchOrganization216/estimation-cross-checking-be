class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@34.126.101.125:5432/InnoAInsure'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BUCKET_NAME = "innoa-bucket"
    KEY_PATH = ""  # Set to an empty string in production
    PROJECT_ID = "innoainsure-project-43"
    SECRET_KEY = 'your-very-secret-key'
