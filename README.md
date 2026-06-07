# E Blue Artist

A simple art blog hosted on [GitHub Pages](https://pages.github.com/) at [www.e-blue-artist.com](https://www.e-blue-artist.com).

## Contents

- **Materials** — honest art supply recommendations for beginners
- **Art Tips** — short, practical techniques
- **Artist Spotlight** — interesting artists worth knowing

## Local preview

Open `index.html` in a browser, or run a local server:

```bash
python -m http.server 8000
```

Then visit `http://localhost:8000`.

## Deploy

Push to the `main` branch of [eblueartist/e-blue-artist](https://github.com/eblueartist/e-blue-artist). GitHub Pages serves the site automatically. The `CNAME` file points the custom domain to `www.e-blue-artist.com`.

## Structure

```
├── index.html          Home page & blog listing
├── posts/              Individual blog posts
├── css/style.css       Nautical theme styles
├── js/main.js          Mobile navigation
├── assets/logo.png     Site logo
└── CNAME               Custom domain config
```
