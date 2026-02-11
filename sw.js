const CACHE_NAME = 'ttc-damme-v1';
const ASSETS = [
    'index.html',
    'style.css',
    'app.js',
    'data.js',
    'icon.png'
];

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => cache.addAll(ASSETS))
    );
});

self.addEventListener('fetch', (event) => {
    // Basic network-first strategy for data update flexibility
    event.respondWith(
        fetch(event.request).catch(() => {
            return caches.match(event.request);
        })
    );
});
