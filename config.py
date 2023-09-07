# core/config.py

import os

class Config:
    """Base configuration class. Uses environment variables where available."""
    
    # Default to local PostgreSQL installation with your credentials
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:12234@localhost:5432/tripalytics")

class DevelopmentConfig(Config):
    """Development configuration - for local development environment."""
    
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    """Testing configuration - for unit tests and integration tests."""
    
    DEBUG = False
    TESTING = True
    DATABASE_URL = os.getenv("TEST_DATABASE_URL", "postgresql://postgres:12234@localhost:5432/tripalytics_test")

class ProductionConfig(Config):
    """Production configuration - for deployment."""
    
    DEBUG = False
    TESTING = False

# Depending on the environment, use the appropriate configuration
config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)
