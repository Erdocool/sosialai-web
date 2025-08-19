"""
SosyalAI AI Servisleri - OpenAI, KlingAI Entegrasyonu
"""
import openai
import requests
import json
import logging
from typing import Dict, List, Optional, Any
from config.settings import settings

logger = logging.getLogger(__name__)

class AIService:
    """AI servisleri ana sınıfı"""
    
    def __init__(self):
        self.openai_client = None
        self.klingai_api_key = settings.KLINGAI_API_KEY
        
        # OpenAI client'ı başlat
        if settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY
            self.openai_client = openai
        else:
            logger.warning("OpenAI API anahtarı bulunamadı")
    
    async def generate_content_ideas(self, platform: str, category: str, language: str = "tr") -> List[Dict]:
        """İçerik fikirleri üret"""
        try:
            if not self.openai_client:
                return self._fallback_content_ideas(platform, category, language)
            
            prompt = self._build_content_idea_prompt(platform, category, language)
            
            response = await self.openai_client.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Sen sosyal medya içerik uzmanısın. Yaratıcı ve etkileşimli içerik fikirleri üretirsin."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.8
            )
            
            content = response.choices[0].message.content
            return self._parse_content_ideas(content)
            
        except Exception as e:
            logger.error(f"İçerik fikri üretme hatası: {e}")
            return self._fallback_content_ideas(platform, category, language)
    
    async def generate_caption(self, content_type: str, platform: str, language: str = "tr") -> str:
        """İçerik caption'ı üret"""
        try:
            if not self.openai_client:
                return self._fallback_caption(content_type, platform, language)
            
            prompt = self._build_caption_prompt(content_type, platform, language)
            
            response = await self.openai_client.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Sen sosyal medya caption uzmanısın. Etkileşimi artıran, viral olabilecek caption'lar yazarsın."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Caption üretme hatası: {e}")
            return self._fallback_caption(content_type, platform, language)
    
    async def generate_hashtags(self, content: str, platform: str, count: int = 20) -> List[str]:
        """İçeriğe uygun hashtag'ler üret"""
        try:
            if not self.openai_client:
                return self._fallback_hashtags(platform, count)
            
            prompt = f"""
            Aşağıdaki içerik için {platform} platformunda kullanılabilecek {count} adet popüler hashtag üret:
            
            İçerik: {content}
            
            Sadece hashtag'leri liste halinde döndür, başka açıklama ekleme.
            """
            
            response = await self.openai_client.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Sen hashtag uzmanısın. Popüler ve etkili hashtag'ler önerirsin."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.6
            )
            
            content = response.choices[0].message.content
            return self._parse_hashtags(content)
            
        except Exception as e:
            logger.error(f"Hashtag üretme hatası: {e}")
            return self._fallback_hashtags(platform, count)
    
    async def generate_image(self, prompt: str, style: str = "modern") -> Optional[str]:
        """DALL-E ile görsel üret"""
        try:
            if not self.openai_client:
                return None
            
            enhanced_prompt = f"{prompt}, {style} style, high quality, social media optimized"
            
            response = await self.openai_client.Image.acreate(
                prompt=enhanced_prompt,
                n=1,
                size="1024x1024",
                quality="hd"
            )
            
            image_url = response.data[0].url
            logger.info(f"Görsel başarıyla üretildi: {image_url}")
            return image_url
            
        except Exception as e:
            logger.error(f"Görsel üretme hatası: {e}")
            return None
    
    async def generate_video_prompt(self, content_type: str, platform: str) -> str:
        """Video üretimi için prompt oluştur"""
        try:
            if not self.openai_client:
                return self._fallback_video_prompt(content_type, platform)
            
            prompt = f"""
            {platform} platformu için {content_type} türünde video üretimi yapılacak.
            Video için detaylı, yaratıcı ve teknik açıdan net bir prompt oluştur.
            """
            
            response = await self.openai_client.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Sen video üretim uzmanısın. AI video araçları için detaylı prompt'lar yazarsın."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Video prompt üretme hatası: {e}")
            return self._fallback_video_prompt(content_type, platform)
    
    def _build_content_idea_prompt(self, platform: str, category: str, language: str) -> str:
        """İçerik fikri için prompt oluştur"""
        language_map = {"tr": "Türkçe", "en": "İngilizce"}
        lang_name = language_map.get(language, "Türkçe")
        
        return f"""
        {platform} platformu için {category} kategorisinde {lang_name} içerik fikirleri üret.
        
        Her fikir için:
        - Başlık
        - Kısa açıklama
        - İçerik türü (görsel, video, carousel, text)
        - Hedef kitle
        - Beklenen etkileşim
        
        Toplam 5 fikir üret.
        """
    
    def _build_caption_prompt(self, content_type: str, platform: str, language: str) -> str:
        """Caption için prompt oluştur"""
        language_map = {"tr": "Türkçe", "en": "İngilizce"}
        lang_name = language_map.get(language, "Türkçe")
        
        return f"""
        {platform} platformu için {content_type} türünde {lang_name} caption yaz.
        
        Caption özellikleri:
        - Etkileşimi artırıcı
        - Viral potansiyeli yüksek
        - Platform algoritmasına uygun
        - Emoji kullanımı dengeli
        - Call-to-action içeren
        
        Sadece caption metnini döndür.
        """
    
    def _parse_content_ideas(self, content: str) -> List[Dict]:
        """AI'dan gelen içerik fikirlerini parse et"""
        # Basit parsing - gerçek uygulamada daha gelişmiş olabilir
        ideas = []
        lines = content.split('\n')
        
        current_idea = {}
        for line in lines:
            line = line.strip()
            if line.startswith('-') or line.startswith('•'):
                if current_idea:
                    ideas.append(current_idea)
                current_idea = {'description': line[1:].strip()}
            elif ':' in line and current_idea:
                key, value = line.split(':', 1)
                current_idea[key.strip().lower()] = value.strip()
        
        if current_idea:
            ideas.append(current_idea)
        
        return ideas[:5]  # Maksimum 5 fikir
    
    def _parse_hashtags(self, content: str) -> List[str]:
        """AI'dan gelen hashtag'leri parse et"""
        hashtags = []
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('#'):
                hashtags.append(line)
            elif line and not line.startswith('-') and not line.startswith('•'):
                # Satırda hashtag varsa çıkar
                words = line.split()
                for word in words:
                    if word.startswith('#'):
                        hashtags.append(word)
        
        return hashtags[:20]  # Maksimum 20 hashtag
    
    def _fallback_content_ideas(self, platform: str, category: str, language: str) -> List[Dict]:
        """AI servisi çalışmadığında fallback içerik fikirleri"""
        fallback_ideas = {
            "instagram": [
                {"title": "Günlük Motivasyon", "description": "Güne pozitif başlangıç", "type": "image", "audience": "genel", "engagement": "yüksek"},
                {"title": "Behind the Scenes", "description": "Çalışma sürecini göster", "type": "video", "audience": "takipçiler", "engagement": "orta"},
                {"title": "Ürün Tanıtımı", "description": "Öne çıkan özellikler", "type": "carousel", "audience": "potansiyel müşteriler", "engagement": "orta"}
            ],
            "tiktok": [
                {"title": "Trend Challenge", "description": "Popüler challenge'a katıl", "type": "video", "audience": "genç kitle", "engagement": "çok yüksek"},
                {"title": "Hızlı İpucu", "description": "15 saniyede faydalı bilgi", "type": "video", "audience": "öğrenmeye açık", "engagement": "yüksek"}
            ]
        }
        
        return fallback_ideas.get(platform, fallback_ideas["instagram"])
    
    def _fallback_caption(self, content_type: str, platform: str, language: str) -> str:
        """AI servisi çalışmadığında fallback caption"""
        if language == "tr":
            return f"Harika bir {content_type} içeriği! 🎉 Beğenmeyi ve paylaşmayı unutmayın! 💪 #sosialai #otomasyon"
        else:
            return f"Amazing {content_type} content! 🎉 Don't forget to like and share! 💪 #sosialai #automation"
    
    def _fallback_hashtags(self, platform: str, count: int) -> List[str]:
        """AI servisi çalışmadığında fallback hashtag'ler"""
        common_hashtags = {
            "instagram": ["#instagram", "#instagood", "#photooftheday", "#love", "#fashion", "#beautiful", "#happy", "#cute", "#followme", "#picoftheday"],
            "tiktok": ["#tiktok", "#fyp", "#foryou", "#viral", "#trending", "#funny", "#dance", "#music", "#comedy", "#entertainment"],
            "twitter": ["#twitter", "#trending", "#news", "#tech", "#business", "#politics", "#sports", "#entertainment", "#lifestyle", "#health"]
        }
        
        platform_hashtags = common_hashtags.get(platform, common_hashtags["instagram"])
        return platform_hashtags[:count]
    
    def _fallback_video_prompt(self, content_type: str, platform: str) -> str:
        """AI servisi çalışmadığında fallback video prompt"""
        return f"Create a {content_type} video for {platform} platform. High quality, engaging content with smooth transitions and modern visual effects."

# Global AI service instance
ai_service = AIService()
