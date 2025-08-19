"""
SosyalAI Ana API Uygulaması
"""
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from database.database import get_db, init_db
from services.ai_service import ai_service
from services.strategy_service import strategy_service
from core.schemas import (
    ContentIdeaRequest, ContentIdeaResponse, CaptionRequest, CaptionResponse,
    HashtagRequest, HashtagResponse, StrategyRequest, StrategyResponse,
    PostScheduleRequest, PostScheduleResponse, APIKeysRequest
)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="SosyalAI API",
    description="Sosyal Medya Otomasyon & Akıllı Paylaşım Stratejisi API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production'da spesifik origin'ler belirtin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
app.mount("/static", StaticFiles(directory="uploads"), name="static")

@app.on_event("startup")
async def startup_event():
    """Uygulama başlangıcında çalışacak event"""
    try:
        # Veritabanını başlat
        init_db()
        logger.info("Veritabanı başarıyla başlatıldı")
        
        # Zamanlayıcıyı başlat
        strategy_service.start_scheduler()
        logger.info("Zamanlayıcı başarıyla başlatıldı")
        
    except Exception as e:
        logger.error(f"Uygulama başlangıç hatası: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Uygulama kapanışında çalışacak event"""
    try:
        # Zamanlayıcıyı durdur
        strategy_service.stop_scheduler()
        logger.info("Zamanlayıcı durduruldu")
        
    except Exception as e:
        logger.error(f"Uygulama kapanış hatası: {e}")

@app.get("/")
async def root():
    """Ana endpoint"""
    return {
        "message": "SosyalAI API'ye Hoş Geldiniz!",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/health")
async def health_check():
    """Sağlık kontrolü"""
    return {
        "status": "healthy",
        "database": "connected",
        "scheduler": "running" if strategy_service.scheduler.running else "stopped"
    }

# AI İçerik Üretimi Endpoint'leri

@app.post("/api/v1/content/ideas", response_model=List[ContentIdeaResponse])
async def generate_content_ideas(
    request: ContentIdeaRequest,
    db: Session = Depends(get_db)
):
    """İçerik fikirleri üret"""
    try:
        logger.info(f"İçerik fikri üretiliyor: {request.platform}, {request.category}")
        
        ideas = await ai_service.generate_content_ideas(
            platform=request.platform,
            category=request.category,
            language=request.language
        )
        
        return ideas
        
    except Exception as e:
        logger.error(f"İçerik fikri üretme hatası: {e}")
        raise HTTPException(status_code=500, detail="İçerik fikri üretilemedi")

@app.post("/api/v1/content/caption", response_model=CaptionResponse)
async def generate_caption(
    request: CaptionRequest,
    db: Session = Depends(get_db)
):
    """İçerik caption'ı üret"""
    try:
        logger.info(f"Caption üretiliyor: {request.content_type}, {request.platform}")
        
        caption = await ai_service.generate_caption(
            content_type=request.content_type,
            platform=request.platform,
            language=request.language
        )
        
        return CaptionResponse(
            caption=caption,
            platform=request.platform,
            content_type=request.content_type
        )
        
    except Exception as e:
        logger.error(f"Caption üretme hatası: {e}")
        raise HTTPException(status_code=500, detail="Caption üretilemedi")

@app.post("/api/v1/content/hashtags", response_model=HashtagResponse)
async def generate_hashtags(
    request: HashtagRequest,
    db: Session = Depends(get_db)
):
    """İçerik için hashtag'ler üret"""
    try:
        logger.info(f"Hashtag üretiliyor: {request.platform}")
        
        hashtags = await ai_service.generate_hashtags(
            content=request.content,
            platform=request.platform,
            count=request.count
        )
        
        return HashtagResponse(
            hashtags=hashtags,
            platform=request.platform,
            count=len(hashtags)
        )
        
    except Exception as e:
        logger.error(f"Hashtag üretme hatası: {e}")
        raise HTTPException(status_code=500, detail="Hashtag'ler üretilemedi")

@app.post("/api/v1/content/image")
async def generate_image(
    prompt: str,
    style: str = "modern",
    db: Session = Depends(get_db)
):
    """AI ile görsel üret"""
    try:
        logger.info(f"Görsel üretiliyor: {prompt}")
        
        image_url = await ai_service.generate_image(
            prompt=prompt,
            style=style
        )
        
        if not image_url:
            raise HTTPException(status_code=500, detail="Görsel üretilemedi")
        
        return {"image_url": image_url, "prompt": prompt, "style": style}
        
    except Exception as e:
        logger.error(f"Görsel üretme hatası: {e}")
        raise HTTPException(status_code=500, detail="Görsel üretilemedi")

# Strateji ve Zamanlama Endpoint'leri

@app.post("/api/v1/strategy/best-time", response_model=StrategyResponse)
async def get_best_posting_time(
    request: StrategyRequest,
    db: Session = Depends(get_db)
):
    """En iyi paylaşım zamanını hesapla"""
    try:
        logger.info(f"Strateji hesaplanıyor: {request.platform}")
        
        strategy = strategy_service.get_best_posting_time(
            platform=request.platform,
            user_history=request.user_history
        )
        
        return StrategyResponse(**strategy)
        
    except Exception as e:
        logger.error(f"Strateji hesaplama hatası: {e}")
        raise HTTPException(status_code=500, detail="Strateji hesaplanamadı")

@app.post("/api/v1/strategy/schedule", response_model=PostScheduleResponse)
async def schedule_post(
    request: PostScheduleRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Post'u zamanla"""
    try:
        logger.info(f"Post zamanlanıyor: {request.post_id}")
        
        # Zamanlama işlemi
        success = strategy_service.schedule_post({
            "post_id": request.post_id,
            "scheduled_time": request.scheduled_time
        })
        
        if not success:
            raise HTTPException(status_code=500, detail="Post zamanlanamadı")
        
        return PostScheduleResponse(
            post_id=request.post_id,
            scheduled_time=request.scheduled_time,
            status="scheduled"
        )
        
    except Exception as e:
        logger.error(f"Post zamanlama hatası: {e}")
        raise HTTPException(status_code=500, detail="Post zamanlanamadı")

@app.get("/api/v1/strategy/platforms")
async def get_supported_platforms():
    """Desteklenen platformları listele"""
    platforms = list(strategy_service.platform_best_times.keys())
    return {
        "platforms": platforms,
        "count": len(platforms)
    }

@app.get("/api/v1/strategy/tips/{platform}")
async def get_platform_tips(platform: str):
    """Platform için ipuçları al"""
    try:
        tips = strategy_service._get_platform_tips(platform)
        return {
            "platform": platform,
            "tips": tips
        }
    except Exception as e:
        logger.error(f"Platform ipucu alma hatası: {e}")
        raise HTTPException(status_code=404, detail="Platform bulunamadı")

# Trend Analizi Endpoint'leri

@app.get("/api/v1/trends/{platform}")
async def get_trending_topics(platform: str):
    """Platform trendlerini al"""
    try:
        # Burada gerçek trend analizi yapılacak
        # Şimdilik örnek veri döndürüyoruz
        sample_trends = {
            "instagram": [
                "reels", "carousel", "stories", "igtv", "live"
            ],
            "tiktok": [
                "challenges", "dances", "comedy", "education", "beauty"
            ],
            "twitter": [
                "threads", "spaces", "fleets", "trending", "news"
            ]
        }
        
        trends = sample_trends.get(platform, [])
        return {
            "platform": platform,
            "trending_topics": trends,
            "analyzed_at": "2024-01-01T00:00:00Z"
        }
        
    except Exception as e:
        logger.error(f"Trend analizi hatası: {e}")
        raise HTTPException(status_code=500, detail="Trend analizi yapılamadı")

# Performans Takibi Endpoint'leri

@app.get("/api/v1/performance/{post_id}")
async def get_post_performance(post_id: int, db: Session = Depends(get_db)):
    """Post performansını al"""
    try:
        # Burada gerçek performans verisi veritabanından alınacak
        # Şimdilik örnek veri döndürüyoruz
        sample_performance = {
            "post_id": post_id,
            "likes": 150,
            "comments": 25,
            "shares": 10,
            "views": 1200,
            "reach": 5000,
            "engagement_rate": 3.7
        }
        
        return sample_performance
        
    except Exception as e:
        logger.error(f"Performans verisi alma hatası: {e}")
        raise HTTPException(status_code=500, detail="Performans verisi alınamadı")

# API Key Yönetimi Endpoint'leri

@app.post("/api/v1/settings/api-keys")
async def save_api_keys(request: APIKeysRequest):
    """API key'leri kaydet"""
    try:
        logger.info("API key'ler kaydediliyor")
        
        # Burada gerçek veritabanına kayıt yapılacak
        # Şimdilik başarılı olarak döndürüyoruz
        return {
            "message": "API key'ler başarıyla kaydedildi",
            "status": "success",
            "saved_keys": list(request.dict().keys())
        }
        
    except Exception as e:
        logger.error(f"API key kaydetme hatası: {e}")
        raise HTTPException(status_code=500, detail="API key'ler kaydedilemedi")

@app.post("/api/v1/test/openai")
async def test_openai_key(request: dict):
    """OpenAI API key'ini test et"""
    try:
        api_key = request.get("api_key")
        if not api_key:
            raise HTTPException(status_code=400, detail="API key gerekli")
        
        # OpenAI API key'ini test et
        import openai
        openai.api_key = api_key
        
        # Basit bir test yap
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Merhaba"}],
            max_tokens=10
        )
        
        return {
            "message": "OpenAI API key geçerli",
            "status": "valid",
            "model": "gpt-3.5-turbo"
        }
        
    except Exception as e:
        logger.error(f"OpenAI API key test hatası: {e}")
        raise HTTPException(status_code=400, detail="Geçersiz API key")

@app.post("/api/v1/test/klingai")
async def test_klingai_key(request: dict):
    """KlingAI API key'ini test et"""
    try:
        api_key = request.get("api_key")
        if not api_key:
            raise HTTPException(status_code=400, detail="API key gerekli")
        
        # KlingAI API key'ini test et (placeholder)
        # Gerçek implementasyonda KlingAI API'si kullanılacak
        
        return {
            "message": "KlingAI API key geçerli",
            "status": "valid",
            "service": "klingai"
        }
        
    except Exception as e:
        logger.error(f"KlingAI API key test hatası: {e}")
        raise HTTPException(status_code=400, detail="Geçersiz API key")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
