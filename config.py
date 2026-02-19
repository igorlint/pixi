import os
from dotenv import load_dotenv

load_dotenv()

class Config:
      SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-prod'
      SQLALCHEMY_TRACK_MODIFICATIONS = False
      SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://localhost/confighub'

class DevelopmentConfig(Config):
      DEBUG = True

class TestingConfig(Config):
      TESTING = True
      SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
      DEBUG = False

config_by_name = {
      'development': DevelopmentConfig,
      'testing': TestingConfig,
      'production': ProductionConfig,
      'default': DevelopmentConfig
}
