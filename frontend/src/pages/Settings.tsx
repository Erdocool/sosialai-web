import React, { useState, useEffect } from 'react'
import { toast } from 'react-hot-toast'

interface APIKeys {
  openai: string
  klingai: string
  twitter: string
  twitter_secret: string
  instagram: string
  youtube: string
  tiktok: string
  linkedin: string
  facebook: string
}

const Settings: React.FC = () => {
  const [apiKeys, setApiKeys] = useState<APIKeys>({
    openai: '',
    klingai: '',
    twitter: '',
    twitter_secret: '',
    instagram: '',
    youtube: '',
    tiktok: '',
    linkedin: '',
    facebook: ''
  })

  const [isLoading, setIsLoading] = useState(false)
  const [showKeys, setShowKeys] = useState(false)

  // API key'leri localStorage'dan yükle
  useEffect(() => {
    const savedKeys = localStorage.getItem('sosialai_api_keys')
    if (savedKeys) {
      try {
        const parsed = JSON.parse(savedKeys)
        setApiKeys(parsed)
      } catch (error) {
        console.error('API key\'leri yüklenirken hata:', error)
      }
    }
  }, [])

  // API key'leri kaydet
  const saveAPIKeys = async () => {
    setIsLoading(true)
    
    try {
      // Backend'e API key'leri gönder
      const response = await fetch('http://localhost:8000/api/v1/settings/api-keys', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(apiKeys),
      })

      if (response.ok) {
        // LocalStorage'a kaydet
        localStorage.setItem('sosialai_api_keys', JSON.stringify(apiKeys))
        toast.success('API key\'ler başarıyla kaydedildi!')
      } else {
        toast.error('API key\'ler kaydedilirken hata oluştu')
      }
    } catch (error) {
      // Backend bağlantısı yoksa sadece localStorage'a kaydet
      localStorage.setItem('sosialai_api_keys', JSON.stringify(apiKeys))
      toast.success('API key\'ler yerel olarak kaydedildi!')
    } finally {
      setIsLoading(false)
    }
  }

  // API key'leri test et
  const testAPIKey = async (service: string, key: string) => {
    if (!key.trim()) {
      toast.error(`${service} API key'i boş olamaz`)
      return
    }

    setIsLoading(true)
    
    try {
      let testEndpoint = ''
      let testData = {}

      switch (service) {
        case 'openai':
          testEndpoint = 'http://localhost:8000/api/v1/test/openai'
          testData = { api_key: key }
          break
        case 'klingai':
          testEndpoint = 'http://localhost:8000/api/v1/test/klingai'
          testData = { api_key: key }
          break
        default:
          toast(`${service} test endpoint'i henüz eklenmedi`)
          setIsLoading(false)
          return
      }

      const response = await fetch(testEndpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(testData),
      })

      if (response.ok) {
        toast.success(`${service} API key'i geçerli!`)
      } else {
        toast.error(`${service} API key'i geçersiz`)
      }
    } catch (error) {
      toast.error(`${service} test edilirken hata oluştu`)
    } finally {
      setIsLoading(false)
    }
  }

  // Tüm API key'leri temizle
  const clearAllKeys = () => {
    if (window.confirm('Tüm API key\'ler silinecek. Emin misiniz?')) {
      setApiKeys({
        openai: '',
        klingai: '',
        twitter: '',
        twitter_secret: '',
        instagram: '',
        youtube: '',
        tiktok: '',
        linkedin: '',
        facebook: ''
      })
      localStorage.removeItem('sosialai_api_keys')
      toast.success('Tüm API key\'ler temizlendi')
    }
  }

  const handleInputChange = (key: keyof APIKeys, value: string) => {
    setApiKeys(prev => ({
      ...prev,
      [key]: value
    }))
  }

  return (
    <div className="container mx-auto p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          API Key Ayarları
        </h1>
        <p className="text-gray-600">
          Sosyal medya platformları ve AI servisleri için API key'lerinizi yapılandırın
        </p>
      </div>

      {/* API Key Giriş Paneli */}
      <div className="bg-white rounded-lg shadow-sm border mb-6">
        <div className="p-6 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold text-gray-900">API Key Yönetimi</h2>
            <div className="flex items-center space-x-3">
              <button
                onClick={() => setShowKeys(!showKeys)}
                className="text-sm text-blue-600 hover:text-blue-800"
              >
                {showKeys ? 'Gizle' : 'Göster'}
              </button>
              <button
                onClick={clearAllKeys}
                className="text-sm text-red-600 hover:text-red-800"
              >
                Tümünü Temizle
              </button>
            </div>
          </div>
        </div>

        <div className="p-6">
          {/* AI Servisleri */}
          <div className="mb-8">
            <h3 className="text-lg font-medium text-gray-900 mb-4 flex items-center">
              <span className="w-2 h-2 bg-purple-500 rounded-full mr-3"></span>
              AI Servisleri
            </h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* OpenAI */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  OpenAI API Key
                  <span className="text-red-500 ml-1">*</span>
                </label>
                <div className="flex space-x-2">
                  <input
                    type={showKeys ? 'text' : 'password'}
                    value={apiKeys.openai}
                    onChange={(e) => handleInputChange('openai', e.target.value)}
                    placeholder="sk-..."
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                  <button
                    onClick={() => testAPIKey('openai', apiKeys.openai)}
                    disabled={isLoading || !apiKeys.openai.trim()}
                    className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Test Et
                  </button>
                </div>
                <p className="text-xs text-gray-500 mt-1">
                  ChatGPT, DALL-E ve diğer OpenAI servisleri için gerekli
                </p>
              </div>

              {/* KlingAI */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  KlingAI API Key
                </label>
                <div className="flex space-x-2">
                  <input
                    type={showKeys ? 'text' : 'password'}
                    value={apiKeys.klingai}
                    onChange={(e) => handleInputChange('klingai', e.target.value)}
                    placeholder="kling_..."
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                  <button
                    onClick={() => testAPIKey('klingai', apiKeys.klingai)}
                    disabled={isLoading || !apiKeys.klingai.trim()}
                    className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Test Et
                  </button>
                </div>
                <p className="text-xs text-gray-500 mt-1">
                  Video ve görsel içerik üretimi için
                </p>
              </div>
            </div>
          </div>

          {/* Sosyal Medya Platformları */}
          <div className="mb-8">
            <h3 className="text-lg font-medium text-gray-900 mb-4 flex items-center">
              <span className="w-2 h-2 bg-blue-500 rounded-full mr-3"></span>
              Sosyal Medya Platformları
            </h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Twitter/X */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Twitter/X API Key
                </label>
                <input
                  type={showKeys ? 'text' : 'password'}
                  value={apiKeys.twitter}
                  onChange={(e) => handleInputChange('twitter', e.target.value)}
                  placeholder="Twitter API Key"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                <p className="text-xs text-gray-500 mt-1">
                  Twitter Developer Portal'dan alınır
                </p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Twitter API Secret
                </label>
                <input
                  type={showKeys ? 'text' : 'password'}
                  value={apiKeys.twitter_secret}
                  onChange={(e) => handleInputChange('twitter_secret', e.target.value)}
                  placeholder="Twitter API Secret"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              {/* Instagram */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Instagram API Key
                </label>
                <input
                  type={showKeys ? 'text' : 'password'}
                  value={apiKeys.instagram}
                  onChange={(e) => handleInputChange('instagram', e.target.value)}
                  placeholder="Instagram API Key"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                <p className="text-xs text-gray-500 mt-1">
                  Facebook Developer Portal'dan alınır
                </p>
              </div>

              {/* YouTube */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  YouTube API Key
                </label>
                <input
                  type={showKeys ? 'text' : 'password'}
                  value={apiKeys.youtube}
                  onChange={(e) => handleInputChange('youtube', e.target.value)}
                  placeholder="YouTube API Key"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                <p className="text-xs text-gray-500 mt-1">
                  Google Cloud Console'dan alınır
                </p>
              </div>

              {/* TikTok */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  TikTok API Key
                </label>
                <input
                  type={showKeys ? 'text' : 'password'}
                  value={apiKeys.tiktok}
                  onChange={(e) => handleInputChange('tiktok', e.target.value)}
                  placeholder="TikTok API Key"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                <p className="text-xs text-gray-500 mt-1">
                  TikTok Developer Portal'dan alınır
                </p>
              </div>

              {/* LinkedIn */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  LinkedIn API Key
                </label>
                <input
                  type={showKeys ? 'text' : 'password'}
                  value={apiKeys.linkedin}
                  onChange={(e) => handleInputChange('linkedin', e.target.value)}
                  placeholder="LinkedIn API Key"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                <p className="text-xs text-gray-500 mt-1">
                  LinkedIn Developer Portal'dan alınır
                </p>
              </div>

              {/* Facebook */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Facebook API Key
                </label>
                <input
                  type={showKeys ? 'text' : 'password'}
                  value={apiKeys.facebook}
                  onChange={(e) => handleInputChange('facebook', e.target.value)}
                  placeholder="Facebook API Key"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                <p className="text-xs text-gray-500 mt-1">
                  Facebook Developer Portal'dan alınır
                </p>
              </div>
            </div>
          </div>

          {/* Kaydet Butonu */}
          <div className="flex justify-end space-x-3">
            <button
              onClick={saveAPIKeys}
              disabled={isLoading}
              className="px-6 py-3 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
            >
              {isLoading ? 'Kaydediliyor...' : 'API Key\'leri Kaydet'}
            </button>
          </div>
        </div>
      </div>

      {/* Yardım ve Bilgi */}
      <div className="bg-blue-50 rounded-lg p-6 border border-blue-200">
        <h3 className="text-lg font-medium text-blue-900 mb-3">💡 API Key Nasıl Alınır?</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-blue-800">
          <div>
            <h4 className="font-medium mb-2">OpenAI</h4>
            <p>1. <a href="https://platform.openai.com/api-keys" target="_blank" rel="noopener noreferrer" className="underline">OpenAI Platform</a>'a gidin</p>
            <p>2. API Keys sekmesinden yeni key oluşturun</p>
          </div>
          <div>
            <h4 className="font-medium mb-2">KlingAI</h4>
            <p>1. <a href="https://klingai.com" target="_blank" rel="noopener noreferrer" className="underline">KlingAI</a>'ya gidin</p>
            <p>2. API bölümünden key alın</p>
          </div>
          <div>
            <h4 className="font-medium mb-2">Twitter/X</h4>
            <p>1. <a href="https://developer.twitter.com" target="_blank" rel="noopener noreferrer" className="underline">Twitter Developer</a>'a gidin</p>
            <p>2. App oluşturup API key alın</p>
          </div>
          <div>
            <h4 className="font-medium mb-2">Instagram</h4>
            <p>1. <a href="https://developers.facebook.com" target="_blank" rel="noopener noreferrer" className="underline">Facebook Developer</a>'a gidin</p>
            <p>2. Instagram Basic Display App oluşturun</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Settings
