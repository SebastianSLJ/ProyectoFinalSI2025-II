import React, { useState } from 'react';
import RatingStars from './RatingStars.jsx';
// Simulación de playlists por día, puedes conectar al backend/Spotify después.
const samplePlaylists = [
  // LUNES (Reggaetón)
  [
    { id: 1, title: "DÁKITI", artists: "Bad Bunny, Jhay Cortez", album: "El Último Tour Del Mundo", duration: "3:25" },
    { id: 2, title: "Baila Baila Baila", artists: "Ozuna", album: "Aura", duration: "4:08" },
  ],
  // MARTES (Pop)
  [
    { id: 3, title: "Levitating", artists: "Dua Lipa", album: "Future Nostalgia", duration: "3:23" },
    { id: 4, title: "Watermelon Sugar", artists: "Harry Styles", album: "Fine Line", duration: "2:54" },
  ],
  // ... (agrega más canciones para cada día según lo necesites)
  // MIÉRCOLES
  [
    { id: 5, title: "Bohemian Rhapsody", artists: "Queen", album: "A Night at the Opera", duration: "5:55" },
  ],
  // JUEVES
  [
    { id: 6, title: "Titanium", artists: "David Guetta, Sia", album: "Nothing but the Beat", duration: "4:05" },
  ],
  // VIERNES
  [
    { id: 7, title: "Vivir Mi Vida", artists: "Marc Anthony", album: "3.0", duration: "4:12" },
  ],
  // SÁBADO
  [
    { id: 8, title: "Love Song", artists: "Sara Bareilles", album: "Little Voice", duration: "4:19" },
  ],
  // DOMINGO
  [
    { id: 9, title: "El Santo Cachón", artists: "Los Embajadores Vallenatos", album: "Grandes Éxitos", duration: "4:52" },
  ],
];

export default function PlaylistTable({ activeDay }) {
  const playlist = samplePlaylists[activeDay] || [];
  // Estado para ratings por canción
  const [ratings, setRatings] = useState({});

  function handleSetRating(songId, stars) {
    setRatings(prev => ({
      ...prev,
      [songId]: stars
    }));
  }

  function handleAddSong(songId) {
    alert(`Agregar canción id: ${songId}`);
    // Llama backend o actualiza estado lista aquí
  }

  function handleRemoveSong(songId) {
    alert(`Quitar canción id: ${songId}`);
    // Llama backend o actualiza estado lista aquí
  }

  return (
    <div className="mt-8">
      {/* Desktop / tablet: table view */}
      <div className="hidden md:block overflow-auto bg-gray-900 rounded-xl shadow-lg">
        <table className="w-full text-white overflow-hidden">
          <thead>
            <tr className="bg-gray-800 text-left">
              <th className="py-3 px-4">#</th>
              <th className="px-4">Título</th>
              <th className="px-4">Artista</th>
              <th className="px-4">Álbum</th>
              <th className="px-4">Duración</th>
              <th className="px-4">Rating</th>
              <th className="px-4">Acciones</th>
            </tr>
          </thead>
          <tbody>
            {playlist.map((song, idx) => (
              <tr key={song.id} className="hover:bg-gray-700 transition">
                <td className="py-2 px-4">{idx + 1}</td>
                <td className="px-4 font-semibold">{song.title}</td>
                <td className="px-4">{song.artists}</td>
                <td className="px-4">{song.album}</td>
                <td className="px-4">{song.duration}</td>
                <td className="px-4">
                  <RatingStars
                    rating={ratings[song.id] || 0}
                    onSetRating={stars => handleSetRating(song.id, stars)}
                  />
                </td>
                <td className="px-4 flex gap-2">
                  <button
                    className="bg-green-500 hover:bg-green-600 text-black font-bold px-3 py-1 rounded transition"
                    onClick={() => handleAddSong(song.id)}
                  >
                    Agregar
                  </button>
                  <button
                    className="bg-red-500 hover:bg-red-600 text-white font-bold px-3 py-1 rounded transition"
                    onClick={() => handleRemoveSong(song.id)}
                  >
                    Quitar
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Mobile: stacked cards */}
      <div className="md:hidden space-y-4">
        {playlist.map((song, idx) => (
          <div
            key={song.id}
            className="bg-gray-900 rounded-lg p-4 shadow flex items-center justify-between"
          >
            <div className="flex-1 pr-3">
              <div className="font-semibold text-white truncate">{idx + 1}. {song.title}</div>
              <div className="text-sm text-gray-300 truncate">{song.artists} • {song.album}</div>
            </div>
            <div className="flex flex-col items-end ml-3">
              <div className="text-sm text-gray-300">{song.duration}</div>
              <div className="mt-2">
                <RatingStars
                  rating={ratings[song.id] || 0}
                  onSetRating={stars => handleSetRating(song.id, stars)}
                />
              </div>
            </div>
            <div className="ml-3 flex flex-col gap-2">
              <button
                className="bg-green-500 hover:bg-green-600 text-black font-bold px-3 py-1 rounded transition text-sm"
                onClick={() => handleAddSong(song.id)}
              >
                +
              </button>
              <button
                className="bg-red-500 hover:bg-red-600 text-white font-bold px-3 py-1 rounded transition text-sm"
                onClick={() => handleRemoveSong(song.id)}
              >
                −
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}