import React, { useState } from 'react';
import Header from '../components/Header.jsx';
import DaysTabs from '../components/DaysTabs.jsx';
import SummaryKPIs from '../components/SummaryKPIs.jsx';
import TopSongsTable from '../components/TopSongsTable.jsx';
import SurveyForm from '../components/SurveyForm.jsx';

const mockData = {
  genreDistribution: {
    mainGenre: 'Reggaetón',
    distribution: {
      Reggaetón: 40,
      Pop: 25,
      Rock: 20,
      Electrónica: 15,
    },
  },
  animationLevel: 4,
  ambience: 'Energético',
  salesPeak: '8–10pm',
  topSongs: [
    { id: 1, title: 'DÁKITI', artist: 'Bad Bunny', rating: 5 },
    { id: 2, title: 'Levitating', artist: 'Dua Lipa', rating: 4 },
    { id: 3, title: 'Bohemian Rhapsody', artist: 'Queen', rating: 5 },
  ],
};

export default function Metricas() {
  const [activeDay, setActiveDay] = useState(0);

  const handleSurveySubmit = (formData) => {
    // Aquí puedes guardar el reporte final o enviar al backend
    console.log('Reporte recogido:', formData);
    alert('Reporte enviado con éxito');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-black px-0">
      <Header activeIdx={2} />
      <div className="max-w-5xl mx-auto px-4 py-7">
        <DaysTabs activeDay={activeDay} setActiveDay={setActiveDay} />
        <SummaryKPIs data={mockData} />
        <TopSongsTable songs={mockData.topSongs} />
        <SurveyForm onSubmit={handleSurveySubmit} />
      </div>
    </div>
  );
}
