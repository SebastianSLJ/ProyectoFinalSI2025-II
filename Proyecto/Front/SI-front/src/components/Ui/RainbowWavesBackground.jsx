import React from 'react';

export default function RainbowWavesBackground() {
  const waveCount = 200;

  return (
    <div className="absolute inset-0 -z-10 flex items-center justify-center bg-slate-900 overflow-hidden">
      <div className="flex gap-[2px]">
        {Array.from({ length: waveCount }).map((_, i) => (
          <div
            key={i}
            className="w-[2px] h-full animate-wave bg-gradient-to-b from-pink-500 via-yellow-500 to-blue-500 hover:bg-random transition-all duration-300"
            style={{
              animationDelay: `${i * 0.05}s`,
              height: `${Math.random() * 100 + 100}px`,
            }}
          />
        ))}
      </div>
    </div>
  );
}