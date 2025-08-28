# PWA Boilerplate Tech Stack (2025)

## Core Framework
- **Next.js 15.3+** - App Router, Server Components, edge runtime support
- **React 19** - Latest concurrent features
- **TypeScript 5.6+** - Type safety throughout

## Styling & UI
- **Tailwind CSS v4** - CSS-based config, OKLCH colors
- **shadcn/ui** - Component library with tw-animate-css
- **Lucide React** - Optimized icon library

## State Management
- **TanStack Query v5** - Server state, caching, background refetch
- **Zustand** - Client state (UI, local preferences)
- **@tanstack/react-query-persist-client** - IndexedDB persistence

## Offline-First Architecture
- **PowerSync** - Supabase sync with offline support
- **@serwist/next** - Service worker (Workbox fork)
- **IndexedDB** - Local structured data via TanStack persistence
- **Cache API** - Network resources caching

## Backend & Database
- **Supabase** - Auth, Postgres, real-time, storage
- **Edge Functions** - Serverless APIs on Vercel Edge
- **Row Level Security** - Database-level auth

## Forms & Validation
- **React Hook Form** - Performant form handling
- **Zod** - Schema validation, TypeScript inference
- **@hookform/resolvers** - Zod integration

## Testing
- **Vitest** - Unit tests, component tests
- **Playwright** - E2E tests, PWA testing
- **React Testing Library** - Component testing

## Monitoring & Analytics
- **PostHog** - Product analytics, session replay, feature flags, web vitals
- **Sentry** - Error tracking, performance monitoring

## Development Tools
- **pnpm** - Fast, disk-efficient package manager
- **Biome** - Fast linting/formatting (replaces ESLint+Prettier)

## Deployment
- **Vercel** - Auto-deploy on push, edge functions, preview deployments

## PWA Configuration
```json
{
  "manifest": {
    "name": "App Name",
    "short_name": "App",
    "theme_color": "#0a0a0a",
    "background_color": "#0a0a0a",
    "display": "standalone",
    "orientation": "portrait",
    "scope": "/",
    "start_url": "/"
  },
  "workbox": {
    "runtimeCaching": [
      {
        "urlPattern": "/api/",
        "handler": "NetworkFirst",
        "options": {
          "networkTimeoutSeconds": 3,
          "cacheName": "api-cache"
        }
      }
    ]
  }
}
```

## Directory Structure
```
/
├── app/                    # Next.js App Router
│   ├── (auth)/            # Auth group routes
│   ├── api/               # API routes
│   └── _components/       # Private components
├── components/            # Shared components
│   └── ui/               # shadcn/ui components
├── lib/                   # Utilities
│   ├── supabase/         # Supabase client
│   ├── powersync/        # PowerSync setup
│   └── validations/      # Zod schemas
├── hooks/                # Custom React hooks
├── public/              
│   └── icons/           # PWA icon set
└── tests/
    ├── unit/           # Vitest tests
    └── e2e/            # Playwright tests
```

## Key Features
- **100 Lighthouse Score** - Optimized performance by default
- **Offline-First** - Works without connection
- **Type-Safe** - End-to-end TypeScript
- **Real-time Sync** - PowerSync + Supabase
- **Edge Optimized** - Vercel Edge Runtime
- **Accessible** - WCAG 2.1 AA compliant
- **Secure** - CSP headers, RLS, auth

## Sub-Agents Configuration

### Core Development Agents
1. **frontend** - Generate UI components matching tech stack
2. **backend** - Build Supabase APIs and Edge Functions
3. **tester** - Run Vitest and Playwright tests
4. **optimizer** - Performance optimization for PWA
5. **reviewer** - Code review based on stack conventions

### Commands (not agents)
- `/init` - Initialize project with this tech stack
- `/upgrade` - Update dependencies

## Package List

### Dependencies
```json
{
  "next": "^15.3.0",
  "react": "^19.0.0",
  "react-dom": "^19.0.0",
  "@supabase/supabase-js": "^2.45.0",
  "@supabase/ssr": "^0.5.0",
  "@tanstack/react-query": "^5.0.0",
  "@tanstack/react-query-persist-client": "^5.0.0",
  "zustand": "^5.0.0",
  "react-hook-form": "^7.53.0",
  "zod": "^3.23.0",
  "@hookform/resolvers": "^3.9.0",
  "tailwindcss": "^4.0.0",
  "lucide-react": "^0.460.0",
  "@serwist/next": "^9.0.0",
  "@powersync/react": "^1.0.0"
}
```

### Dev Dependencies
```json
{
  "typescript": "^5.6.0",
  "@types/react": "^19.0.0",
  "@types/node": "^22.0.0",
  "vitest": "^2.0.0",
  "@playwright/test": "^1.48.0",
  "@testing-library/react": "^16.0.0",
  "@biomejs/biome": "^1.9.0"
}
```

## Environment Variables
```env
# Supabase
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=

# PowerSync
NEXT_PUBLIC_POWERSYNC_URL=
POWERSYNC_SERVICE_KEY=

# PostHog
NEXT_PUBLIC_POSTHOG_KEY=
NEXT_PUBLIC_POSTHOG_HOST=

# Sentry
NEXT_PUBLIC_SENTRY_DSN=
SENTRY_AUTH_TOKEN=
```

This configuration represents the optimal PWA-first tech stack for 2025, thoroughly researched and production-ready.