import React, { useState } from 'react';

const ambienceOptions = ['Tranquilo', 'Energético', 'Romántico', 'Festivo', 'Ruidoso', 'Otro'];
const yesNoOptions = ['Sí', 'No', 'No se observó'];

export default function SurveyForm({ onSubmit }) {
  const [formData, setFormData] = useState({
    dominantGenre: '',
    ambience: '',
    animationLevel: 3,
    groupInteraction: '',
    salesComments: '',
    salesPeakTime: '',
    productMusicPeak: '',
    positiveMusicSales: '',
  });

  const handleChange = (field, value) => setFormData(prev => ({ ...prev, [field]: value }));

  return (
    <form
      className="bg-gray-900 p-6 rounded-xl max-w-2xl mx-auto my-6 space-y-6 text-white"
      onSubmit={e => {
        e.preventDefault();
        onSubmit(formData);
      }}
    >
      <h2 className="text-2xl font-bold mb-4">Encuesta al finalizar jornada</h2>

      {/* Dominant Genre */}
      <div>
        <label className="block mb-1">¿Qué género musical predominó durante la jornada?</label>
        <input
          type="text"
          value={formData.dominantGenre}
          onChange={e => handleChange('dominantGenre', e.target.value)}
          className="w-full p-2 rounded bg-gray-700 text-white"
          placeholder="Escriba el género"
          required
        />
      </div>

      {/* Ambiente */}
      <div>
        <label className="block mb-1">¿Cómo describirías el ambiente generado por la música?</label>
        <select
          value={formData.ambience}
          onChange={e => handleChange('ambience', e.target.value)}
          className="w-full p-2 rounded bg-gray-700 text-white"
          required
        >
          <option value="">Seleccione una opción</option>
          {ambienceOptions.map(opt => (
            <option key={opt} value={opt}>{opt}</option>
          ))}
        </select>
      </div>

      {/* Nivel de animación */}
      <div>
        <label className="block mb-1">¿Qué tan animada estuvo la clientela durante la jornada?</label>
        <input
          type="range"
          min="1"
          max="5"
          value={formData.animationLevel}
          onChange={e => handleChange('animationLevel', e.target.value)}
          className="w-full"
        />
        <div className="flex justify-between text-sm">
          {[1, 2, 3, 4, 5].map(n => (
            <span key={n}>{n}</span>
          ))}
        </div>
      </div>

      {/* Interacción grupal */}
      <div>
        <label className="block mb-1">¿Hubo momentos de baile o interacción grupal?</label>
        <select
          value={formData.groupInteraction}
          onChange={e => handleChange('groupInteraction', e.target.value)}
          className="w-full p-2 rounded bg-gray-700 text-white"
          required
        >
          <option value="">Seleccione una opción</option>
          {yesNoOptions.map(opt => (
            <option key={opt} value={opt}>{opt}</option>
          ))}
        </select>
      </div>

      {/* Comentarios */}
      <div>
        <label className="block mb-1">¿Hubo comentarios positivos o negativos sobre la música por parte de los clientes?</label>
        <select
          value={formData.salesComments}
          onChange={e => handleChange('salesComments', e.target.value)}
          className="w-full p-2 rounded bg-gray-700 text-white"
          required
        >
          <option value="">Seleccione una opción</option>
          {yesNoOptions.slice(0, 2).map(opt => (
            <option key={opt} value={opt}>{opt}</option>
          ))}
        </select>
        {formData.salesComments === 'Sí' && (
          <textarea
            className="w-full p-2 mt-2 rounded bg-gray-700 text-white"
            placeholder="¿Cuáles?"
            onChange={e => handleChange('salesCommentsDetails', e.target.value)}
          />
        )}
      </div>

      {/* Pico de ventas */}
      <div>
        <label className="block mb-1">¿En qué horario se registró el mayor volumen de ventas?</label>
        <input
          type="text"
          className="w-full p-2 rounded bg-gray-700 text-white"
          value={formData.salesPeakTime}
          onChange={e => handleChange('salesPeakTime', e.target.value)}
          placeholder="Ej: 6–8pm, 8–10pm..."
          required
        />
      </div>

      {/* Pico canción */}
      <div>
        <label className="block mb-1">¿Hubo alguna canción o género que coincidiera con un pico de ventas?</label>
        <select
          value={formData.productMusicPeak}
          onChange={e => handleChange('productMusicPeak', e.target.value)}
          className="w-full p-2 rounded bg-gray-700 text-white"
          required
        >
          <option value="">Seleccione una opción</option>
          {yesNoOptions.slice(0, 2).map(opt => (
            <option key={opt} value={opt}>{opt}</option>
          ))}
        </select>
        {formData.productMusicPeak === 'Sí' && (
          <input
            type="text"
            className="w-full p-2 mt-2 rounded bg-gray-700 text-white"
            onChange={e => handleChange('productMusicPeakDetails', e.target.value)}
            placeholder="¿Cuál canción o género?"
          />
        )}
      </div>

      {/* Influencia en ventas */}
      <div>
        <label className="block mb-1">¿Consideras que la música influyó positivamente en las ventas?</label>
        <select
          value={formData.positiveMusicSales}
          onChange={e => handleChange('positiveMusicSales', e.target.value)}
          className="w-full p-2 rounded bg-gray-700 text-white"
          required
        >
          <option value="">Seleccione una opción</option>
          {[...yesNoOptions, 'No estoy seguro'].map(opt => (
            <option key={opt} value={opt}>{opt}</option>
          ))}
        </select>
      </div>

      <button
        type="submit"
        className="mt-6 px-6 py-3 rounded bg-pink-600 hover:bg-pink-700 text-white font-bold transition"
      >
        Enviar Reporte
      </button>
    </form>
  );
}
