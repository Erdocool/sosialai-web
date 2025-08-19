#!/usr/bin/env python3
"""
SosyalAI Test Script
"""
import sys
import os
from pathlib import Path

# Proje kök dizinini Python path'ine ekle
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Gerekli modüllerin import edilebilir olup olmadığını test et"""
    print("🔍 Modül import testleri başlatılıyor...")
    
    try:
        from config.settings import settings
        print("✅ Config settings başarıyla import edildi")
    except ImportError as e:
        print(f"❌ Config settings import hatası: {e}")
        return False
    
    try:
        from backend.database.database import init_db, check_db_connection
        print("✅ Database modülü başarıyla import edildi")
    except ImportError as e:
        print(f"❌ Database modülü import hatası: {e}")
        return False
    
    try:
        from backend.services.ai_service import ai_service
        print("✅ AI service başarıyla import edildi")
    except ImportError as e:
        print(f"❌ AI service import hatası: {e}")
        return False
    
    try:
        from backend.services.strategy_service import strategy_service
        print("✅ Strategy service başarıyla import edildi")
    except ImportError as e:
        print(f"❌ Strategy service import hatası: {e}")
        return False
    
    return True

def test_database():
    """Veritabanı bağlantısını test et"""
    print("\n🗄️ Veritabanı testleri başlatılıyor...")
    
    try:
        from backend.database.database import check_db_connection
        if check_db_connection():
            print("✅ Veritabanı bağlantısı başarılı")
            return True
        else:
            print("❌ Veritabanı bağlantısı başarısız")
            return False
    except Exception as e:
        print(f"❌ Veritabanı test hatası: {e}")
        return False

def test_ai_service():
    """AI servisini test et"""
    print("\n🤖 AI servis testleri başlatılıyor...")
    
    try:
        from backend.services.ai_service import ai_service
        
        # Fallback fonksiyonları test et
        fallback_ideas = ai_service._fallback_content_ideas("instagram", "motivasyon", "tr")
        if fallback_ideas:
            print("✅ Fallback içerik fikirleri çalışıyor")
        else:
            print("❌ Fallback içerik fikirleri çalışmıyor")
        
        fallback_caption = ai_service._fallback_caption("image", "instagram", "tr")
        if fallback_caption:
            print("✅ Fallback caption çalışıyor")
        else:
            print("❌ Fallback caption çalışmıyor")
        
        fallback_hashtags = ai_service._fallback_hashtags("instagram", 10)
        if fallback_hashtags:
            print("✅ Fallback hashtag'ler çalışıyor")
        else:
            print("❌ Fallback hashtag'ler çalışmıyor")
        
        return True
        
    except Exception as e:
        print(f"❌ AI servis test hatası: {e}")
        return False

def test_strategy_service():
    """Strateji servisini test et"""
    print("\n📊 Strateji servis testleri başlatılıyor...")
    
    try:
        from backend.services.strategy_service import strategy_service
        
        # Platform stratejilerini test et
        platforms = ["instagram", "tiktok", "twitter", "youtube"]
        
        for platform in platforms:
            strategy = strategy_service.get_best_posting_time(platform)
            if strategy and "platform" in strategy:
                print(f"✅ {platform} stratejisi çalışıyor")
            else:
                print(f"❌ {platform} stratejisi çalışmıyor")
        
        # Platform ipuçlarını test et
        for platform in platforms:
            tips = strategy_service._get_platform_tips(platform)
            if tips:
                print(f"✅ {platform} ipuçları çalışıyor")
            else:
                print(f"❌ {platform} ipuçları çalışmıyor")
        
        return True
        
    except Exception as e:
        print(f"❌ Strateji servis test hatası: {e}")
        return False

def test_config():
    """Konfigürasyon ayarlarını test et"""
    print("\n⚙️ Konfigürasyon testleri başlatılıyor...")
    
    try:
        from config.settings import settings
        
        # Temel ayarları kontrol et
        if hasattr(settings, 'APP_NAME') and settings.APP_NAME == "SosyalAI":
            print("✅ APP_NAME ayarı doğru")
        else:
            print("❌ APP_NAME ayarı hatalı")
        
        if hasattr(settings, 'API_PORT') and settings.API_PORT == 8000:
            print("✅ API_PORT ayarı doğru")
        else:
            print("❌ API_PORT ayarı hatalı")
        
        if hasattr(settings, 'DEFAULT_TIMEZONE') and settings.DEFAULT_TIMEZONE == "Europe/Istanbul":
            print("✅ DEFAULT_TIMEZONE ayarı doğru")
        else:
            print("❌ DEFAULT_TIMEZONE ayarı hatalı")
        
        return True
        
    except Exception as e:
        print(f"❌ Konfigürasyon test hatası: {e}")
        return False

def main():
    """Ana test fonksiyonu"""
    print("🚀 SosyalAI Test Script Başlatılıyor...")
    print("=" * 50)
    
    tests = [
        ("Modül Import", test_imports),
        ("Veritabanı", test_database),
        ("AI Servis", test_ai_service),
        ("Strateji Servis", test_strategy_service),
        ("Konfigürasyon", test_config)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"⚠️ {test_name} testi başarısız")
        except Exception as e:
            print(f"❌ {test_name} testi hata verdi: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Sonuçları: {passed}/{total} başarılı")
    
    if passed == total:
        print("🎉 Tüm testler başarılı! Uygulama çalışmaya hazır.")
        return True
    else:
        print("⚠️ Bazı testler başarısız. Lütfen hataları kontrol edin.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
