"""
SosyalAI Veritabanı Bağlantısı ve Session Yönetimi
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.settings import settings
import logging

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Veritabanı engine oluştur
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
    echo=settings.DEBUG
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base model
Base = declarative_base()

def get_db():
    """Veritabanı session'ı döndür"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Veritabanını başlat ve tabloları oluştur"""
    try:
        # Import all models to ensure they are registered
        from .models import (
            User, SocialAccount, ContentPost, ScheduledPost, 
            PerformanceMetric, TrendAnalysis, AIContentGeneration, PostingStrategy
        )
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Veritabanı tabloları başarıyla oluşturuldu")
        
    except Exception as e:
        logger.error(f"Veritabanı başlatma hatası: {e}")
        raise

def check_db_connection():
    """Veritabanı bağlantısını test et"""
    try:
        with engine.connect() as connection:
            result = connection.execute("SELECT 1")
            logger.info("Veritabanı bağlantısı başarılı")
            return True
    except Exception as e:
        logger.error(f"Veritabanı bağlantı hatası: {e}")
        return False

# Veritabanı başlat
if __name__ == "__main__":
    init_db()
    check_db_connection()
