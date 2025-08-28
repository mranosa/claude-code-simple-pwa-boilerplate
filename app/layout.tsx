import type { Metadata, Viewport } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { Providers } from './providers'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'PWA Boilerplate',
  description: 'A modern PWA boilerplate with Next.js and Supabase',
  manifest: '/manifest.json',
  appleWebApp: {
    capable: true,
    statusBarStyle: 'default',
    title: 'PWA Boilerplate',
  },
  formatDetection: {
    telephone: false,
  },
  openGraph: {
    title: 'PWA Boilerplate',
    description: 'A modern PWA boilerplate with Next.js and Supabase',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'PWA Boilerplate',
    description: 'A modern PWA boilerplate with Next.js and Supabase',
  },
}

export const viewport: Viewport = {
  themeColor: [
    { media: '(prefers-color-scheme: light)', color: '#fafafa' },
    { media: '(prefers-color-scheme: dark)', color: '#0a0a0a' },
  ],
  width: 'device-width',
  initialScale: 1,
  maximumScale: 5,
  userScalable: true,
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head />
      <body className={inter.className}>
        <Providers>{children}</Providers>
      </body>
    </html>
  )
}
