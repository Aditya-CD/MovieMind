# 🎬 MovieMind - Complete Setup Guide

## 📋 What You Have

A complete, production-ready React frontend with:
- ✅ Cinematic dark theme with glassmorphism
- ✅ Revolving movie reel animation
- ✅ Smart autocomplete search
- ✅ Hero card for selected movie
- ✅ 5 interactive recommendation cards
- ✅ TMDB API integration for posters
- ✅ Responsive design
- ✅ Premium animations and effects

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Get Your TMDB API Key

1. Go to https://www.themoviedb.org/signup
2. Create a free account
3. Go to Settings → API → Create → Developer
4. Copy your API Key (v3 auth)

### Step 2: Setup the Frontend

```bash
# Navigate to the frontend folder
cd moviemind-frontend

# Install dependencies (this will take 2-3 minutes)
npm install

# IMPORTANT: Add your TMDB API key
# Open src/services/api.js in a text editor
# Replace 'YOUR_TMDB_API_KEY_HERE' with your actual key
```

### Step 3: Start Everything

**Terminal 1 - Backend:**
```bash
cd backend
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd moviemind-frontend
npm start
```

### Step 4: Open & Enjoy!

- Frontend: http://localhost:3000
- Backend: http://127.0.0.1:8000

---

## 🎨 Design Highlights

### Visual Features
- **Cinzel** font for dramatic titles
- **Montserrat** for clean body text
- Purple-blue gradients (#667eea → #764ba2)
- Glass effect cards with backdrop blur
- Particle background animations
- Smooth hover interactions

### User Experience
1. **Landing**: See revolving reel of trending movies
2. **Search**: Type and get instant autocomplete
3. **Select**: Click or press Enter
4. **Discover**: Hero card + 5 recommendations
5. **Explore**: Hover cards for full details

---

## 📁 File Structure

```
moviemind-frontend/
├── public/
│   └── index.html              # HTML template
├── src/
│   ├── components/
│   │   ├── MovieReel.js        # Infinite scroll animation
│   │   ├── SearchBar.js        # Search with dropdown
│   │   ├── HeroCard.js         # Selected movie card
│   │   └── MovieCard.js        # Recommendation card
│   ├── services/
│   │   └── api.js              # ⚠️ ADD YOUR TMDB KEY HERE
│   ├── App.js                  # Main component
│   ├── App.css                 # All styles
│   ├── index.js                # Entry point
│   └── index.css               # Base CSS
├── package.json                # Dependencies
└── README.md                   # Documentation
```

---

## 🔧 Customization Options

### Change Colors
Edit `src/App.css` variables:
```css
:root {
  --color-bg-primary: #0a0a0f;        /* Main background */
  --gradient-primary: linear-gradient(...);  /* Card accents */
  --color-accent: #667eea;            /* Highlight color */
}
```

### Change Backend URL
If backend runs on different port, edit `src/services/api.js`:
```javascript
const API_BASE_URL = 'http://127.0.0.1:YOUR_PORT';
```

### Adjust Animation Speed
In `src/App.css`, find:
```css
animation: scroll-left 40s linear infinite;
/* Change 40s to make faster/slower */
```

---

## 🐛 Common Issues & Fixes

### Issue: "npm install" fails
**Fix**: 
```bash
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### Issue: Posters not loading
**Fix**: 
- Check TMDB API key in `src/services/api.js`
- Verify API key is valid at https://www.themoviedb.org/settings/api
- Check browser console for CORS errors

### Issue: Backend connection error
**Fix**:
- Ensure backend is running: `uvicorn app.main:app --reload`
- Check backend URL in `src/services/api.js`
- Verify CORS is enabled in backend (already done in your main.py)

### Issue: Dropdown not showing
**Fix**:
- Check `/movies` endpoint: http://127.0.0.1:8000/movies
- Ensure it returns `{"movies": [...]}`
- Check browser console for errors

### Issue: Build fails
**Fix**:
```bash
npm install react-scripts@latest
npm run build
```

---

## 🎯 Features Breakdown

### MovieReel Component
- Fetches trending movies from TMDB
- Duplicates array for seamless infinite scroll
- Pauses on hover
- Grayscale effect with color on hover

### SearchBar Component
- Loads all available movies on mount
- Real-time filtering (top 10 matches)
- Click outside to close dropdown
- Enter key to search

### HeroCard Component
- Large poster with glassmorphism card
- Displays: rating, runtime, year, genres, cast, director
- Smooth scale animation on hover
- Gradient text for title

### MovieCard Component
- Poster with overlay on hover
- Shows: title, rating, year, overview, genres
- Reveal animation from bottom
- Scales up on hover

---

## 📊 API Integration Details

### Backend Endpoints Used
```
GET /movies           → All movie titles (autocomplete)
GET /recommend/{name} → Get recommendations
```

### TMDB Endpoints Used
```
GET /trending/movie/week     → Popular movies (reel)
GET /movie/{id}              → Movie details by ID
GET /search/movie            → Fallback search by title
```

### Poster Loading Logic
1. Try TMDB with movie ID from your database
2. If fails, search TMDB by movie title
3. If fails, show placeholder image

---

## 🚀 Production Deployment

### Build for Production
```bash
npm run build
```

Creates optimized build in `build/` folder.

### Deploy Options
- **Vercel**: `vercel --prod`
- **Netlify**: Drag & drop `build/` folder
- **GitHub Pages**: See React docs
- **Your server**: Serve `build/` folder with nginx/Apache

### Environment Variables
For production, use `.env` file:
```
REACT_APP_API_URL=https://your-backend.com
REACT_APP_TMDB_KEY=your_key
```

Then in code:
```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL;
const TMDB_API_KEY = process.env.REACT_APP_TMDB_KEY;
```

---

## 🎨 Design Philosophy

This isn't just another Netflix clone. MovieMind has:

1. **Unique Typography**: Cinzel for drama, not overused Inter/Roboto
2. **Bold Gradients**: Purple-blue cinema feel, not cliché Netflix red
3. **Glassmorphism**: Modern, premium aesthetic
4. **Cinematic Dark**: Deep blacks with particle effects
5. **Smooth Animations**: Intentional, not excessive
6. **Responsive**: Mobile-first, scales beautifully

---

## 📝 Next Steps (Optional Enhancements)

Want to add more features? Consider:

- [ ] User accounts & watchlists
- [ ] Multiple recommendation algorithms
- [ ] Trailer integration (YouTube API)
- [ ] Advanced filters (genre, year, rating)
- [ ] Social sharing
- [ ] Light theme toggle
- [ ] Movie details page
- [ ] Save/export recommendations
- [ ] Rate movies to improve recommendations
- [ ] Voice search

---

## 🙏 Credits

- **TMDB**: Movie data and posters
- **Google Fonts**: Cinzel & Montserrat
- **React**: UI framework
- **Axios**: HTTP client
- **Framer Motion**: (Available for future animations)

---

## 📞 Support

If you encounter issues:
1. Check this guide's troubleshooting section
2. Inspect browser console (F12)
3. Check backend logs
4. Verify all dependencies installed
5. Ensure backend models are built

---

**Happy movie discovering! 🎬🍿**
