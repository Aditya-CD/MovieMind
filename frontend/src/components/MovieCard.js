import React, { useEffect, useState } from 'react';
import { getMoviePoster } from '../services/api';

const MovieCard = ({ movie }) => {
  const [posterUrl, setPosterUrl] = useState(null);

  useEffect(() => {
    const loadPoster = async () => {
      const url = await getMoviePoster(movie.id, movie.title);
      setPosterUrl(url);
    };

    loadPoster();
  }, [movie.id, movie.title]);

  const formatRating = (rating) => {
    return rating ? rating.toFixed(1) : 'N/A';
  };

  return (
    <div className="movie-card">
      <div className="movie-poster-container">
        <img
          src={posterUrl || 'https://via.placeholder.com/500x750/1a1a24/667eea?text=Loading...'}
          alt={movie.title}
          className="movie-poster"
        />
        
        <div className="movie-overlay">
          <h3 className="overlay-title">{movie.title}</h3>
          
          <div className="overlay-meta">
            {movie.vote_average > 0 && (
              <span>⭐ {formatRating(movie.vote_average)}</span>
            )}
            {movie.release_date && (
              <span>📅 {new Date(movie.release_date).getFullYear()}</span>
            )}
          </div>
          
          {movie.overview && (
            <p className="overlay-overview">{movie.overview}</p>
          )}
          
          {movie.genres && movie.genres.length > 0 && (
            <div className="overlay-genres">
              {movie.genres.slice(0, 3).map((genre, index) => (
                <span key={index} className="overlay-genre">
                  {genre}
                </span>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default MovieCard;
