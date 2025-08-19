"""
SosyalAI Veritabanı Modelleri
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class User(Base):
    """Kullanıcı modeli"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # İlişkiler
    social_accounts = relationship("SocialAccount", back_populates="user")
    content_posts = relationship("ContentPost", back_populates="user")
    scheduled_posts = relationship("ScheduledPost", back_populates="user")

class SocialAccount(Base):
    """Sosyal medya hesap modeli"""
    __tablename__ = "social_accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    platform = Column(String(50), nullable=False)  # instagram, tiktok, twitter, youtube
    username = Column(String(100), nullable=False)
    access_token = Column(Text)
    refresh_token = Column(Text)
    expires_at = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # İlişkiler
    user = relationship("User", back_populates="social_accounts")
    posts = relationship("ContentPost", back_populates="social_account")

class ContentPost(Base):
    """İçerik post modeli"""
    __tablename__ = "content_posts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    social_account_id = Column(Integer, ForeignKey("social_accounts.id"), nullable=False)
    platform = Column(String(50), nullable=False)
    content_type = Column(String(50))  # image, video, text, carousel
    title = Column(String(200))
    caption = Column(Text)
    hashtags = Column(JSON)  # List of hashtags
    media_urls = Column(JSON)  # List of media file paths
    ai_generated = Column(Boolean, default=False)
    ai_prompt = Column(Text)
    status = Column(String(50), default="draft")  # draft, scheduled, published, failed
    published_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # İlişkiler
    user = relationship("User", back_populates="content_posts")
    social_account = relationship("SocialAccount", back_populates="posts")
    scheduled_posts = relationship("ScheduledPost", back_populates="content_post")
    performance_metrics = relationship("PerformanceMetric", back_populates="content_post")

class ScheduledPost(Base):
    """Zamanlanmış post modeli"""
    __tablename__ = "scheduled_posts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content_post_id = Column(Integer, ForeignKey("content_posts.id"), nullable=False)
    scheduled_time = Column(DateTime(timezone=True), nullable=False)
    timezone = Column(String(50), default="Europe/Istanbul")
    status = Column(String(50), default="pending")  # pending, processing, completed, failed
    error_message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # İlişkiler
    user = relationship("User", back_populates="scheduled_posts")
    content_post = relationship("ContentPost", back_populates="scheduled_posts")

class PerformanceMetric(Base):
    """Performans metrik modeli"""
    __tablename__ = "performance_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    content_post_id = Column(Integer, ForeignKey("content_posts.id"), nullable=False)
    platform_post_id = Column(String(100))  # Platform'dan dönen post ID
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    views = Column(Integer, default=0)
    reach = Column(Integer, default=0)
    engagement_rate = Column(Float, default=0.0)
    collected_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # İlişkiler
    content_post = relationship("ContentPost", back_populates="performance_metrics")

class TrendAnalysis(Base):
    """Trend analiz modeli"""
    __tablename__ = "trend_analysis"
    
    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String(50), nullable=False)
    category = Column(String(100))
    trending_topics = Column(JSON)
    hashtag_trends = Column(JSON)
    content_ideas = Column(JSON)
    best_posting_times = Column(JSON)
    analyzed_at = Column(DateTime(timezone=True), server_default=func.now())

class AIContentGeneration(Base):
    """AI içerik üretim modeli"""
    __tablename__ = "ai_content_generation"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content_type = Column(String(50), nullable=False)  # image, video, text
    prompt = Column(Text, nullable=False)
    generated_content = Column(JSON)  # AI'dan dönen içerik
    model_used = Column(String(100))  # gpt-4, dall-e-3, klingai
    tokens_used = Column(Integer)
    cost = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # İlişkiler
    user = relationship("User")

class PostingStrategy(Base):
    """Paylaşım stratejisi modeli"""
    __tablename__ = "posting_strategies"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    platform = Column(String(50), nullable=False)
    strategy_name = Column(String(100), nullable=False)
    best_days = Column(JSON)  # [1, 2, 3, 4, 5, 6, 7] (Monday=1)
    best_hours = Column(JSON)  # [9, 12, 18, 21]
    content_types = Column(JSON)  # ["image", "video", "text"]
    hashtag_strategy = Column(JSON)
    frequency = Column(String(50))  # daily, weekly, custom
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # İlişkiler
    user = relationship("User")
