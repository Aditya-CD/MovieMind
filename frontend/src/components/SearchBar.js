import React, { useState, useEffect, useRef } from 'react';
import { fetchAllMovies } from '../services/api';

const SearchBar = ({ onSearch }) => {
  const [query, setQuery] = useState('');
  const [allMovies, setAllMovies] = useState([]);
  const [filteredMovies, setFilteredMovies] = useState([]);
  const [showDropdown, setShowDropdown] = useState(false);
  const dropdownRef = useRef(null);

  useEffect(() => {
    const loadMovies = async () => {
      try {
        const movies = await fetchAllMovies();
        setAllMovies(movies);
      } catch (error) {
        console.error('Failed to load movies:', error);
      }
    };

    loadMovies();
  }, []);

  useEffect(() => {
    if (query.length > 0) {
      const filtered = allMovies
        .filter(movie => movie.toLowerCase().includes(query.toLowerCase()))
        .slice(0, 10); // Show top 10 matches
      setFilteredMovies(filtered);
      setShowDropdown(filtered.length > 0);
    } else {
      setFilteredMovies([]);
      setShowDropdown(false);
    }
  }, [query, allMovies]);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setShowDropdown(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleInputChange = (e) => {
    setQuery(e.target.value);
  };

  const handleSelectMovie = (movie) => {
    setQuery(movie);
    setShowDropdown(false);
    onSearch(movie);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && query.trim()) {
      setShowDropdown(false);
      onSearch(query);
    }
  };

  return (
    <div className="search-section">
      <div className="search-container" ref={dropdownRef}>
        <input
          type="text"
          className="search-input"
          placeholder="Search for a movie..."
          value={query}
          onChange={handleInputChange}
          onKeyPress={handleKeyPress}
        />
        
        {showDropdown && (
          <div className="dropdown">
            {filteredMovies.map((movie, index) => (
              <div
                key={index}
                className="dropdown-item"
                onClick={() => handleSelectMovie(movie)}
              >
                {movie}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default SearchBar;
