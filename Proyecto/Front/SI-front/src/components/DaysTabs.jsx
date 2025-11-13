import React from 'react';

const daysGenres = [
  { day: 'Lunes', genre: 'Reggaetón' },
  { day: 'Martes', genre: 'Pop' },
  { day: 'Miércoles', genre: 'Rock' },
  { day: 'Jueves', genre: 'Electrónica' },
  { day: 'Viernes', genre: 'Salsa' },
  { day: 'Sábado', genre: 'Indie' },
  { day: 'Domingo', genre: 'Vallenato' }
];

export default function DaysTabs({ activeDay, setActiveDay }) {
  return (
    <div className="mt-6 overflow-x-auto no-scrollbar">
      <div className="inline-flex gap-2 px-2">
        {daysGenres.map((item, idx) => (
          <button
            key={item.day}
            className={`inline-block px-4 py-2 rounded-full border font-medium whitespace-nowrap ${activeDay === idx ? "bg-blue-600 text-white border-blue-700" : "bg-gray-100 text-slate-900 border-transparent hover:bg-blue-100"}`}
            onClick={() => setActiveDay(idx)}
          >
            {item.day} <span className="text-sm text-gray-500">({item.genre})</span>
          </button>
        ))}
      </div>
    </div>
  )
}
