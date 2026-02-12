import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000';
const TMDB_API_KEY = '4512aeeeacb7923520deb43aae7bda48';
const TMDB_IMAGE_BASE = 'https://image.tmdb.org/t/p/w500';

// Fetch all available movie titles
export const fetchAllMovies = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/movies`);
    return response.data.movies;
  } catch (error) {
    console.error('Error fetching movies:', error);
    throw error;
  }
};

// Get movie recommendations
export const getRecommendations = async (movieName) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/recommend/${encodeURIComponent(movieName)}`);
    return response.data;
  } catch (error) {
    console.error('Error getting recommendations:', error);
    throw error;
  }
};

// Search TMDB for movie poster by movie ID
export const getTMDBPoster = async (movieId) => {
  try {
    const response = await axios.get(
      `https://api.themoviedb.org/3/movie/${movieId}?api_key=${TMDB_API_KEY}`
    );
    
    if (response.data.poster_path) {
      return `${TMDB_IMAGE_BASE}${response.data.poster_path}`;
    }
    return null;
  } catch (error) {
    console.error('Error fetching TMDB poster:', error);
    return null;
  }
};

// Fallback: Search TMDB by movie title if ID doesn't work
export const searchTMDBByTitle = async (title) => {
  try {
    const response = await axios.get(
      `https://api.themoviedb.org/3/search/movie?api_key=${TMDB_API_KEY}&query=${encodeURIComponent(title)}`
    );
    
    if (response.data.results && response.data.results.length > 0) {
      const movie = response.data.results[0];
      if (movie.poster_path) {
        return `${TMDB_IMAGE_BASE}${movie.poster_path}`;
      }
    }
    return null;
  } catch (error) {
    console.error('Error searching TMDB:', error);
    return null;
  }
};

// Combined function to get poster with fallbacks
export const getMoviePoster = async (movieId, movieTitle) => {
  // Try TMDB ID first
  let posterUrl = await getTMDBPoster(movieId);
  
  // If ID fails, search by title
  if (!posterUrl) {
    posterUrl = await searchTMDBByTitle(movieTitle);
  }
  
  // Return placeholder if both fail
  return posterUrl || 'https://via.placeholder.com/500x750/1a1a24/667eea?text=No+Poster';
};

// Fetch popular movies for the revolving reel (using TMDB trending)
export const getPopularMovies = async () => {
  try {
    const response = await axios.get(
      `https://api.themoviedb.org/3/trending/movie/week?api_key=${TMDB_API_KEY}`
    );
    
    return response.data.results.map(movie => ({
      id: movie.id,
      title: movie.title,
      poster: movie.poster_path ? `${TMDB_IMAGE_BASE}${movie.poster_path}` : null
    }));
  } catch (error) {
    console.error('Error fetching popular movies:', error);
    return [];
  }
};
