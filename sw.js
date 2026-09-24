const CACHE_NAME = 'verbrauch-v27';
const urlsToCache = [
  './',
  './app.html',
  './index.html',
  './faq.html',
  './impressum.html',
  './datenschutz.html',
  './agb.html',
  './icon.svg',
  './manifest.json',
  'https://unpkg.com/lucide@latest',
  'https://cdn.jsdelivr.net/npm/chart.js',
  'https://cdn.jsdelivr.net/npm/tesseract.js@5/dist/tesseract.min.js',
  'https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js'
];

// Tailwind script via CDN and Firebase scripts can sometimes fail in addAll due to CORS/opaque responses, 
// so we'll cache them dynamically in fetch event if possible, or just let them load online.
// But we can try to cache the stable CDNs.

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        // Use a non-strict addAll approach to prevent the whole install from failing if one CDN fails
        return Promise.allSettled(
          urlsToCache.map(url => cache.add(url).catch(err => console.warn('Cache failed for', url, err)))
        );
      })
  );
});

self.addEventListener('fetch', event => {
  // Only cache GET requests
  if (event.request.method !== 'GET') return;
  // Don't cache Firestore API calls
  if (event.request.url.includes('firestore.googleapis.com')) return;

  // Network First, fallback to cache strategy
  event.respondWith(
    fetch(event.request).then(response => {
      // If we got a valid response, clone it and update the cache
      if(response && response.status === 200 && response.type === 'basic') {
        const responseToCache = response.clone();
        caches.open(CACHE_NAME).then(cache => {
          cache.put(event.request, responseToCache);
        });
      }
      return response;
    }).catch(() => {
      // If network fails (offline), return from cache
      return caches.match(event.request);
    })
  );
});
