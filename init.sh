#!/bin/bash

# PWA Boilerplate Initialization Script
# Based on TECHSTACK.md configuration

set -e

echo "🚀 Initializing PWA Boilerplate..."

# Check if pnpm is installed
if ! command -v pnpm &> /dev/null; then
    echo "📦 Installing pnpm..."
    npm install -g pnpm
fi

# Save existing files
echo "💾 Preserving existing configuration files..."
mkdir -p .temp-backup
cp -r .claude .temp-backup/ 2>/dev/null || true
cp TECHSTACK.md .temp-backup/ 2>/dev/null || true
cp CLAUDE.md .temp-backup/ 2>/dev/null || true
cp .env .temp-backup/ 2>/dev/null || true
cp .env.example .temp-backup/ 2>/dev/null || true
cp -r logs .temp-backup/ 2>/dev/null || true

# Initialize Next.js project in current directory
echo "⚡ Creating Next.js app with TypeScript and App Router..."
pnpm create next-app . --typescript --app --tailwind --no-git --import-alias "@/*" <<EOF
y
EOF

# Restore preserved files
echo "♻️ Restoring configuration files..."
cp -r .temp-backup/.claude . 2>/dev/null || true
cp .temp-backup/TECHSTACK.md . 2>/dev/null || true
cp .temp-backup/CLAUDE.md . 2>/dev/null || true
cp .temp-backup/.env . 2>/dev/null || true
cp .temp-backup/.env.example . 2>/dev/null || true
cp -r .temp-backup/logs . 2>/dev/null || true
rm -rf .temp-backup

# Install core dependencies
echo "📦 Installing core dependencies..."
pnpm add \
  @supabase/supabase-js@latest \
  @supabase/ssr@latest \
  @tanstack/react-query@^5.0.0 \
  zustand@latest \
  react-hook-form@latest \
  zod@latest \
  @hookform/resolvers@latest \
  lucide-react@latest \
  @serwist/next@latest \
  @serwist/precaching@latest \
  @serwist/sw@latest \
  @serwist/strategies@latest \
  @serwist/expiration@latest \
  @serwist/routing@latest \
  @powersync/react@latest \
  clsx@latest \
  tailwind-merge@latest \
  class-variance-authority@latest

# Install dev dependencies
echo "🔧 Installing dev dependencies..."
pnpm add -D \
  @types/react@latest \
  @types/node@latest \
  @types/serviceworker@latest \
  @tailwindcss/postcss@latest \
  vitest@latest \
  @vitejs/plugin-react@latest \
  @playwright/test@latest \
  @testing-library/react@latest \
  @testing-library/jest-dom@latest \
  jsdom@latest \
  @biomejs/biome@latest \
  husky@latest \
  lint-staged@latest \
  @tanstack/react-query-devtools@latest

# Create project structure
echo "📁 Creating project structure..."
mkdir -p app/api
mkdir -p app/\(auth\)
mkdir -p app/_components
mkdir -p components/ui
mkdir -p lib/supabase
mkdir -p lib/powersync
mkdir -p lib/validations
mkdir -p hooks
mkdir -p public/icons
mkdir -p tests/unit
mkdir -p tests/e2e

# Create manifest.json
echo "📱 Creating PWA manifest..."
cat > public/manifest.json << 'EOF'
{
  "name": "PWA App",
  "short_name": "PWA",
  "description": "Progressive Web Application",
  "theme_color": "#0a0a0a",
  "background_color": "#0a0a0a",
  "display": "standalone",
  "orientation": "portrait",
  "scope": "/",
  "start_url": "/",
  "icons": [
    {
      "src": "/icons/icon-72x72.png",
      "sizes": "72x72",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-96x96.png",
      "sizes": "96x96",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-128x128.png",
      "sizes": "128x128",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-144x144.png",
      "sizes": "144x144",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-152x152.png",
      "sizes": "152x152",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "/icons/icon-384x384.png",
      "sizes": "384x384",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-512x512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "maskable"
    }
  ]
}
EOF

# Create next.config.js for PWA
echo "⚙️ Configuring Next.js for PWA..."
cat > next.config.mjs << 'EOF'
import withSerwistInit from "@serwist/next";

const withSerwist = withSerwistInit({
  swSrc: "app/sw.ts",
  swDest: "public/sw.js",
});

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    domains: ["localhost"],
  },
};

export default withSerwist(nextConfig);
EOF

# Create service worker
echo "🔧 Creating service worker..."
cat > app/sw.ts << 'EOF'
/// <reference lib="webworker" />
import type { PrecacheEntry } from "@serwist/precaching";
import { installSerwist } from "@serwist/sw";
import { NetworkFirst, StaleWhileRevalidate, CacheFirst } from "@serwist/strategies";
import { ExpirationPlugin } from "@serwist/expiration";
import { registerRoute } from "@serwist/routing";

declare const self: ServiceWorkerGlobalScope & {
  __SW_MANIFEST: (PrecacheEntry | string)[] | undefined;
};

// Precache all static assets
installSerwist({
  precacheEntries: self.__SW_MANIFEST,
  skipWaiting: true,
  clientsClaim: true,
  navigationPreload: true,
  runtimeCaching: [],
});

// Cache page navigations (html) with network-first strategy
registerRoute(
  ({ request }) => request.mode === "navigate",
  new NetworkFirst({
    cacheName: "pages",
    plugins: [
      new ExpirationPlugin({
        maxEntries: 10,
        maxAgeSeconds: 60 * 60 * 24 * 30, // 30 days
      }),
    ],
  })
);

// Cache JS and CSS with stale-while-revalidate
registerRoute(
  ({ request }) =>
    request.destination === "script" ||
    request.destination === "style",
  new StaleWhileRevalidate({
    cacheName: "static-resources",
    plugins: [
      new ExpirationPlugin({
        maxEntries: 60,
        maxAgeSeconds: 60 * 60 * 24 * 30, // 30 days
      }),
    ],
  })
);

// Cache images with cache-first
registerRoute(
  ({ request }) => request.destination === "image",
  new CacheFirst({
    cacheName: "images",
    plugins: [
      new ExpirationPlugin({
        maxEntries: 100,
        maxAgeSeconds: 60 * 60 * 24 * 30, // 30 days
      }),
    ],
  })
);
EOF

# Create Supabase client
echo "🗄️ Setting up Supabase client..."
cat > lib/supabase/client.ts << 'EOF'
import { createBrowserClient } from "@supabase/ssr";

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  );
}
EOF

cat > lib/supabase/server.ts << 'EOF'
import { createServerClient, type CookieOptions } from "@supabase/ssr";
import { cookies } from "next/headers";

export async function createClient() {
  const cookieStore = await cookies();

  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll();
        },
        setAll(cookiesToSet) {
          try {
            cookiesToSet.forEach(({ name, value, options }) =>
              cookieStore.set(name, value, options)
            );
          } catch {
            // Server Component, ignore
          }
        },
      },
    }
  );
}
EOF

# Create TanStack Query provider
echo "📊 Setting up TanStack Query..."
cat > app/providers.tsx << 'EOF'
"use client";

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import { useState } from "react";

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: 60 * 1000,
            gcTime: 5 * 60 * 1000,
          },
        },
      })
  );

  return (
    <QueryClientProvider client={queryClient}>
      {children}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}
EOF

# Update layout.tsx
echo "🎨 Updating layout with providers..."
cat > app/layout.tsx << 'EOF'
import type { Metadata, Viewport } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Providers } from "./providers";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "PWA App",
  description: "Progressive Web Application",
  manifest: "/manifest.json",
};

export const viewport: Viewport = {
  themeColor: "#0a0a0a",
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <link rel="manifest" href="/manifest.json" />
        <link rel="apple-touch-icon" href="/icons/icon-192x192.png" />
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-status-bar-style" content="default" />
        <meta name="apple-mobile-web-app-title" content="PWA App" />
      </head>
      <body className={inter.className}>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
EOF

# Create PWA install prompt component
echo "💾 Creating PWA install component..."
cat > components/pwa-install.tsx << 'EOF'
"use client";

import { useEffect, useState } from "react";
import { Download } from "lucide-react";

export function PWAInstall() {
  const [deferredPrompt, setDeferredPrompt] = useState<any>(null);
  const [showInstall, setShowInstall] = useState(false);

  useEffect(() => {
    const handleBeforeInstallPrompt = (e: Event) => {
      e.preventDefault();
      setDeferredPrompt(e);
      setShowInstall(true);
    };

    window.addEventListener("beforeinstallprompt", handleBeforeInstallPrompt);

    return () => {
      window.removeEventListener("beforeinstallprompt", handleBeforeInstallPrompt);
    };
  }, []);

  const handleInstall = async () => {
    if (!deferredPrompt) return;

    deferredPrompt.prompt();
    const { outcome } = await deferredPrompt.userChoice;
    
    if (outcome === "accepted") {
      setShowInstall(false);
    }
    setDeferredPrompt(null);
  };

  if (!showInstall) return null;

  return (
    <button
      onClick={handleInstall}
      className="fixed bottom-4 right-4 flex items-center gap-2 rounded-lg bg-blue-600 px-4 py-2 text-white shadow-lg hover:bg-blue-700 transition-colors"
    >
      <Download className="h-5 w-5" />
      Install App
    </button>
  );
}
EOF

# Create offline indicator
echo "🔌 Creating offline indicator..."
cat > components/offline-indicator.tsx << 'EOF'
"use client";

import { useEffect, useState } from "react";
import { WifiOff } from "lucide-react";

export function OfflineIndicator() {
  const [isOffline, setIsOffline] = useState(false);

  useEffect(() => {
    setIsOffline(!navigator.onLine);

    const handleOnline = () => setIsOffline(false);
    const handleOffline = () => setIsOffline(true);

    window.addEventListener("online", handleOnline);
    window.addEventListener("offline", handleOffline);

    return () => {
      window.removeEventListener("online", handleOnline);
      window.removeEventListener("offline", handleOffline);
    };
  }, []);

  if (!isOffline) return null;

  return (
    <div className="fixed top-0 left-0 right-0 bg-orange-500 text-white py-2 px-4 text-center flex items-center justify-center gap-2">
      <WifiOff className="h-4 w-4" />
      <span>You are offline - Some features may be limited</span>
    </div>
  );
}
EOF

# Create environment files
echo "🔐 Creating environment files..."
cat > .env.sample << 'EOF'
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
EOF

# Create lib/utils.ts for cn helper
echo "🛠️ Creating utility functions..."
cat > lib/utils.ts << 'EOF'
import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
EOF

# Setup shadcn/ui
echo "🎨 Initializing shadcn/ui..."
cat > components.json << 'EOF'
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "new-york",
  "rsc": true,
  "tsx": true,
  "tailwind": {
    "config": "tailwind.config.ts",
    "css": "app/globals.css",
    "baseColor": "zinc",
    "cssVariables": true
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils"
  }
}
EOF

# Configure Vitest
echo "🧪 Setting up Vitest..."
cat > vitest.config.ts << 'EOF'
import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
  plugins: [react()],
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: "./tests/setup.ts",
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./"),
    },
  },
});
EOF

cat > tests/setup.ts << 'EOF'
import "@testing-library/jest-dom";
EOF

# Configure Playwright
echo "🎭 Setting up Playwright..."
cat > playwright.config.ts << 'EOF'
import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./tests/e2e",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: "html",
  use: {
    baseURL: "http://localhost:3000",
    trace: "on-first-retry",
  },
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
  ],
  webServer: {
    command: "pnpm dev",
    url: "http://localhost:3000",
    reuseExistingServer: !process.env.CI,
  },
});
EOF

# Configure Biome
echo "🎨 Setting up Biome..."
cat > biome.json << 'EOF'
{
  "$schema": "https://biomejs.dev/schemas/1.9.4/schema.json",
  "organizeImports": {
    "enabled": true
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true
    }
  },
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100
  },
  "files": {
    "ignore": [
      "node_modules",
      ".next",
      "out",
      "public",
      ".cache",
      "dist",
      "coverage"
    ]
  }
}
EOF

# Setup Husky
echo "🐺 Setting up Git hooks..."
pnpm exec husky init

cat > .husky/pre-commit << 'EOF'
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

pnpm lint-staged
EOF

chmod +x .husky/pre-commit

# Configure lint-staged
cat > .lintstagedrc.json << 'EOF'
{
  "*.{js,jsx,ts,tsx}": ["pnpm biome check --write"],
  "*.{json,md,mdx,css,yml,yaml}": ["pnpm biome format --write"]
}
EOF

# Update package.json scripts
echo "📝 Updating package.json scripts..."
node -e "
const fs = require('fs');
const packageJson = JSON.parse(fs.readFileSync('package.json', 'utf8'));

packageJson.scripts = {
  ...packageJson.scripts,
  'dev': 'next dev',
  'build': 'next build',
  'start': 'next start',
  'lint': 'biome check .',
  'format': 'biome format --write .',
  'test': 'vitest',
  'test:ui': 'vitest --ui',
  'test:e2e': 'playwright test',
  'test:e2e:ui': 'playwright test --ui',
  'prepare': 'husky'
};

fs.writeFileSync('package.json', JSON.stringify(packageJson, null, 2));
"

# Fix PostCSS configuration for Tailwind CSS v4
echo "🔧 Updating PostCSS configuration..."
cat > postcss.config.js << 'EOF'
module.exports = {
  plugins: {
    '@tailwindcss/postcss': {},
    autoprefixer: {},
  },
};
EOF

# Generate basic PWA icons (placeholder)
echo "🎨 Creating placeholder icons..."
for size in 72 96 128 144 152 192 384 512; do
  cat > public/icons/icon-${size}x${size}.png << EOF
# Placeholder for ${size}x${size} icon
# Replace with actual PWA icons
EOF
done

echo "✅ PWA Boilerplate initialization complete!"
echo ""
echo "📋 Next steps:"
echo "1. Replace placeholder icons in /public/icons with actual PWA icons"
echo "2. Configure environment variables in .env.local (copy from .env.sample)"
echo "3. Run 'pnpm dev' to start the development server"
echo "4. Initialize shadcn/ui components: 'pnpm dlx shadcn@latest add button'"
echo ""
echo "🚀 Happy coding!"