const CACHE_NAME = 'verbrauch-v1';
const urlsToCache = [
  './',
  './index.html',
  './icon.svg',
  './manifest.json',
  'https://unpkg.com/lucide@latest',
  'https://cdn.jsdelivr.net/npm/chart.js',
  'https://cdn.jsdelivr.net/npm/tesseract.js@5/dist/tesseract.min.js'
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

  event.respondWith(
    caches.match(event.request)
      .then(response => {
        if (response) {
          return response;
        }
        return fetch(event.request).then(
          function(response) {
            // Check if we received a valid response
            if(!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }

            // IMPORTANT: Clone the response. A response is a stream
            // and because we want the browser to consume the response
            // as well as the cache consuming the response, we need
            // to clone it so we have two streams.
            var responseToCache = response.clone();

            caches.open(CACHE_NAME)
              .then(function(cache) {
                cache.put(event.request, responseToCache);
              });

            return response;
          }
        );
      })
  );
});
