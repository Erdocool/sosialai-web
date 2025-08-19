"""
SosyalAI API Şemaları - Pydantic Modelleri
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

# Base Models

class BaseResponse(BaseModel):
    """Temel response modeli"""
    success: bool = True
    message: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)

# Content Generation Models

class ContentIdeaRequest(BaseModel):
    """İçerik fikri üretme request'i"""
    platform: str = Field(..., description="Sosyal medya platformu")
    category: str = Field(..., description="İçerik kategorisi")
    language: str = Field(default="tr", description="İçerik dili (tr/en)")
    
    class Config:
        schema_extra = {
            "example": {
                "platform": "instagram",
                "category": "motivasyon",
                "language": "tr"
            }
        }

class ContentIdeaResponse(BaseModel):
    """İçerik fikri response'u"""
    title: Optional[str] = Field(None, description="İçerik başlığı")
    description: str = Field(..., description="İçerik açıklaması")
    content_type: Optional[str] = Field(None, description="İçerik türü")
    audience: Optional[str] = Field(None, description="Hedef kitle")
    engagement: Optional[str] = Field(None, description="Beklenen etkileşim")
    
    class Config:
        schema_extra = {
            "example": {
                "title": "Günlük Motivasyon",
                "description": "Güne pozitif başlangıç yapmak için motivasyonel içerik",
                "content_type": "image",
                "audience": "genel",
                "engagement": "yüksek"
            }
        }

class CaptionRequest(BaseModel):
    """Caption üretme request'i"""
    content_type: str = Field(..., description="İçerik türü")
    platform: str = Field(..., description="Platform")
    language: str = Field(default="tr", description="Dil")
    additional_context: Optional[str] = Field(None, description="Ek bağlam")
    
    class Config:
        schema_extra = {
            "example": {
                "content_type": "image",
                "platform": "instagram",
                "language": "tr",
                "additional_context": "Motivasyonel içerik"
            }
        }

class CaptionResponse(BaseModel):
    """Caption response'u"""
    caption: str = Field(..., description="Üretilen caption")
    platform: str = Field(..., description="Platform")
    content_type: str = Field(..., description="İçerik türü")
    
    class Config:
        schema_extra = {
            "example": {
                "caption": "Harika bir gün! 🌅 Pozitif enerji ile başlayalım! 💪 #motivasyon #günlük",
                "platform": "instagram",
                "content_type": "image"
            }
        }

class HashtagRequest(BaseModel):
    """Hashtag üretme request'i"""
    content: str = Field(..., description="İçerik metni")
    platform: str = Field(..., description="Platform")
    count: int = Field(default=20, ge=5, le=50, description="Hashtag sayısı")
    
    class Config:
        schema_extra = {
            "example": {
                "content": "Motivasyonel içerik ile güne başlıyorum",
                "platform": "instagram",
                "count": 20
            }
        }

class HashtagResponse(BaseModel):
    """Hashtag response'u"""
    hashtags: List[str] = Field(..., description="Üretilen hashtag'ler")
    platform: str = Field(..., description="Platform")
    count: int = Field(..., description="Hashtag sayısı")
    
    class Config:
        schema_extra = {
            "example": {
                "hashtags": ["#motivasyon", "#günlük", "#pozitif", "#enerji"],
                "platform": "instagram",
                "count": 4
            }
        }

# Strategy Models

class StrategyRequest(BaseModel):
    """Strateji hesaplama request'i"""
    platform: str = Field(..., description="Platform")
    user_history: Optional[Dict[str, Any]] = Field(None, description="Kullanıcı geçmişi")
    
    class Config:
        schema_extra = {
            "example": {
                "platform": "instagram",
                "user_history": {
                    "performance_data": [
                        {"posted_hour": 18, "engagement_rate": 4.2},
                        {"posted_hour": 21, "engagement_rate": 3.8}
                    ]
                }
            }
        }

class StrategyResponse(BaseModel):
    """Strateji response'u"""
    platform: str = Field(..., description="Platform")
    strategy: Dict[str, Any] = Field(..., description="Strateji detayları")
    recommended_times: List[Dict[str, Any]] = Field(..., description="Önerilen zamanlar")
    confidence_score: float = Field(..., description="Güvenilirlik skoru")
    next_best_time: Optional[Dict[str, Any]] = Field(None, description="Bir sonraki en iyi zaman")
    tips: List[str] = Field(..., description="Platform ipuçları")
    
    class Config:
        schema_extra = {
            "example": {
                "platform": "instagram",
                "strategy": {
                    "best_days": [1, 2, 3, 4, 5],
                    "best_hours": [9, 12, 18, 21]
                },
                "recommended_times": [
                    {
                        "datetime": "2024-01-15T18:00:00",
                        "day_name": "Monday",
                        "time": "18:00",
                        "priority": "high"
                    }
                ],
                "confidence_score": 0.85,
                "next_best_time": {
                    "datetime": "2024-01-15T18:00:00",
                    "day_name": "Monday",
                    "time": "18:00"
                },
                "tips": [
                    "Reels paylaşımları için 18:00-21:00 arası en iyi",
                    "Carousel postlar için 12:00-14:00 arası tercih edin"
                ]
            }
        }

class PostScheduleRequest(BaseModel):
    """Post zamanlama request'i"""
    post_id: int = Field(..., description="Post ID")
    scheduled_time: datetime = Field(..., description="Zamanlanan zaman")
    
    class Config:
        schema_extra = {
            "example": {
                "post_id": 123,
                "scheduled_time": "2024-01-15T18:00:00"
            }
        }

class PostScheduleResponse(BaseModel):
    """Post zamanlama response'u"""
    post_id: int = Field(..., description="Post ID")
    scheduled_time: datetime = Field(..., description="Zamanlanan zaman")
    status: str = Field(..., description="Zamanlama durumu")
    
    class Config:
        schema_extra = {
            "example": {
                "post_id": 123,
                "scheduled_time": "2024-01-15T18:00:00",
                "status": "scheduled"
            }
        }

# Content Models

class ContentPostRequest(BaseModel):
    """İçerik post request'i"""
    platform: str = Field(..., description="Platform")
    content_type: str = Field(..., description="İçerik türü")
    title: Optional[str] = Field(None, description="Başlık")
    caption: str = Field(..., description="Caption")
    hashtags: List[str] = Field(default=[], description="Hashtag'ler")
    media_urls: Optional[List[str]] = Field(None, description="Medya dosya URL'leri")
    ai_generated: bool = Field(default=False, description="AI ile üretildi mi?")
    
    class Config:
        schema_extra = {
            "example": {
                "platform": "instagram",
                "content_type": "image",
                "title": "Günlük Motivasyon",
                "caption": "Harika bir gün! 🌅",
                "hashtags": ["#motivasyon", "#günlük"],
                "media_urls": ["https://example.com/image.jpg"],
                "ai_generated": True
            }
        }

class ContentPostResponse(BaseModel):
    """İçerik post response'u"""
    id: int = Field(..., description="Post ID")
    platform: str = Field(..., description="Platform")
    status: str = Field(..., description="Durum")
    created_at: datetime = Field(..., description="Oluşturulma zamanı")
    
    class Config:
        schema_extra = {
            "example": {
                "id": 123,
                "platform": "instagram",
                "status": "draft",
                "created_at": "2024-01-15T10:00:00"
            }
        }

# Performance Models

class PerformanceMetrics(BaseModel):
    """Performans metrikleri"""
    post_id: int = Field(..., description="Post ID")
    likes: int = Field(default=0, description="Beğeni sayısı")
    comments: int = Field(default=0, description="Yorum sayısı")
    shares: int = Field(default=0, description="Paylaşım sayısı")
    views: int = Field(default=0, description="Görüntülenme sayısı")
    reach: int = Field(default=0, description="Erişim sayısı")
    engagement_rate: float = Field(default=0.0, description="Etkileşim oranı")
    collected_at: datetime = Field(..., description="Veri toplama zamanı")
    
    class Config:
        schema_extra = {
            "example": {
                "post_id": 123,
                "likes": 150,
                "comments": 25,
                "shares": 10,
                "views": 1200,
                "reach": 5000,
                "engagement_rate": 3.7,
                "collected_at": "2024-01-15T18:00:00"
            }
        }

# Error Models

class ErrorResponse(BaseModel):
    """Hata response'u"""
    success: bool = False
    error: str = Field(..., description="Hata mesajı")
    error_code: Optional[str] = Field(None, description="Hata kodu")
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        schema_extra = {
            "example": {
                "success": False,
                "error": "İçerik üretilemedi",
                "error_code": "CONTENT_GENERATION_FAILED",
                "timestamp": "2024-01-15T10:00:00"
            }
        }

# Success Models

class SuccessResponse(BaseModel):
    """Başarı response'u"""
    success: bool = True
    message: str = Field(..., description="Başarı mesajı")
    data: Optional[Dict[str, Any]] = Field(None, description="Ek veri")
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "message": "İşlem başarıyla tamamlandı",
                "data": {"post_id": 123},
                "timestamp": "2024-01-15T10:00:00"
            }
        }

# API Key Management Models

class APIKeysRequest(BaseModel):
    """API key'leri kaydetme request'i"""
    openai: Optional[str] = Field(None, description="OpenAI API Key")
    klingai: Optional[str] = Field(None, description="KlingAI API Key")
    twitter: Optional[str] = Field(None, description="Twitter/X API Key")
    twitter_secret: Optional[str] = Field(None, description="Twitter/X API Secret")
    instagram: Optional[str] = Field(None, description="Instagram API Key")
    youtube: Optional[str] = Field(None, description="YouTube API Key")
    tiktok: Optional[str] = Field(None, description="TikTok API Key")
    linkedin: Optional[str] = Field(None, description="LinkedIn API Key")
    facebook: Optional[str] = Field(None, description="Facebook API Key")
    
    class Config:
        schema_extra = {
            "example": {
                "openai": "sk-...",
                "klingai": "kling_...",
                "twitter": "twitter_api_key",
                "twitter_secret": "twitter_api_secret",
                "instagram": "instagram_api_key",
                "youtube": "youtube_api_key",
                "tiktok": "tiktok_api_key",
                "linkedin": "linkedin_api_key",
                "facebook": "facebook_api_key"
            }
        }
