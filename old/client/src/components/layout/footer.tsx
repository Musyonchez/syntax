"use client";

import Link from "next/link";
import Image from "next/image";
import { motion } from "framer-motion";
import { Heart, Github, Twitter, Mail } from "lucide-react";

const footerLinks = {
  Product: [
    { label: "Practice", href: "/practice", external: false },
    { label: "Leaderboard", href: "/leaderboard", external: false },
    { label: "Forum", href: "/forum", external: false },
    { label: "Snippets", href: "/snippets", external: false },
  ],
  Community: [
    { label: "GitHub", href: "https://github.com/syntaxmem", external: true },
    { label: "Discord", href: "#", external: true },
    { label: "Twitter", href: "#", external: true },
    { label: "Blog", href: "/blog", external: false },
  ],
  Support: [
    { label: "Documentation", href: "/docs", external: false },
    { label: "Help Center", href: "/help", external: false },
    { label: "Contact", href: "/contact", external: false },
    { label: "Bug Reports", href: "/bugs", external: false },
  ],
  Legal: [
    { label: "Privacy Policy", href: "/privacy", external: false },
    { label: "Terms of Service", href: "/terms", external: false },
    { label: "Cookie Policy", href: "/cookies", external: false },
  ],
};

const socialLinks = [
  { icon: Github, href: "https://github.com/syntaxmem", label: "GitHub" },
  { icon: Twitter, href: "#", label: "Twitter" },
  { icon: Mail, href: "mailto:hello@syntaxmem.dev", label: "Email" },
];

export function Footer() {
  return (
    <footer className="border-t bg-background w-full flex justify-center">
      <div className="container py-12 px-4">
        {/* Brand Section - Full width on sm-lg */}
        <div className="mb-8 text-center lg:hidden">
          <Link href="/" className="inline-flex items-center justify-center">
            <Image
              src="/logo2.png"
              alt="SyntaxMem Logo"
              width={180}
              height={40}
              className="h-10"
            />
          </Link>
          <p className="mt-4 text-sm text-muted-foreground max-w-md mx-auto">
            Master programming through interactive code completion challenges.
            Practice, compete, and improve your coding skills.
          </p>
          <div className="mt-6 flex space-x-4 justify-center">
            {socialLinks.map((social) => {
              const Icon = social.icon;
              return (
                <motion.a
                  key={social.label}
                  href={social.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                  className="flex h-9 w-9 items-center justify-center rounded-md border border-input bg-background hover:bg-accent hover:text-accent-foreground"
                >
                  <Icon className="h-4 w-4" />
                  <span className="sr-only">{social.label}</span>
                </motion.a>
              );
            })}
          </div>
        </div>

        <div className="grid gap-8 grid-cols-2 lg:grid-cols-5">
          {/* Brand Column - Only visible on lg+ */}
          <div className="hidden lg:block lg:col-span-1">
            <Link href="/" className="flex items-center">
              <Image
                src="/logo2.png"
                alt="SyntaxMem Logo"
                width={120}
                height={40}
                className="h-10"
              />
            </Link>
            <p className="mt-4 text-sm text-muted-foreground">
              Master programming through interactive code completion challenges.
              Practice, compete, and improve your coding skills.
            </p>
            <div className="mt-6 flex space-x-4">
              {socialLinks.map((social) => {
                const Icon = social.icon;
                return (
                  <motion.a
                    key={social.label}
                    href={social.href}
                    target="_blank"
                    rel="noopener noreferrer"
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.9 }}
                    className="flex h-9 w-9 items-center justify-center rounded-md border border-input bg-background hover:bg-accent hover:text-accent-foreground"
                  >
                    <Icon className="h-4 w-4" />
                    <span className="sr-only">{social.label}</span>
                  </motion.a>
                );
              })}
            </div>
          </div>

          {/* Link Columns */}
          {Object.entries(footerLinks).map(([category, links]) => (
            <div key={category}>
              <h3 className="text-sm font-semibold">{category}</h3>
              <ul className="mt-4 space-y-3">
                {links.map((link) => (
                  <li key={link.label}>
                    <Link
                      href={link.href}
                      target={link.external ? "_blank" : undefined}
                      rel={link.external ? "noopener noreferrer" : undefined}
                      className="text-sm text-muted-foreground hover:text-foreground transition-colors"
                    >
                      {link.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        {/* Bottom Section */}
        <div className="mt-12 flex flex-col items-center justify-between border-t pt-8 md:flex-row">
          <p className="text-sm text-muted-foreground">
            © {new Date().getFullYear()} SyntaxMem. All rights reserved.
          </p>
          <div className="mt-4 flex items-center space-x-1 text-sm text-muted-foreground md:mt-0">
            <span>Made with</span>
            <motion.div
              animate={{ scale: [1, 1.2, 1] }}
              transition={{ repeat: Infinity, duration: 2 }}
            >
              <Heart className="h-4 w-4 text-red-500" />
            </motion.div>
            <span>by developers, for developers</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
