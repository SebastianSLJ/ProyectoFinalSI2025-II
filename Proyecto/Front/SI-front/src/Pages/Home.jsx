import React from 'react';
import Header from '../components/Header.jsx';
import SongListSection from '../components/SongListSection.jsx';
import perrobailando from '../assets/perrobailando.gif';

// Simula datos traídos del backend/Spotify API (reemplaza por fetch real luego)
const SONGS_TOP = [
  {
    id: 1,
    title: "DIOMEDEZ",
    artist: "Blessd, GeezyDee",
    cover: "https://i.scdn.co/image/ab67616d0000b273ad21e2bf4973ac098fbc7aa7",
  },
  {
    id: 2,
    title: "Hips Don't Lie - Spotify Anniversary",
    artist: "Shakira, Ed Sheeran, Beéle",
    cover: "https://i.scdn.co/image/ab67616d0000b2733569a1e2677f9b97b254f943",
  },
  // agrega más como quieras...
];

const SONGS_OTHER = [
  {
    id: 6,
    title: "BORONDO",
    artist: "Beéle",
    cover: "https://i.scdn.co/image/ab67616d0000b273a8d350090d6fefddb5a29392",
  },
  {
    id: 7,
    title: "DeBí TiRAR MÁS FoToS",
    artist: "Bad Bunny",
    cover: "https://i.scdn.co/image/ab67616d0000b273f8a2f9ee8de8222c9611e1d6",
  },
  // ...más
];

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-black">

      <img
        src={perrobailando}
        alt="Decorativo"
        className="absolute bottom-4 right-4 w-24 h-24 z-50"
      />

      <Header />
      <div className="flex">
        <main className="flex-1 p-8">
          <h1 className="text-3xl font-bold mb-6 text-white">
            Canciones Recomendadas
          </h1>
          <SongListSection title="Top" songs={SONGS_TOP} />
          <SongListSection title="Más populares" songs={SONGS_OTHER} />
        </main>
      </div>
    </div>
  );
}
