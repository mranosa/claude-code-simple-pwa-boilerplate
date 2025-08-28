# PWA Boilerplate

A production-ready Progressive Web Application boilerplate with Next.js 15, TypeScript, Supabase, and Claude Code automation.

## Quick Start

```bash
# Clone the repository
git clone <repo-url>
cd pwa-boilerplate

# Run setup script
bash setup.sh

# Start development
pnpm dev
```

## What You Get

Running `setup.sh` creates a complete PWA with:

### Core Technologies

- **Next.js 15.3+** - React framework with App Router
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS v4** - Utility-first CSS framework
- **Supabase** - Backend as a Service (Auth + Database)
- **PowerSync** - Offline-first data synchronization
- **Serwist** - Next-generation service worker tooling

### State Management & Data Fetching

- **TanStack Query v5** - Server state management
- **Zustand** - Client state management
- **React Hook Form** - Form handling with Zod validation

### Development Tools

- **Biome** - Fast formatter and linter
- **Vitest** - Unit testing framework
- **Playwright** - E2E testing framework
- **pnpm** - Fast, disk-efficient package manager

### Claude Code Integration

The setup includes Claude Code hooks for enhanced development:

- Automated logging and session management
- TTS (Text-to-Speech) announcements
- Safety checks for dangerous commands
- Approved commands configuration
- Custom output styles

### PWA Features

- Service worker with offline support
- App manifest for installability
- Custom install prompt component
- Offline indicator component
- Optimized caching strategies

## Project Structure

After setup, your project will have:

```
├── app/                    # Next.js app directory
│   ├── api/               # API routes
│   ├── (auth)/           # Auth pages
│   ├── _components/      # Route components
│   └── sw.ts            # Service worker
├── components/           # Shared components
├── lib/                 # Utilities
├── public/             # Static assets
├── tests/              # Test files
└── .claude/           # Claude Code config
```

## Environment Configuration

After setup, configure your `.env.local`:

```env
# Supabase (Required)
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key

# Optional services
ELEVENLABS_API_KEY=your_api_key
NEXT_PUBLIC_POSTHOG_KEY=your_posthog_key
```

## Post-Setup Steps

1. **Generate PWA Icons**
   - Visit [PWA Builder](https://www.pwabuilder.com/imageGenerator)
   - Upload your logo
   - Replace placeholder icons in `/public/icons`

2. **Configure Supabase**
   - Create project at [supabase.com](https://supabase.com)
   - Copy credentials to `.env.local`

3. **Install UI Components**
   ```bash
   pnpm dlx shadcn@latest add button card
   ```

4. **Test PWA Installation**
   - Open http://localhost:3000
   - Look for install prompt
   - Test offline functionality

## Available Scripts

```bash
pnpm dev        # Start development server
pnpm build      # Build for production
pnpm start      # Start production server
pnpm lint       # Run linting
pnpm format     # Format code
pnpm test       # Run unit tests
pnpm test:e2e   # Run E2E tests
```

## Tech Stack Details

### Frontend Architecture
- **App Router** for file-based routing
- **Server Components** for better performance
- **Streaming SSR** for faster page loads
- **Parallel Routes** for complex layouts
- **Error Boundaries** for graceful error handling

### Offline-First Architecture
- **PowerSync** for real-time sync
- **Optimistic updates** for instant feedback
- **Conflict resolution** built-in
- **Background sync** when reconnected

### Security
- **Row Level Security** with Supabase
- **JWT authentication** 
- **CSRF protection**
- **Content Security Policy** headers

### Performance
- **Code splitting** automatic
- **Image optimization** built-in
- **Font optimization** automatic
- **Prefetching** for faster navigation
- **Bundle analysis** tools included

## License

MIT