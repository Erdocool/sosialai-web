"""
SosyalAI Akıllı Paylaşım Stratejisi Servisi
"""
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from config.settings import settings

logger = logging.getLogger(__name__)

class StrategyService:
    """Akıllı paylaşım stratejisi servisi"""
    
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.timezone = pytz.timezone(settings.DEFAULT_TIMEZONE)
        
        # Platform bazlı en iyi paylaşım zamanları (genel veriler)
        self.platform_best_times = {
            "instagram": {
                "best_days": [1, 2, 3, 4, 5],  # Pazartesi-Cuma
                "best_hours": [9, 12, 18, 21],  # 09:00, 12:00, 18:00, 21:00
                "peak_hours": [18, 21],  # En iyi saatler
                "avoid_hours": [2, 3, 4, 5],  # Kaçınılması gereken saatler
                "content_types": ["image", "carousel", "video", "reel"],
                "optimal_frequency": "daily"
            },
            "tiktok": {
                "best_days": [2, 3, 4, 5, 6],  # Salı-Cumartesi
                "best_hours": [10, 14, 19, 22],  # 10:00, 14:00, 19:00, 22:00
                "peak_hours": [19, 22],  # En iyi saatler
                "avoid_hours": [1, 2, 3, 4],  # Kaçınılması gereken saatler
                "content_types": ["video", "duet", "challenge"],
                "optimal_frequency": "2-3_daily"
            },
            "twitter": {
                "best_days": [1, 2, 3, 4, 5],  # Pazartesi-Cuma
                "best_hours": [8, 12, 17, 20],  # 08:00, 12:00, 17:00, 20:00
                "peak_hours": [12, 17],  # En iyi saatler
                "avoid_hours": [2, 3, 4, 5],  # Kaçınılması gereken saatler
                "content_types": ["text", "image", "video", "thread"],
                "optimal_frequency": "3-5_daily"
            },
            "youtube": {
                "best_days": [2, 3, 4, 5, 6],  # Salı-Cumartesi
                "best_hours": [14, 18, 20],  # 14:00, 18:00, 20:00
                "peak_hours": [18, 20],  # En iyi saatler
                "avoid_hours": [1, 2, 3, 4],  # Kaçınılması gereken saatler
                "content_types": ["video", "shorts", "live"],
                "optimal_frequency": "weekly"
            }
        }
    
    def get_best_posting_time(self, platform: str, user_history: Optional[Dict] = None) -> Dict:
        """Platform için en iyi paylaşım zamanını hesapla"""
        try:
            platform_strategy = self.platform_best_times.get(platform, {})
            
            if not platform_strategy:
                return self._get_default_strategy()
            
            # Kullanıcı geçmişi varsa kişiselleştir
            if user_history:
                personalized_strategy = self._personalize_strategy(platform_strategy, user_history)
            else:
                personalized_strategy = platform_strategy
            
            # En iyi zamanları hesapla
            best_times = self._calculate_optimal_times(personalized_strategy)
            
            return {
                "platform": platform,
                "strategy": personalized_strategy,
                "recommended_times": best_times,
                "confidence_score": self._calculate_confidence_score(user_history),
                "next_best_time": self._get_next_best_time(best_times),
                "tips": self._get_platform_tips(platform)
            }
            
        except Exception as e:
            logger.error(f"En iyi paylaşım zamanı hesaplama hatası: {e}")
            return self._get_default_strategy()
    
    def _personalize_strategy(self, base_strategy: Dict, user_history: Dict) -> Dict:
        """Kullanıcı geçmişine göre stratejiyi kişiselleştir"""
        personalized = base_strategy.copy()
        
        # Geçmiş performans verilerini analiz et
        if "performance_data" in user_history:
            performance = user_history["performance_data"]
            
            # En iyi performans gösteren saatleri bul
            best_performing_hours = self._analyze_performance_hours(performance)
            if best_performing_hours:
                personalized["best_hours"] = best_performing_hours
            
            # En iyi performans gösteren günleri bul
            best_performing_days = self._analyze_performance_days(performance)
            if best_performing_days:
                personalized["best_days"] = best_performing_days
        
        # Kullanıcı tercihlerini uygula
        if "user_preferences" in user_history:
            prefs = user_history["user_preferences"]
            if "preferred_hours" in prefs:
                personalized["best_hours"] = prefs["preferred_hours"]
            if "preferred_days" in prefs:
                personalized["best_days"] = prefs["preferred_days"]
        
        return personalized
    
    def _analyze_performance_hours(self, performance_data: List[Dict]) -> List[int]:
        """Performans verilerinden en iyi saatleri analiz et"""
        hour_performance = {}
        
        for post in performance_data:
            if "posted_hour" in post and "engagement_rate" in post:
                hour = post["posted_hour"]
                engagement = post["engagement_rate"]
                
                if hour not in hour_performance:
                    hour_performance[hour] = []
                hour_performance[hour].append(engagement)
        
        # Ortalama engagement rate'e göre sırala
        avg_performance = {}
        for hour, rates in hour_performance.items():
            avg_performance[hour] = sum(rates) / len(rates)
        
        # En iyi 4 saati döndür
        best_hours = sorted(avg_performance.items(), key=lambda x: x[1], reverse=True)[:4]
        return [hour for hour, _ in best_hours]
    
    def _analyze_performance_days(self, performance_data: List[Dict]) -> List[int]:
        """Performans verilerinden en iyi günleri analiz et"""
        day_performance = {}
        
        for post in performance_data:
            if "posted_day" in post and "engagement_rate" in post:
                day = post["posted_day"]
                engagement = post["engagement_rate"]
                
                if day not in day_performance:
                    day_performance[day] = []
                day_performance[day].append(engagement)
        
        # Ortalama engagement rate'e göre sırala
        avg_performance = {}
        for day, rates in day_performance.items():
            avg_performance[day] = sum(rates) / len(rates)
        
        # En iyi 5 günü döndür
        best_days = sorted(avg_performance.items(), key=lambda x: x[1], reverse=True)[:5]
        return [day for day, _ in best_days]
    
    def _calculate_optimal_times(self, strategy: Dict) -> List[Dict]:
        """Stratejiye göre optimal zamanları hesapla"""
        optimal_times = []
        
        # Bu hafta için öneriler
        current_date = datetime.now(self.timezone)
        
        for day in strategy.get("best_days", []):
            for hour in strategy.get("best_hours", []):
                # Gelecek hafta için zaman hesapla
                days_ahead = (day - current_date.weekday()) % 7
                if days_ahead == 0:
                    days_ahead = 7  # Gelecek hafta
                
                target_date = current_date + timedelta(days=days_ahead)
                target_datetime = target_date.replace(
                    hour=hour, minute=0, second=0, microsecond=0
                )
                
                # Geçmiş zamanları önerme
                if target_datetime > current_date:
                    optimal_times.append({
                        "datetime": target_datetime,
                        "day_name": target_datetime.strftime("%A"),
                        "time": target_datetime.strftime("%H:%M"),
                        "priority": "high" if hour in strategy.get("peak_hours", []) else "medium"
                    })
        
        # Zaman sırasına göre sırala
        optimal_times.sort(key=lambda x: x["datetime"])
        
        return optimal_times[:10]  # En iyi 10 zamanı döndür
    
    def _calculate_confidence_score(self, user_history: Optional[Dict]) -> float:
        """Öneri güvenilirlik skorunu hesapla"""
        if not user_history:
            return 0.7  # Varsayılan skor
        
        # Kullanıcı verisi miktarına göre skor hesapla
        data_points = 0
        if "performance_data" in user_history:
            data_points += len(user_history["performance_data"])
        
        if "user_preferences" in user_history:
            data_points += 1
        
        # Skor hesaplama (0.5 - 1.0 arası)
        if data_points == 0:
            return 0.5
        elif data_points < 10:
            return 0.6
        elif data_points < 30:
            return 0.75
        elif data_points < 50:
            return 0.85
        else:
            return 0.95
    
    def _get_next_best_time(self, optimal_times: List[Dict]) -> Optional[Dict]:
        """Bir sonraki en iyi paylaşım zamanını bul"""
        if not optimal_times:
            return None
        
        current_time = datetime.now(self.timezone)
        
        for time_slot in optimal_times:
            if time_slot["datetime"] > current_time:
                return time_slot
        
        return None
    
    def _get_platform_tips(self, platform: str) -> List[str]:
        """Platform için özel ipuçları"""
        tips = {
            "instagram": [
                "Reels paylaşımları için 18:00-21:00 arası en iyi",
                "Carousel postlar için 12:00-14:00 arası tercih edin",
                "Stories için gün boyunca düzenli paylaşım yapın",
                "Hashtag kullanımında 20-30 arası optimal"
            ],
            "tiktok": [
                "Trend challenge'lara katılmak için 19:00-22:00 arası",
                "Eğitici içerikler için 14:00-16:00 arası",
                "Müzik içerikleri için 20:00-23:00 arası",
                "Günlük 2-3 video paylaşımı optimal"
            ],
            "twitter": [
                "Breaking news için 08:00-09:00 arası",
                "Thread paylaşımları için 12:00-13:00 arası",
                "Engagement için 17:00-18:00 arası",
                "Günlük 3-5 tweet optimal"
            ],
            "youtube": [
                "Uzun videolar için 18:00-20:00 arası",
                "Shorts için 14:00-16:00 arası",
                "Live yayınlar için 20:00-22:00 arası",
                "Haftalık 1-2 video optimal"
            ]
        }
        
        return tips.get(platform, ["Düzenli paylaşım yapın", "Takipçi etkileşimini takip edin"])
    
    def _get_default_strategy(self) -> Dict:
        """Varsayılan strateji"""
        return {
            "platform": "unknown",
            "strategy": {
                "best_days": [1, 2, 3, 4, 5],
                "best_hours": [9, 12, 18, 21],
                "content_types": ["image", "video", "text"]
            },
            "recommended_times": [],
            "confidence_score": 0.5,
            "next_best_time": None,
            "tips": ["Düzenli paylaşım yapın", "Takipçi etkileşimini takip edin"]
        }
    
    def schedule_post(self, post_data: Dict) -> bool:
        """Post'u zamanla"""
        try:
            scheduled_time = post_data["scheduled_time"]
            post_id = post_data["post_id"]
            
            # Zamanlayıcıya ekle
            job = self.scheduler.add_job(
                func=self._execute_scheduled_post,
                trigger=CronTrigger(
                    year=scheduled_time.year,
                    month=scheduled_time.month,
                    day=scheduled_time.day,
                    hour=scheduled_time.hour,
                    minute=scheduled_time.minute,
                    timezone=self.timezone
                ),
                args=[post_id],
                id=f"post_{post_id}",
                replace_existing=True
            )
            
            logger.info(f"Post {post_id} başarıyla zamanlandı: {scheduled_time}")
            return True
            
        except Exception as e:
            logger.error(f"Post zamanlama hatası: {e}")
            return False
    
    async def _execute_scheduled_post(self, post_id: int):
        """Zamanlanmış post'u çalıştır"""
        try:
            logger.info(f"Zamanlanmış post çalıştırılıyor: {post_id}")
            
            # Burada gerçek post işlemi yapılacak
            # Platform API'leri çağrılacak
            
            logger.info(f"Post {post_id} başarıyla paylaşıldı")
            
        except Exception as e:
            logger.error(f"Zamanlanmış post çalıştırma hatası: {e}")
    
    def start_scheduler(self):
        """Zamanlayıcıyı başlat"""
        if not self.scheduler.running:
            self.scheduler.start()
            logger.info("Zamanlayıcı başlatıldı")
    
    def stop_scheduler(self):
        """Zamanlayıcıyı durdur"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Zamanlayıcı durduruldu")

# Global strategy service instance
strategy_service = StrategyService()
