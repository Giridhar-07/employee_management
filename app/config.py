import os
from datetime import timedelta

class Config:
    """Base configuration"""
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-this-in-production'
    
    # Database - Supports both SQLite and PostgreSQL
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///company.db'
    # Fix PostgreSQL URI if needed (postgres:// is deprecated, use postgresql://)
    if DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'max_overflow': 20,
    }
    
    # Session Configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=int(os.environ.get('PERMANENT_SESSION_LIFETIME', 7)))
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'True') == 'True'
    SESSION_COOKIE_HTTPONLY = os.environ.get('SESSION_COOKIE_HTTPONLY', 'True') == 'True'
    SESSION_COOKIE_SAMESITE = os.environ.get('SESSION_COOKIE_SAMESITE', 'Lax')
    
    # Security Headers
    PREFERRED_URL_SCHEME = 'https'
    
    # JSON Configuration
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = False


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    SQLALCHEMY_ECHO = True
    SESSION_COOKIE_SECURE = False
    PREFERRED_URL_SCHEME = 'http'


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_ECHO = False
    # Enforce security in production
    SESSION_COOKIE_SECURE = True
    PREFERRED_URL_SCHEME = 'https'


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
