import { defaultCache } from '@serwist/next/browser'
import type { PrecacheEntry } from '@serwist/precaching'
import { installSerwist } from '@serwist/sw'

declare const self: ServiceWorkerGlobalScope & {
  __SW_MANIFEST: (PrecacheEntry | string)[]
  __BUILD_ID: string
  __BUILD_TIME: string
}

const revision = self.__BUILD_ID + self.__BUILD_TIME

installSerwist({
  precacheEntries: self.__SW_MANIFEST,
  skipWaiting: true,
  clientsClaim: true,
  navigationPreload: true,
  runtimeCaching: [
    ...defaultCache,
    {
      urlPattern: /^https:\/\/fonts\.(?:googleapis|gstatic)\.com\/.*/i,
      handler: 'CacheFirst',
      options: {
        cacheName: 'google-fonts',
        expiration: {
          maxEntries: 10,
          maxAgeSeconds: 60 * 60 * 24 * 365, // 365 days
        },
      },
    },
    {
      urlPattern: /^https:\/\/cdn\.jsdelivr\.net\/.*/i,
      handler: 'CacheFirst',
      options: {
        cacheName: 'jsdelivr',
        expiration: {
          maxEntries: 10,
          maxAgeSeconds: 60 * 60 * 24 * 365, // 365 days
        },
      },
    },
    {
      urlPattern: ({ url }) => {
        const isSameOrigin = self.location.origin === url.origin
        if (!isSameOrigin) return false
        const pathname = url.pathname
        // Exclude /api/auth/* to avoid caching auth responses
        if (pathname.startsWith('/api/auth/')) return false
        if (pathname.startsWith('/api/')) return true
        return false
      },
      handler: 'NetworkFirst',
      options: {
        cacheName: 'api-cache',
        networkTimeoutSeconds: 3,
        expiration: {
          maxEntries: 50,
          maxAgeSeconds: 60 * 5, // 5 minutes
        },
        cacheableResponse: {
          statuses: [0, 200],
        },
      },
    },
    {
      urlPattern: ({ url }) => {
        const isSameOrigin = self.location.origin === url.origin
        if (!isSameOrigin) return false
        const pathname = url.pathname
        const isImage = /\.(png|jpg|jpeg|svg|gif|webp|avif)$/.test(pathname)
        return isImage
      },
      handler: 'CacheFirst',
      options: {
        cacheName: 'images',
        expiration: {
          maxEntries: 100,
          maxAgeSeconds: 60 * 60 * 24 * 30, // 30 days
        },
      },
    },
  ],
  fallbacks: {
    entries: [
      {
        url: '/offline',
        revision,
        matcher: ({ request }) => request.destination === 'document',
      },
    ],
  },
})