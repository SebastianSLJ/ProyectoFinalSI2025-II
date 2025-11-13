import React from 'react';

export default function TopSongsTable({ songs }) {
  return (
    <table className="w-full text-white bg-gray-900 rounded-xl shadow-lg overflow-hidden">
      <thead>
        <tr className="bg-gray-800 text-left">
          <th className="px-4 py-3">#</th>
          <th className="px-4 py-3">Título</th>
          <th className="px-4 py-3">Artista</th>
          <th className="px-4 py-3">Rating</th>
        </tr>
      </thead>
      <tbody>
        {songs.map((song, i) => (
          <tr key={song.id} className="hover:bg-gray-700 transition">
            <td className="px-4 py-3">{i + 1}</td>
            <td className="px-4 py-3 font-semibold">{song.title}</td>
            <td className="px-4 py-3">{song.artist}</td>
            <td className="px-4 py-3">
              {'★'.repeat(song.rating)}{'☆'.repeat(5 - song.rating)}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
