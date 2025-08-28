import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { CheckCircle2, Smartphone, Wifi, Zap } from 'lucide-react'

export default function HomePage() {
  return (
    <main className="min-h-screen gradient-bg">
      <div className="container mx-auto px-4 py-16">
        <div className="flex flex-col items-center text-center space-y-8">
          <div className="space-y-4 max-w-3xl">
            <h1 className="text-4xl font-bold tracking-tighter sm:text-5xl md:text-6xl lg:text-7xl bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600">
              Modern PWA Boilerplate
            </h1>
            <p className="mx-auto max-w-[700px] text-muted-foreground text-lg sm:text-xl">
              Production-ready Progressive Web App with Next.js 15, Supabase, and offline-first
              architecture. Built for speed, reliability, and exceptional user experience.
            </p>
          </div>

          <div className="flex gap-4 flex-wrap justify-center">
            <Button asChild size="lg">
              <Link href="/dashboard">Get Started</Link>
            </Button>
            <Button asChild variant="outline" size="lg">
              <Link href="https://github.com">View Source</Link>
            </Button>
          </div>

          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3 w-full max-w-5xl mt-16">
            <Card className="shadow-lg hover:shadow-xl transition-all hover:scale-105 border bg-white/80 backdrop-blur">
              <CardHeader>
                <Smartphone className="h-10 w-10 mb-2 stroke-primary" />
                <CardTitle>PWA Ready</CardTitle>
                <CardDescription>
                  Installable app with service worker, offline support, and push notifications
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm text-muted-foreground">
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="h-4 w-4 stroke-green-500" />
                    100 Lighthouse Score
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="h-4 w-4 stroke-green-500" />
                    App manifest configured
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="h-4 w-4 stroke-green-500" />
                    Service worker caching
                  </li>
                </ul>
              </CardContent>
            </Card>

            <Card className="shadow-lg hover:shadow-xl transition-all hover:scale-105 border bg-white/80 backdrop-blur">
              <CardHeader>
                <Wifi className="h-10 w-10 mb-2 stroke-primary" />
                <CardTitle>Offline First</CardTitle>
                <CardDescription>
                  PowerSync + Supabase for seamless offline/online data synchronization
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm text-muted-foreground">
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="h-4 w-4 stroke-green-500" />
                    Local-first database
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="h-4 w-4 stroke-green-500" />
                    Automatic conflict resolution
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="h-4 w-4 stroke-green-500" />
                    Real-time sync
                  </li>
                </ul>
              </CardContent>
            </Card>

            <Card className="shadow-lg hover:shadow-xl transition-all hover:scale-105 border bg-white/80 backdrop-blur">
              <CardHeader>
                <Zap className="h-10 w-10 mb-2 stroke-primary" />
                <CardTitle>Performance</CardTitle>
                <CardDescription>
                  Optimized for Core Web Vitals with edge runtime and modern best practices
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm text-muted-foreground">
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="h-4 w-4 stroke-green-500" />
                    Server Components
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="h-4 w-4 stroke-green-500" />
                    Edge Functions
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="h-4 w-4 stroke-green-500" />
                    Optimistic updates
                  </li>
                </ul>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </main>
  )
}