import React from 'react';

export default function RatingStars({ rating, onSetRating }) {
  return (
    <div className="flex">
      {Array.from({ length: 5 }).map((_, idx) => (
        <button
          key={idx}
          className="text-yellow-400 mx-px text-lg focus:outline-none"
          onClick={() => onSetRating(idx + 1)}
          type="button"
        >
          {idx < rating ? '★' : '☆'}
        </button>
      ))}
    </div>
  );
}
