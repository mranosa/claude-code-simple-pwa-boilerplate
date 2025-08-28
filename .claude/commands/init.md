# Initialize PWA boilerplate artifacts

Scaffolds a production-ready PWA with Next.js 15, TypeScript, Supabase, and offline-first capabilities.

## What it does:

1. Creates a Next.js 15.3+ app with TypeScript and App Router
2. Installs all dependencies (TanStack Query, Zustand, Supabase, etc.)
3. Sets up PWA configuration with manifest and service worker
4. Configures testing with Vitest and Playwright
5. Sets up Tailwind CSS v4 and shadcn/ui
6. Creates initial project structure and components
7. Configures development tools (Biome, Husky)

## Usage:

Simply run: `/init`

## Implementation:

When this command is called, execute the init.sh script:

```bash
bash ./init.sh
```

## Requirements:

- Node.js 18+ installed
- Git repository initialized
- Internet connection for package installation

## Post-initialization:

After running /init, you need to:
1. Replace placeholder icons in /public/icons
2. Configure environment variables in .env.local
3. Run `pnpm dev` to start development