import React from 'react';
import RainbowWavesBackground from './Ui/RainbowWavesBackground.jsx';
import { useNavigate } from 'react-router-dom';

export default function PagLogin() {
  const navigate = useNavigate();
  return (
    <div className="relative min-h-screen flex flex-col items-center justify-center text-white">
      <RainbowWavesBackground />
      <main className="relative z-10 text-center">
        <h1 className="text-5xl sm:text-7xl font-bold mb-12 text-white drop-shadow-lg">Bienvenido a tu gestor de música favorita</h1>
        <button className="
          px-10 py-5
          text-4xl sm:text-6xl
          font-bold
          rounded-lg
          bg-pink-500 hover:bg-pink-600
          text-white
          shadow-lg
          transition-colors duration-300
          focus-visible:outline focus-visible:outline-2 focus-visible:outline-pink-300
        "onClick={() => navigate("/home")} >
          Iniciar
        </button>
      </main>
    </div>
  );
}

