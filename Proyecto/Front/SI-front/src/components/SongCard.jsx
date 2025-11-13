import React, { useState } from 'react';

function getRandomColor() {
  const h = Math.floor(Math.random() * 360);
  return `hsl(${h},80%,70%)`;
}

export default function SongCard({ song }) {
  const [cardColor, setCardColor] = useState("#18181b");
  return (
    <div
      className="w-48 rounded-lg bg-slate-900 hover:scale-105 transition transform shadow-lg p-4 relative"
      style={{ border: `3px solid ${cardColor}` }}
      onMouseEnter={() => setCardColor(getRandomColor())}
    >
      <img
        src={song.cover}
        alt={song.title}
        className="w-full h-48 object-cover rounded-md mb-2"
      />
      <div className="font-bold text-white text-lg truncate">{song.title}</div>
      <div className="text-sm text-gray-300">{song.artist}</div>
      <div className="absolute top-2 right-2">
        {/* Puedes reemplazar por menú real si lo necesitas */}
        <select className="rounded px-2 py-1 text-xs bg-slate-800 text-white">
          <option>Acción</option>
          <option>Add Miércoles</option>
          <option>Add Jueves</option>
          <option>Add Viernes</option>
          <option>Add Sábado</option>
          <option>BlackList</option>
        </select>
      </div>
    </div>
  );
}
