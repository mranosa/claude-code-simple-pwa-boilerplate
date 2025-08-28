# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Progressive Web Application (PWA) boilerplate built with Next.js 15, TypeScript, and Supabase. It provides offline-first functionality with PowerSync, service worker support via Serwist, and a modern React 19 setup.

## Development Commands

```bash
pnpm dev          # Start development server (port 3000)
pnpm build        # Build for production
pnpm start        # Start production server
pnpm lint         # Run Biome linter and auto-fix issues
pnpm format       # Format code with Biome
pnpm typecheck    # Run TypeScript type checking
pnpm test         # Run unit tests with Vitest
pnpm test:e2e     # Run E2E tests with Playwright
```

### Testing Specific Files
```bash
pnpm test path/to/file.test.ts     # Run specific unit test
pnpm test:e2e path/to/test.spec.ts # Run specific E2E test
```

## Architecture

### Tech Stack
- **Frontend**: Next.js 15 (App Router), React 19, TypeScript 5.6+
- **Styling**: Tailwind CSS v4, shadcn/ui components
- **State Management**: 
  - TanStack Query v5 for server state
  - Zustand for client state
- **Offline Support**: PowerSync + Supabase, Serwist (service worker)
- **Forms**: React Hook Form + Zod validation
- **Testing**: Vitest (unit), Playwright (E2E)
- **Code Quality**: Biome (linting/formatting), TypeScript

### Directory Structure
```
app/                 # Next.js App Router pages
├── (auth)/         # Auth group routes
├── api/            # API routes
├── _components/    # Private route components
├── sw.ts          # Service worker configuration
└── providers.tsx   # React Query provider setup

components/         # Shared UI components
├── ui/            # shadcn/ui components

lib/               # Utilities and integrations
├── supabase/      # Supabase client setup
├── powersync/     # PowerSync configuration
├── validations/   # Zod schemas
└── utils.ts       # Helper functions

hooks/             # Custom React hooks
tests/             # Test files
├── unit/          # Vitest unit tests
├── e2e/           # Playwright E2E tests
└── setup.ts       # Test setup file
```

### Key Configurations

#### Next.js Configuration
- Service worker enabled via Serwist (disabled in development)
- Typed routes enabled for type-safe navigation
- Security headers configured (CSP, XSS protection, etc.)
- Image optimization for AVIF and WebP formats

#### Testing Setup
- Vitest with React Testing Library for unit tests
- Playwright configured for Chrome, Firefox, Safari, and mobile browsers
- Test coverage reporting enabled
- Path aliases configured (@/components, @/lib, etc.)

#### Code Style
- Biome for linting and formatting
- 2 spaces indentation
- Single quotes for JS, double quotes for JSX
- 100 character line width
- Semicolons as needed (ASI)

### PWA Features
- Manifest file at `/public/manifest.json`
- Service worker with offline page support
- Install prompt component integration
- Network-first caching strategy for API routes

### Environment Variables Required
```env
# Supabase (Required)
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=

# Optional
ELEVENLABS_API_KEY=
NEXT_PUBLIC_POSTHOG_KEY=
```

## Important Patterns

### Component Structure
- Use functional components with TypeScript
- Follow existing shadcn/ui patterns for new UI components
- Client components marked with 'use client' directive
- Server components by default in App Router

### State Management
- Use TanStack Query for server data fetching
- Zustand for UI state and local preferences
- React Hook Form for form handling
- Always validate with Zod schemas

### Error Handling
- Retry logic configured in QueryClient (max 2 retries)
- Skip retries for 404 and 401 errors
- 1-minute stale time for queries

### Security Best Practices
- Row Level Security enabled in Supabase
- Security headers configured in next.config.mjs
- Never commit sensitive data or API keys
- Use environment variables for configuration