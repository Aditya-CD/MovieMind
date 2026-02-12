# MovieMind: Cinematic Interface

MovieMind is a high-fidelity React-based dashboard designed to provide an immersive discovery experience for machine learning-driven movie recommendations. The interface utilizes modern CSS techniques and asynchronous data fetching to bridge the gap between complex backend logic and user-centric design.

## Technical Overview

The application is architected to handle real-time metadata rendering from a FastAPI backend while maintaining a consistent visual performance. Key technical implementations include:

* **Asynchronous Data Flow:** Managed through the Fetch API to coordinate between the ML recommendation engine and the TMDB image server.
* **State Management:** Robust handling of loading, error, and success states to ensure a smooth user journey.
* **CSS Architecture:** A variable-driven design system utilizing CSS Grid for layout integrity and Flexbox for component-level alignment.
* **Performance Optimization:** Strategic use of hardware-accelerated CSS properties for animations and backdrop-filter effects.

## Features

* **Dynamic Search Engine:** A controlled component with an autocomplete dropdown that allows for rapid selection from the 4,800+ movie dataset.
* **Glassmorphism UI:** Implementation of backdrop-filter blurs and semi-transparent layers to create a modern, premium aesthetic.
* **Infinite Motion Reel:** A CSS-animated movie reel that provides continuous visual engagement.
* **Responsive Layout:** A grid-based system that reconfigures dynamically from a 5-column desktop view to optimized mobile layouts.

## Setup and Installation

### Prerequisites
* Node.js (Version 14 or higher)
* A running instance of the MovieMind Backend (FastAPI)
* A valid TMDB API Key for fetching movie posters

### Local Development

1.  **Clone the repository and install dependencies:**

    Bash

    ```
    git clone https://github.com/Aditya-CD/MovieMind.git
    cd moviemind-frontend
    npm install

    ```

2.  **Configure API Credentials:** Open `src/services/api.js` and input your TMDB API Key:

    JavaScript

    ```
    const TMDB_API_KEY = 'YOUR_ACTUAL_API_KEY';

    ```

3.  **Launch the Application:**

    Bash

    ```
    npm start

    ```

Project Architecture
--------------------

Plaintext

```
src/
├── components/
│   ├── MovieReel.js      # Handles infinite horizontal scroll animation
│   ├── SearchBar.js      # Manages selection logic and autocomplete
│   ├── HeroCard.js       # Renders primary movie data and metadata
│   └── MovieCard.js      # Individual recommendation units with hover overlays
├── services/
│   └── api.js            # Centralized API service for backend and TMDB
├── App.js                # Core application controller
└── App.css               # Global design system and CSS variables

```

UI System and Variables
-----------------------

The theme is controlled via CSS custom properties located in the `:root` selector. This allows for rapid brand pivoting without modifying individual component files.

-   **Typography:** The Serif `Cinzel` font is used for high-impact display titles, while `Montserrat` handles data-heavy body text.

-   **Color Palette:** A deep cinematic base (`#0a0a0f`) accented by purple and gold gradients to signify premium quality.

-   **Layout:** Strict adherence to a 5-column grid to ensure symmetry in recommendation results.

Production Deployment
---------------------

To generate an optimized build for production:

Bash

```
npm run build

```

This will produce a `build/` directory containing minified assets ready for deployment on services such as Netlify, Vercel, or GitHub Pages.

* * * * *

**Developed for the MovieMind Machine Learning Project.**