/* 소생커뮤니티 — 설치(앱 아이콘) 요건을 맞추기 위한 최소 서비스 워커.
   캐시는 하지 않고 모든 요청을 네트워크로 그대로 보냅니다. */
self.addEventListener('install', function () { self.skipWaiting(); });
self.addEventListener('activate', function (e) { e.waitUntil(self.clients.claim()); });
self.addEventListener('fetch', function (e) { e.respondWith(fetch(e.request)); });
