import React from 'react';
import SongCard from './SongCard.jsx';

export default function SongListSection({ title, songs }) {
  return (
    <section className="my-8">
      <h2 className="mb-4 text-2xl font-bold text-slate-900 text-white">
        {title}
      </h2>
      <div className="flex flex-wrap gap-6">
        {songs.map(song => (
          <SongCard key={song.id} song={song} />
        ))}
      </div>
    </section>
  );
}
