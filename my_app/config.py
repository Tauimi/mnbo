"""
Конфигурация приложения
"""
import os
from pathlib import Path

# Базовый каталог проекта
BASE_DIR = Path(__file__).resolve().parent.parent

class Config:
    """Базовая конфигурация"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Конфигурация для загрузки файлов
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'my_app', 'static', 'images')
    PRODUCT_IMAGES = os.path.join(UPLOAD_FOLDER, 'products')
    CATEGORY_IMAGES = os.path.join(UPLOAD_FOLDER, 'categories')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    @staticmethod
    def init_app(app):
        """Инициализация приложения на основе конфигурации"""
        # Создаем директории для загрузки, если они не существуют
        os.makedirs(app.config['PRODUCT_IMAGES'], exist_ok=True)
        os.makedirs(app.config['CATEGORY_IMAGES'], exist_ok=True)

class DevelopmentConfig(Config):
    """Конфигурация для разработки"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{BASE_DIR / "dev.db"}'

class ProductionConfig(Config):
    """Конфигурация для продакшена"""
    DEBUG = False
    
    # PostgreSQL для продакшена на Railway
    DATABASE_URL = os.getenv('DATABASE_URL', '')
    if DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://')
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL or f'sqlite:///{BASE_DIR / "prod.db"}'
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True

# Словарь доступных конфигураций
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 