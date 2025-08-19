#!/usr/bin/env python3
"""
SosyalAI Başlatma Script'i
"""
import os
import sys
import subprocess
import time
from pathlib import Path

def check_python_version():
    """Python versiyonunu kontrol et"""
    if sys.version_info < (3, 9):
        print("❌ Python 3.9 veya üzeri gerekli!")
        print(f"Mevcut versiyon: {sys.version}")
        return False
    print(f"✅ Python versiyonu uygun: {sys.version}")
    return True

def check_dependencies():
    """Gerekli bağımlılıkları kontrol et"""
    print("🔍 Bağımlılıklar kontrol ediliyor...")
    
    required_packages = [
        'fastapi', 'uvicorn', 'sqlalchemy', 'openai', 
        'requests', 'pandas', 'numpy', 'pillow'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} bulunamadı")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ Eksik paketler: {', '.join(missing_packages)}")
        print("Lütfen 'pip install -r requirements.txt' komutunu çalıştırın")
        return False
    
    return True

def install_dependencies():
    """Bağımlılıkları yükle"""
    print("\n📦 Bağımlılıklar yükleniyor...")
    
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True, capture_output=True, text=True)
        print("✅ Bağımlılıklar başarıyla yüklendi")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Bağımlılık yükleme hatası: {e}")
        return False

def create_env_file():
    """Environment dosyası oluştur"""
    env_file = Path(".env")
    env_example = Path("env.example")
    
    if not env_file.exists() and env_example.exists():
        print("\n📝 .env dosyası oluşturuluyor...")
        try:
            with open(env_example, 'r', encoding='utf-8') as f:
                content = f.read()
            
            with open(env_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ .env dosyası oluşturuldu")
            print("⚠️ Lütfen .env dosyasında API anahtarlarını güncelleyin")
            return True
        except Exception as e:
            print(f"❌ .env dosyası oluşturma hatası: {e}")
            return False
    
    return True

def start_backend():
    """Backend'i başlat"""
    print("\n🚀 Backend başlatılıyor...")
    
    try:
        # Backend'i arka planda başlat
        process = subprocess.Popen([
            sys.executable, "main.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Kısa bir süre bekle
        time.sleep(3)
        
        if process.poll() is None:
            print("✅ Backend başarıyla başlatıldı")
            print(f"🌐 API: http://127.0.0.1:8000")
            print(f"📚 Dokümantasyon: http://127.0.0.1:8000/docs")
            return process
        else:
            print("❌ Backend başlatılamadı")
            return None
            
    except Exception as e:
        print(f"❌ Backend başlatma hatası: {e}")
        return None

def start_frontend():
    """Frontend'i başlat"""
    print("\n🎨 Frontend başlatılıyor...")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Frontend dizini bulunamadı")
        return None
    
    try:
        # Node.js bağımlılıklarını kontrol et
        package_json = frontend_dir / "package.json"
        if not package_json.exists():
            print("❌ package.json bulunamadı")
            return None
        
        # npm install çalıştır
        print("📦 Frontend bağımlılıkları yükleniyor...")
        subprocess.run([
            "npm", "install"
        ], cwd=frontend_dir, check=True, capture_output=True)
        
        # Frontend'i başlat
        print("🚀 Frontend dev server başlatılıyor...")
        process = subprocess.Popen([
            "npm", "run", "dev"
        ], cwd=frontend_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Kısa bir süre bekle
        time.sleep(5)
        
        if process.poll() is None:
            print("✅ Frontend başarıyla başlatıldı")
            print(f"🌐 Frontend: http://localhost:5173")
            return process
        else:
            print("❌ Frontend başlatılamadı")
            return None
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Frontend başlatma hatası: {e}")
        return None
    except FileNotFoundError:
        print("❌ npm bulunamadı. Node.js yüklü olduğundan emin olun")
        return None

def main():
    """Ana fonksiyon"""
    print("🚀 SosyalAI Başlatılıyor...")
    print("=" * 50)
    
    # Python versiyonunu kontrol et
    if not check_python_version():
        sys.exit(1)
    
    # Bağımlılıkları kontrol et
    if not check_dependencies():
        print("\n📦 Bağımlılıklar yükleniyor...")
        if not install_dependencies():
            print("❌ Bağımlılık yükleme başarısız!")
            sys.exit(1)
    
    # Environment dosyasını oluştur
    create_env_file()
    
    # Backend'i başlat
    backend_process = start_backend()
    if not backend_process:
        print("❌ Backend başlatılamadı!")
        sys.exit(1)
    
    # Frontend'i başlat
    frontend_process = start_frontend()
    
    print("\n" + "=" * 50)
    print("🎉 SosyalAI başarıyla başlatıldı!")
    print("\n📱 Kullanım:")
    print("• Backend API: http://127.0.0.1:8000")
    print("• API Dokümantasyon: http://127.0.0.1:8000/docs")
    if frontend_process:
        print("• Frontend: http://localhost:5173")
    
    print("\n⏹️ Uygulamayı durdurmak için Ctrl+C tuşlayın")
    
    try:
        # Ana süreçleri bekle
        if frontend_process:
            frontend_process.wait()
        backend_process.wait()
    except KeyboardInterrupt:
        print("\n\n🛑 Uygulama durduruluyor...")
        
        # Süreçleri temizle
        if frontend_process:
            frontend_process.terminate()
        backend_process.terminate()
        
        print("✅ Uygulama durduruldu")

if __name__ == "__main__":
    main()
