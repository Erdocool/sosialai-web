# SosyalAI - Sosyal Medya Otomasyon & Akıllı Paylaşım Stratejisi

## 🚀 Proje Hakkında

SosyalAI, kullanıcıların TikTok, Instagram, X (Twitter), YouTube gibi sosyal medya platformlarında otomatik içerik üretme, planlama ve paylaşma işlemlerini tek bir masaüstü uygulama üzerinden yapabilmesini sağlayan kapsamlı bir otomasyon aracıdır.

## ✨ Temel Özellikler

- 🤖 **AI Destekli İçerik Üretimi**: OpenAI ve KlingAI entegrasyonu ile görsel, video ve metin üretimi
- 📊 **Trend Analizi**: Platform trendlerini analiz ederek içerik fikirleri üretme
- 🕒 **Akıllı Zamanlama**: En uygun paylaşım saat ve günlerini otomatik öneri
- 📱 **Çoklu Platform Desteği**: Instagram, TikTok, X, YouTube entegrasyonu
- 🏷️ **Hashtag Optimizasyonu**: İçeriğe ve platforma uygun hashtag önerileri
- 📈 **Performans Takibi**: Detaylı analitik ve raporlama
- 🎯 **Otomatik Paylaşım**: Zamanlanmış ve otomatik içerik yayınlama

## 🛠️ Teknoloji Stack

- **Backend**: Python 3.9+
- **Frontend**: Electron + React
- **Veritabanı**: SQLite
- **AI Servisleri**: OpenAI API, KlingAI
- **Otomasyon**: Selenium/Playwright
- **Zamanlama**: APScheduler

## 📁 Proje Yapısı

```
sosialai/
├── backend/                 # Python backend
│   ├── api/                # API endpoints
│   ├── core/               # Ana iş mantığı
│   ├── services/           # AI, platform entegrasyonları
│   ├── database/           # Veritabanı modelleri
│   └── utils/              # Yardımcı fonksiyonlar
├── frontend/               # Electron frontend
│   ├── src/                # React uygulaması
│   ├── public/             # Statik dosyalar
│   └── electron/           # Electron ana süreç
├── config/                  # Konfigürasyon dosyaları
├── requirements.txt         # Python bağımlılıkları
└── package.json            # Node.js bağımlılıkları
```

## 🚀 Kurulum

### Backend Kurulumu
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend Kurulumu
```bash
cd frontend
npm install
npm run dev
```

## 📋 Kullanım Senaryosu

1. **Platform Seçimi**: Hangi sosyal medya platformlarında içerik üretilecek?
2. **Trend Analizi**: Sistem trendleri analiz eder ve içerik fikirleri üretir
3. **AI İçerik Üretimi**: Görsel, video ve metin otomatik oluşturulur
4. **Strateji Planlama**: En iyi paylaşım zamanı otomatik önerilir
5. **Paylaşım**: İçerik preview edilir ve planlanan zamanda paylaşılır
6. **Raporlama**: Performans metrikleri takip edilir

## 🔧 Konfigürasyon

`.env` dosyasında gerekli API anahtarlarını tanımlayın:
```
OPENAI_API_KEY=your_openai_api_key
KLINGAI_API_KEY=your_klingai_api_key
```

## 📝 Lisans

MIT License

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📞 İletişim

Proje hakkında sorularınız için issue açabilir veya pull request gönderebilirsiniz.
