/* ZEUS · Service worker: funciona sin conexión (cache-first del "app shell"). */
const CACHE = 'zeus-v4.1.0';
const SHELL = [
  './', 'index.html', 'manifest.webmanifest',
  'assets/fonts/sora-latin-var.woff2', 'assets/fonts/dm-sans-latin-var.woff2',
  'assets/icons/favicon.svg', 'assets/icons/favicon-32.png',
  'assets/icons/icon-192.png', 'assets/icons/icon-512.png',
  'assets/icons/icon-maskable-192.png', 'assets/icons/icon-maskable-512.png',
  'data/historial-inicial.json'
];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  const url = new URL(e.request.url);
  if (url.origin !== location.origin) return;
  e.respondWith(
    caches.match(e.request, {ignoreSearch: true}).then(hit =>
      hit || fetch(e.request).then(res => {
        if (res.ok) { const copy = res.clone(); caches.open(CACHE).then(c => c.put(e.request, copy)); }
        return res;
      }).catch(() => caches.match('index.html'))
    )
  );
});
