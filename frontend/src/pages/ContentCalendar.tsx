import React from 'react'

const ContentCalendar: React.FC = () => {
  return (
    <div className="container mx-auto p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          İçerik Takvimi
        </h1>
        <p className="text-gray-600">
          Paylaşım planlaması ve zamanlama
        </p>
      </div>

      <div className="bg-white rounded-lg p-6 shadow-sm border">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Takvim Görünümü</h2>
        <p className="text-gray-600">İçerik takvimi yakında eklenecek...</p>
      </div>
    </div>
  )
}

export default ContentCalendar
