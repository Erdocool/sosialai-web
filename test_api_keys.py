#!/usr/bin/env python3
"""
API Key Test Script - SosyalAI
Bu script API key yönetimi endpoint'lerini test eder.
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:8000"

def test_api_key_endpoints():
    """API key endpoint'lerini test et"""
    
    print("🔑 SosyalAI API Key Test Script'i")
    print("=" * 50)
    
    # Test verisi
    test_api_keys = {
        "openai": "sk-test123456789",
        "klingai": "kling_test123456789",
        "twitter": "twitter_test_key",
        "twitter_secret": "twitter_test_secret",
        "instagram": "instagram_test_key",
        "youtube": "youtube_test_key",
        "tiktok": "tiktok_test_key",
        "linkedin": "linkedin_test_key",
        "facebook": "facebook_test_key"
    }
    
    try:
        # 1. API key'leri kaydet
        print("\n1️⃣ API Key'leri Kaydetme Testi")
        print("-" * 30)
        
        response = requests.post(
            f"{BASE_URL}/api/v1/settings/api-keys",
            json=test_api_keys,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Başarılı: {result['message']}")
            print(f"   Kaydedilen key'ler: {result['saved_keys']}")
        else:
            print(f"❌ Hata: {response.status_code} - {response.text}")
            
        # 2. OpenAI API key test
        print("\n2️⃣ OpenAI API Key Test")
        print("-" * 30)
        
        response = requests.post(
            f"{BASE_URL}/api/v1/test/openai",
            json={"api_key": test_api_keys["openai"]},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ OpenAI Test Başarılı: {result['message']}")
        else:
            print(f"❌ OpenAI Test Hatası: {response.status_code} - {response.text}")
            
        # 3. KlingAI API key test
        print("\n3️⃣ KlingAI API Key Test")
        print("-" * 30)
        
        response = requests.post(
            f"{BASE_URL}/api/v1/test/klingai",
            json={"api_key": test_api_keys["klingai"]},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ KlingAI Test Başarılı: {result['message']}")
        else:
            print(f"❌ KlingAI Test Hatası: {response.status_code} - {response.text}")
            
        # 4. Health check
        print("\n4️⃣ API Health Check")
        print("-" * 30)
        
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ API Sağlıklı: {result['status']}")
            print(f"   Veritabanı: {result['database']}")
            print(f"   Zamanlayıcı: {result['scheduler']}")
        else:
            print(f"❌ Health Check Hatası: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Backend bağlantısı kurulamadı!")
        print("   Backend'in çalıştığından emin olun: python -m uvicorn api.main:app --host 127.0.0.1 --port 8000")
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {e}")

def test_frontend_integration():
    """Frontend entegrasyonunu test et"""
    
    print("\n🌐 Frontend Entegrasyon Testi")
    print("=" * 50)
    
    try:
        # Frontend'e bağlan
        response = requests.get("http://localhost:5173")
        if response.status_code == 200:
            print("✅ Frontend erişilebilir")
        else:
            print(f"❌ Frontend hatası: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Frontend bağlantısı kurulamadı!")
        print("   Frontend'in çalıştığından emin olun: npm run dev")

if __name__ == "__main__":
    print("🚀 SosyalAI API Key Test Script'i başlatılıyor...")
    print(f"   Backend URL: {BASE_URL}")
    print(f"   Frontend URL: http://localhost:5173")
    print()
    
    # Backend testleri
    test_api_key_endpoints()
    
    # Frontend testleri
    test_frontend_integration()
    
    print("\n" + "=" * 50)
    print("✨ Test tamamlandı!")
    print("\n📝 Kullanım:")
    print("   1. Frontend'de Settings sayfasına gidin")
    print("   2. API key'lerinizi girin")
    print("   3. 'Test Et' butonları ile key'leri test edin")
    print("   4. 'API Key'leri Kaydet' ile kaydedin")
    print("\n🔗 Linkler:")
    print("   - Frontend: http://localhost:5173/settings")
    print("   - Backend API: http://localhost:8000/docs")
