import React from 'react';

export default function SummaryKPIs({ data }) {
  // data: { genreDistribution, animationLevel, ambience, salesPeak }
  // Ejemplos simples con barras y textos
  return (
    <div className="flex flex-wrap justify-between gap-6 mb-8">
      {/* Género predominante */}
      <div className="bg-gray-800 rounded-xl p-6 flex-1 min-w-[250px]">
        <h3 className="font-semibold mb-2 text-white">Género predominante</h3>
        <div className="text-lg font-bold text-pink-500">{data.genreDistribution.mainGenre}</div>
        {/* Distribución ronda */}
        <div className="mt-4 flex gap-2">
          {Object.entries(data.genreDistribution.distribution).map(([genre, percent]) => (
            <div key={genre} className="flex flex-col items-center">
              <div className="w-8 h-8 rounded-full bg-pink-400" />
              <span className="text-sm text-white">{genre.slice(0,3)}</span>
              <span className="text-xs text-gray-400">{percent}%</span>
            </div>
          ))}
        </div>
      </div>

      {/* Nivel de animación */}
      <div className="bg-gray-800 rounded-xl p-6 flex-1 min-w-[250px] text-white">
        <h3 className="font-semibold mb-2">Animación clientela</h3>
        <div className="text-4xl font-bold">{data.animationLevel} / 5</div>
      </div>

      {/* Ambiente */}
      <div className="bg-gray-800 rounded-xl p-6 flex-1 min-w-[250px]">
        <h3 className="font-semibold mb-2 text-white">Ambiente generado</h3>
        <p className="text-white">{data.ambience}</p>
      </div>

      {/* Pico ventas */}
      <div className="bg-gray-800 rounded-xl p-6 flex-1 min-w-[250px] text-white">
        <h3 className="font-semibold mb-2">Pico de ventas</h3>
        <p>{data.salesPeak}</p>
      </div>
    </div>
  );
}
