import React, { useEffect, useState } from 'react';
import { getPopularMovies } from '../services/api';

const MovieReel = () => {
  const [movies, setMovies] = useState([]);

  useEffect(() => {
    const loadPopularMovies = async () => {
      try {
        const popularMovies = await getPopularMovies();
        // Duplicate the array for seamless infinite scroll
        setMovies([...popularMovies, ...popularMovies]);
      } catch (error) {
        console.error('Failed to load popular movies:', error);
      }
    };

    loadPopularMovies();
  }, []);

  if (movies.length === 0) {
    return null;
  }

  return (
    <div className="movie-reel-container">
      <div className="movie-reel">
        {movies.map((movie, index) => (
          movie.poster && (
            <img
              key={`${movie.id}-${index}`}
              src={movie.poster}
              alt={movie.title}
              className="reel-poster"
            />
          )
        ))}
      </div>
    </div>
  );
};

export default MovieReel;
