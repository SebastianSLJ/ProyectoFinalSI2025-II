import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const menuItems = [
  { label: 'Home', route: '/home' },
  { label: 'Listas de reproducción', route: '/listas' },
  { label: 'Métricas', route: '/metricas' }
];

export default function Header({ activeIdx = 0 }) {
  const [selected, setSelected] = useState(activeIdx);
  const navigate = useNavigate();

  return (
    <header className="flex items-center justify-between px-8 py-4 bg-slate-900 text-white">
      <nav className="flex gap-3">
        {menuItems.map((item, idx) => (
          <button
            key={item.label}
            className={`
              px-5 py-2 rounded-full font-semibold transition
              ${selected === idx
                ? "bg-green-500 shadow-md text-black"
                : "bg-slate-800 hover:bg-green-400 hover:text-black hover:shadow-md"}
            `}
            onClick={() => {
              setSelected(idx);
              navigate(item.route);
            }}
          >
            {item.label}
          </button>
        ))}
      </nav>
      {/* Buscador animado */}
      <div className="relative max-w-12 focus-within:max-w-[290px] transition-[max-width] ease-in-out duration-300">
        <input
          className="
            block w-full border-none outline-none rounded-full p-[12px] px-4
            text-base bg-slate-800 text-white placeholder:text-transparent
            focus:placeholder:text-gray-400 focus:bg-slate-700 focus:text-white
            transition
          "
          placeholder="Buscar canción, artista..."
        />
        <span className="absolute top-1/2 right-6 -translate-y-1/2 text-lg pointer-events-none">
          <svg width="22" height="22" fill="none" stroke="white" strokeWidth="2" viewBox="0 0 24 24">
            <circle cx="11" cy="11" r="7"/>
            <line x1="16" y1="16" x2="20" y2="20"/>
          </svg>
        </span>
      </div>  


    </header>
  );
}
