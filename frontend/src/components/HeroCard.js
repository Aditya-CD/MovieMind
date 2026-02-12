import React, { useEffect, useState } from 'react';
import { getMoviePoster } from '../services/api';

const HeroCard = ({ movie }) => {
  const [posterUrl, setPosterUrl] = useState(null);

  useEffect(() => {
    const loadPoster = async () => {
      const url = await getMoviePoster(movie.id, movie.title);
      setPosterUrl(url);
    };

    loadPoster();
  }, [movie.id, movie.title]);

  const formatRuntime = (minutes) => {
    if (!minutes) return 'N/A';
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return `${hours}h ${mins}m`;
  };

  const formatRating = (rating) => {
    return rating ? rating.toFixed(1) : 'N/A';
  };

  return (
    <div className="hero-card">
      <img
        src={posterUrl || 'https://via.placeholder.com/280x420/1a1a24/667eea?text=Loading...'}
        alt={movie.title}
        className="hero-poster"
      />
      
      <div className="hero-details">
        <h2 className="hero-title">{movie.title}</h2>
        
        <div className="hero-meta">
          {movie.vote_average > 0 && (
            <div className="meta-item">
              <span className="meta-icon">⭐</span>
              <span>{formatRating(movie.vote_average)}/10</span>
            </div>
          )}
          
          {movie.runtime > 0 && (
            <div className="meta-item">
              <span className="meta-icon">🕐</span>
              <span>{formatRuntime(movie.runtime)}</span>
            </div>
          )}
          
          {movie.release_date && (
            <div className="meta-item">
              <span className="meta-icon">📅</span>
              <span>{new Date(movie.release_date).getFullYear()}</span>
            </div>
          )}
        </div>
        
        {movie.overview && (
          <p className="hero-overview">{movie.overview}</p>
        )}
        
        {movie.genres && movie.genres.length > 0 && (
          <div className="hero-genres">
            <div className="label">Genres</div>
            <div className="genre-tags">
              {movie.genres.map((genre, index) => (
                <span key={index} className="genre-tag">
                  {genre}
                </span>
              ))}
            </div>
          </div>
        )}
        
        {movie.cast && movie.cast.length > 0 && (
          <div className="hero-cast">
            <div className="label">Cast</div>
            <div className="cast-list">
              {movie.cast.join(' • ')}
            </div>
          </div>
        )}
        
        {movie.director && (
          <div className="hero-cast">
            <div className="label">Director</div>
            <div className="cast-list">
              {movie.director}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default HeroCard;
