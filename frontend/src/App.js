import React, { useState } from 'react';
import './App.css';
import MovieReel from './components/MovieReel';
import SearchBar from './components/SearchBar';
import HeroCard from './components/HeroCard';
import MovieCard from './components/MovieCard';
import { getRecommendations } from './services/api';

function App() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedMovie, setSelectedMovie] = useState(null);
  const [recommendations, setRecommendations] = useState([]);

  const handleSearch = async (movieName) => {
    setLoading(true);
    setError(null);
    setSelectedMovie(null);
    setRecommendations([]);

    try {
      const data = await getRecommendations(movieName);
      setSelectedMovie(data.selected_movie);
      setRecommendations(data.recommendations);
    } catch (err) {
      setError('Movie not found or server error. Please try another movie.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="header">
        <h1 className="logo">MovieMind</h1>
        <p className="tagline">Discover Your Next Favorite Film</p>
      </header>

      <MovieReel />

      <SearchBar onSearch={handleSearch} />

      {loading && (
        <div className="loading">
          <p>Finding perfect recommendations...</p>
        </div>
      )}

      {error && (
        <div className="error">
          <p>{error}</p>
        </div>
      )}

      {!loading && !error && selectedMovie && (
        <div className="results-section">
          <HeroCard movie={selectedMovie} />

          {recommendations.length > 0 && (
            <>
              <h2 className="recommendations-title">
                Recommended For You
              </h2>
              <div className="recommendations-grid">
                {recommendations.map((movie, index) => (
                  <MovieCard key={index} movie={movie} />
                ))}
              </div>
            </>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
