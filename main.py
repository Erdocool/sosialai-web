"""
SosyalAI Ana Uygulama
"""
import asyncio
import logging
import sys
import os
from pathlib import Path

# Proje kök dizinini Python path'ine ekle
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from backend.api.main import app
from backend.database.database import init_db, check_db_connection
from backend.services.strategy_service import strategy_service
from config.settings import settings

# Logging konfigürasyonu
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sosialai.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

async def startup():
    """Uygulama başlangıç işlemleri"""
    try:
        logger.info("SosyalAI başlatılıyor...")
        
        # Veritabanı bağlantısını kontrol et
        if not check_db_connection():
            logger.error("Veritabanı bağlantısı başarısız!")
            return False
        
        # Veritabanını başlat
        init_db()
        logger.info("Veritabanı başarıyla başlatıldı")
        
        # Zamanlayıcıyı başlat
        strategy_service.start_scheduler()
        logger.info("Zamanlayıcı başarıyla başlatıldı")
        
        logger.info("SosyalAI başarıyla başlatıldı!")
        return True
        
    except Exception as e:
        logger.error(f"Uygulama başlangıç hatası: {e}")
        return False

async def shutdown():
    """Uygulama kapanış işlemleri"""
    try:
        logger.info("SosyalAI kapatılıyor...")
        
        # Zamanlayıcıyı durdur
        strategy_service.stop_scheduler()
        logger.info("Zamanlayıcı durduruldu")
        
        logger.info("SosyalAI başarıyla kapatıldı!")
        
    except Exception as e:
        logger.error(f"Uygulama kapanış hatası: {e}")

def main():
    """Ana fonksiyon"""
    try:
        # Event loop oluştur
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Başlangıç işlemlerini çalıştır
        if not loop.run_until_complete(startup()):
            logger.error("Uygulama başlatılamadı!")
            sys.exit(1)
        
        # FastAPI uygulamasını çalıştır
        import uvicorn
        uvicorn.run(
            app,
            host=settings.API_HOST,
            port=settings.API_PORT,
            log_level="info",
            access_log=True
        )
        
    except KeyboardInterrupt:
        logger.info("Kullanıcı tarafından durduruldu")
    except Exception as e:
        logger.error(f"Ana uygulama hatası: {e}")
    finally:
        # Kapanış işlemlerini çalıştır
        try:
            loop.run_until_complete(shutdown())
        except Exception as e:
            logger.error(f"Kapanış hatası: {e}")
        
        loop.close()

if __name__ == "__main__":
    main()
