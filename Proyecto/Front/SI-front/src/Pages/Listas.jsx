import React, { useState } from 'react';
import Header from '../components/Header.jsx';
import DaysTabs from '../components/DaysTabs.jsx';
import PlaylistTable from '../components/PlaylistTable.jsx';

export default function Listas() {
  const [activeDay, setActiveDay] = useState(0);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-black px-0">
      <Header activeIdx={1} />
      <div className="max-w-4xl mx-auto px-4 py-7">
        <DaysTabs activeDay={activeDay} setActiveDay={setActiveDay} />
        <PlaylistTable activeDay={activeDay} />
      </div>
    </div>
  );
}
