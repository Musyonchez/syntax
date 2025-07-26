import type { Metadata } from "next"
import { Inter, JetBrains_Mono } from "next/font/google"
import "./globals.css"

import { ThemeProvider } from "@/components/providers/theme-provider"
import { QueryProvider } from "@/components/providers/query-provider"
import { AuthProvider } from "@/components/providers/auth-provider"
import { Navigation } from "@/components/layout/navigation"
import { Footer } from "@/components/layout/footer"
import { Toaster } from "@/components/ui/sonner"

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-sans",
})

const jetbrainsMono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-mono",
})

export const metadata: Metadata = {
  title: {
    default: "SyntaxMem - Master Programming Through Practice",
    template: "%s | SyntaxMem",
  },
  description: "Interactive coding practice platform where you complete masked code snippets to improve your programming skills. Practice Python, JavaScript, and more!",
  keywords: ["coding", "programming", "practice", "learning", "python", "javascript", "algorithms", "software development"],
  authors: [{ name: "SyntaxMem Team" }],
  creator: "SyntaxMem",
  openGraph: {
    type: "website",
    locale: "en_US",
    url: "https://syntaxmem.dev",
    title: "SyntaxMem - Master Programming Through Practice",
    description: "Interactive coding practice platform where you complete masked code snippets to improve your programming skills.",
    siteName: "SyntaxMem",
    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "SyntaxMem - Master Programming Through Practice",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "SyntaxMem - Master Programming Through Practice",
    description: "Interactive coding practice platform where you complete masked code snippets to improve your programming skills.",
    images: ["/og-image.png"],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className={`${inter.variable} ${jetbrainsMono.variable} font-sans antialiased`}
      >
        <ThemeProvider>
          <QueryProvider>
            <AuthProvider>
              <div className="relative flex min-h-screen flex-col">
                <Navigation />
                <main className="flex-1">{children}</main>
                <Footer />
              </div>
              <Toaster richColors />
            </AuthProvider>
          </QueryProvider>
        </ThemeProvider>
      </body>
    </html>
  )
}
