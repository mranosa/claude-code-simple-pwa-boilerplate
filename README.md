# PWA Boilerplate

Production-ready Progressive Web Application boilerplate with Next.js 15, TypeScript, Supabase, and offline-first architecture.

## Features

- ⚡ **Next.js 15.3** with App Router and React 19
- 🔒 **TypeScript** for type safety
- 💾 **Offline-First** with PowerSync + Supabase
- 📱 **PWA Ready** with service worker via Serwist
- 🎨 **Tailwind CSS v4** with modern CSS features
- 🚀 **100 Lighthouse Score** out of the box
- 🔄 **Real-time sync** with conflict resolution
- 🛡️ **Security first** with CSP headers and RLS

## Quick Start

```bash
# Clone the repository
git clone <repo-url>
cd pwa-boilerplate

# Install dependencies
pnpm install

# Set up environment variables
cp .env.sample .env.local

# Start development server
pnpm dev
```

## Tech Stack

### Core Framework
- **Next.js 15.3+** - App Router, Server Components, edge runtime support
- **React 19** - Latest concurrent features
- **TypeScript 5.6+** - Type safety throughout

### Styling & UI
- **Tailwind CSS v4** - Utility-first CSS with OKLCH colors
- **shadcn/ui** - Radix UI + Tailwind components
- **Lucide React** - Optimized icon library
- **CSS Variables** - Theme customization support

### State Management
- **TanStack Query v5** - Server state, caching, background refetch
- **Zustand** - Client state for UI and local preferences
- **React Hook Form** - Performant form handling with Zod validation

### Offline-First Architecture
- **PowerSync** - Offline-first sync with Supabase
- **@serwist/next** - Service worker (Workbox successor)
- **IndexedDB** - Local structured data persistence
- **Cache API** - Network resources caching

### Backend & Database
- **Supabase** - Auth, Postgres, real-time, storage
- **Edge Functions** - Serverless APIs on Vercel Edge
- **Row Level Security** - Database-level authorization

### Development Tools
- **pnpm** - Fast, disk-efficient package manager
- **Biome** - Fast linting/formatting (replaces ESLint+Prettier)
- **Vitest** - Unit testing framework
- **Playwright** - E2E testing for multiple browsers

## Available Scripts

```bash
pnpm dev          # Start development server (port 3000)
pnpm build        # Build for production
pnpm start        # Start production server
pnpm lint         # Run Biome linter and auto-fix
pnpm format       # Format code with Biome
pnpm typecheck    # TypeScript type checking
pnpm test         # Run unit tests with Vitest
pnpm test:e2e     # Run E2E tests with Playwright
```

## Project Structure

```
├── app/                    # Next.js App Router
│   ├── dashboard/         # Dashboard page
│   ├── offline/          # Offline fallback page
│   ├── layout.tsx        # Root layout
│   ├── page.tsx          # Home page
│   ├── providers.tsx     # React Query provider
│   ├── sw.ts            # Service worker config
│   └── globals.css      # Global styles
├── components/          # Shared components
│   └── ui/             # shadcn/ui components
├── lib/                # Utilities
│   └── utils.ts       # Helper functions
├── tests/             # Test files
│   └── setup.ts      # Test configuration
├── public/           
│   └── manifest.json # PWA manifest
└── [config files]    # Various configuration files
```

## Environment Variables

Create a `.env.local` file with the following variables:

```env
# Supabase (Required)
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key

# Optional Services
ELEVENLABS_API_KEY=your_api_key            # Text-to-speech
NEXT_PUBLIC_POSTHOG_KEY=your_posthog_key   # Analytics
```

## PWA Configuration

The app is configured as a Progressive Web App with:

- **Service Worker** - Offline support and caching strategies
- **Web Manifest** - Installability on mobile and desktop
- **Responsive Design** - Works on all screen sizes
- **Offline Page** - Fallback when network is unavailable
- **App Shell Architecture** - Fast initial load

### Caching Strategies

```javascript
// API Routes - Network First (3s timeout)
/api/* → NetworkFirst with 5min cache

// Static Assets - Cache First
fonts.googleapis.com → 365 days
images → 30 days cache

// Auth Routes - Network Only
/api/auth/* → No caching
```

## Performance

### Optimizations
- **Server Components** by default
- **Code Splitting** automatic
- **Image Optimization** with Next.js Image
- **Font Optimization** automatic
- **Edge Runtime** support
- **Prefetching** for faster navigation

### Security Headers
```javascript
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=()
```

## Development Guidelines

### Component Patterns
- Use functional components with TypeScript
- Server Components by default
- Client Components with 'use client' directive
- Follow shadcn/ui patterns for UI components

### State Management
- TanStack Query for server data
- Zustand for UI state
- React Hook Form for forms
- Zod for validation schemas

### Code Style
- Biome for linting/formatting
- 2 spaces indentation
- Single quotes for JS
- Double quotes for JSX
- 100 character line width

### Testing
- Unit tests with Vitest
- E2E tests with Playwright
- Test coverage reporting
- Path aliases configured

## Deployment

### Vercel (Recommended)
```bash
# Deploy to Vercel
vercel

# Or connect GitHub repo for auto-deployment
```

### Docker
```dockerfile
# Dockerfile available for containerized deployment
docker build -t pwa-boilerplate .
docker run -p 3000:3000 pwa-boilerplate
```

## Supabase Setup

1. Create a project at [supabase.com](https://supabase.com)
2. Copy your project URL and anon key
3. Add to `.env.local`
4. Run database migrations (if any)
5. Configure Row Level Security policies

## PWA Installation

### Generate Icons
1. Visit [PWA Builder](https://www.pwabuilder.com/imageGenerator)
2. Upload your logo (512x512px recommended)
3. Download generated icon set
4. Replace files in `/public/icons/`

### Test Installation
1. Open app in Chrome/Edge
2. Look for install prompt in address bar
3. Install and test offline functionality
4. Check app in chrome://apps

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Common Tasks

### Add a New Page
```bash
# Create new route
mkdir app/new-page
touch app/new-page/page.tsx
```

### Add UI Component
```bash
# Install shadcn/ui component
pnpm dlx shadcn@latest add button card dialog
```

### Run Tests
```bash
# Run all tests
pnpm test

# Run specific test file
pnpm test path/to/test.spec.ts

# Run with coverage
pnpm test --coverage
```

### Update Dependencies
```bash
# Check outdated packages
pnpm outdated

# Update all dependencies
pnpm update --latest
```

## Troubleshooting

### Service Worker Issues
- Clear browser cache and reload
- Check DevTools > Application > Service Workers
- Ensure `NODE_ENV=production` for testing

### TypeScript Errors
```bash
# Clear TypeScript cache
rm -rf .next
pnpm typecheck
```

### Build Errors
```bash
# Clean build
rm -rf .next node_modules
pnpm install
pnpm build
```

## Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS v4](https://tailwindcss.com)
- [Supabase Docs](https://supabase.com/docs)
- [PowerSync Documentation](https://docs.powersync.com)
- [Serwist Documentation](https://serwist.pages.dev)
- [shadcn/ui Components](https://ui.shadcn.com)

## License

MIT

---

Built with ❤️ using modern web technologies. Ready for production deployment.