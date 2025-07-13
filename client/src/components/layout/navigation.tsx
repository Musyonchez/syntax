"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { useState } from "react";
import {
  Moon,
  Sun,
  Code,
  Trophy,
  MessageCircle,
  BookOpen,
  User,
  LogOut,
  Menu,
  X,
} from "lucide-react";
import { useTheme } from "next-themes";
import { useSession, signOut } from "next-auth/react";

import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";

const navItems = [
  { href: "/practice", label: "Practice", icon: Code },
  { href: "/leaderboard", label: "Leaderboard", icon: Trophy },
  { href: "/forum", label: "Forum", icon: MessageCircle },
  { href: "/snippets", label: "Snippets", icon: BookOpen },
];

export function Navigation() {
  const pathname = usePathname();
  const { theme, setTheme } = useTheme();
  const { data: session } = useSession();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const toggleTheme = () => {
    setTheme(theme === "dark" ? "light" : "dark");
  };

  const closeMobileMenu = () => {
    setIsMobileMenuOpen(false);
  };

  return (
    <motion.header
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 flex justify-center"
    >
      <div className="container flex h-16 items-center justify-between px-4">
        {/* Logo */}
        <Link href="/" className="flex items-center space-x-2">
          <motion.div
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="flex items-center space-x-2"
          >
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary">
              <Code className="h-5 w-5 text-primary-foreground" />
            </div>
            <span className="text-xl font-bold">SyntaxMem</span>
          </motion.div>
        </Link>

        {/* Navigation Menu */}
        <nav className="hidden md:flex items-center space-x-6">
          {navItems.map((item) => {
            const isActive = pathname.startsWith(item.href);
            const Icon = item.icon;

            return (
              <Link key={item.href} href={item.href}>
                <motion.div
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className={`relative flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    isActive
                      ? "text-primary bg-primary/10"
                      : "text-muted-foreground hover:text-foreground hover:bg-muted"
                  }`}
                >
                  <Icon className="h-4 w-4" />
                  <span>{item.label}</span>
                  {isActive && (
                    <motion.div
                      layoutId="activeTab"
                      className="absolute inset-0 bg-primary/5 rounded-md"
                      initial={false}
                      transition={{
                        type: "spring",
                        stiffness: 500,
                        damping: 30,
                      }}
                    />
                  )}
                </motion.div>
              </Link>
            );
          })}
        </nav>

        {/* Right Side Actions */}
        <div className="flex items-center space-x-4">
          {/* Theme Toggle - Hidden on mobile, visible on desktop */}
          <Button
            variant="ghost"
            size="icon"
            onClick={toggleTheme}
            className="hidden md:flex h-9 w-9"
          >
            <motion.div
              key={theme}
              initial={{ scale: 0, rotate: -180 }}
              animate={{ scale: 1, rotate: 0 }}
              exit={{ scale: 0, rotate: 180 }}
              transition={{ duration: 0.2 }}
            >
              {theme === "dark" ? (
                <Sun className="h-4 w-4" />
              ) : (
                <Moon className="h-4 w-4" />
              )}
            </motion.div>
            <span className="sr-only">Toggle theme</span>
          </Button>

          {/* User Menu - Hidden on mobile, visible on desktop */}
          {session?.user ? (
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button
                  variant="ghost"
                  className="hidden md:flex relative h-9 w-9 rounded-full"
                >
                  <Avatar className="h-8 w-8">
                    <AvatarImage
                      src={session.user.image || ""}
                      alt={session.user.name || ""}
                    />
                    <AvatarFallback>
                      {session.user.name?.charAt(0).toUpperCase()}
                    </AvatarFallback>
                  </Avatar>
                  {session.user.role === "admin" && (
                    <Badge className="absolute -top-1 -right-1 h-4 w-4 p-0 text-xs">
                      A
                    </Badge>
                  )}
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent className="w-56" align="end" forceMount>
                <DropdownMenuLabel className="font-normal">
                  <div className="flex flex-col space-y-1">
                    <p className="text-sm font-medium leading-none">
                      {session.user.name}
                    </p>
                    <p className="text-xs leading-none text-muted-foreground">
                      {session.user.email}
                    </p>
                  </div>
                </DropdownMenuLabel>
                <DropdownMenuSeparator />
                <DropdownMenuItem asChild>
                  <Link href="/dashboard" className="cursor-pointer">
                    <User className="mr-2 h-4 w-4" />
                    Dashboard
                  </Link>
                </DropdownMenuItem>
                {session.user.role === "admin" && (
                  <DropdownMenuItem asChild>
                    <Link href="/admin" className="cursor-pointer">
                      <Code className="mr-2 h-4 w-4" />
                      Admin Panel
                    </Link>
                  </DropdownMenuItem>
                )}
                <DropdownMenuSeparator />
                <DropdownMenuItem
                  className="cursor-pointer"
                  onClick={() => signOut()}
                >
                  <LogOut className="mr-2 h-4 w-4" />
                  Sign Out
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          ) : (
            <Link href="/auth/signin" className="hidden md:block">
              <Button variant="default" size="sm">
                Sign In
              </Button>
            </Link>
          )}

          {/* Mobile Menu Button - Only visible on mobile */}
          <Button
            variant="ghost"
            size="icon"
            className="md:hidden h-9 w-9"
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            aria-label="Toggle mobile menu"
          >
            <motion.div
              animate={{ rotate: isMobileMenuOpen ? 180 : 0 }}
              transition={{ duration: 0.2 }}
            >
              {isMobileMenuOpen ? (
                <X className="h-5 w-5" />
              ) : (
                <Menu className="h-5 w-5" />
              )}
            </motion.div>
          </Button>
        </div>
      </div>

      {/* Mobile Menu Overlay */}
      <AnimatePresence>
        {isMobileMenuOpen && (
          <>
            {/* Backdrop */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.2 }}
              className="fixed inset-0 z-50 bg-black/30 backdrop-blur-sm md:hidden"
              onClick={closeMobileMenu}
            />

            {/* Mobile Menu Panel */}
            <motion.div
              initial={{ x: "100%" }}
              animate={{ x: 0 }}
              exit={{ x: "100%" }}
              transition={{ type: "spring", damping: 30, stiffness: 300 }}
              className="fixed right-0 top-0 z-50 h-full w-[280px] border-l bg-background shadow-2xl md:hidden"
            >
              {/* Mobile Menu Header */}
              <div className="flex items-center justify-between border-b px-6 py-4">
                <div className="flex items-center space-x-2">
                  <div className="flex h-6 w-6 items-center justify-center rounded-md bg-primary">
                    <Code className="h-4 w-4 text-primary-foreground" />
                  </div>
                  <span className="text-lg font-semibold">SyntaxMem</span>
                </div>
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={closeMobileMenu}
                  className="h-8 w-8"
                >
                  <X className="h-4 w-4" />
                </Button>
              </div>

              {/* Mobile Menu Content */}
              <div className="flex flex-col px-6 py-6 bg-background">
                {/* Navigation Links */}
                <nav className="space-y-2">
                  {navItems.map((item, index) => {
                    const isActive = pathname.startsWith(item.href);
                    const Icon = item.icon;

                    return (
                      <motion.div
                        key={item.href}
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.1 }}
                      >
                        <Link
                          href={item.href}
                          onClick={closeMobileMenu}
                          className={`flex items-center space-x-3 rounded-lg px-3 py-3 text-sm font-medium transition-colors ${
                            isActive
                              ? "bg-primary/10 text-primary"
                              : "text-muted-foreground hover:bg-muted hover:text-foreground"
                          }`}
                        >
                          <Icon className="h-5 w-5" />
                          <span>{item.label}</span>
                        </Link>
                      </motion.div>
                    );
                  })}
                </nav>

                {/* Divider */}
                <div className="my-6 border-t" />

                {/* Theme Toggle */}
                <motion.div
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.5 }}
                >
                  <Button
                    variant="ghost"
                    onClick={toggleTheme}
                    className="w-full justify-start space-x-3 px-3 py-3 h-auto mb-2"
                  >
                    {theme === "dark" ? (
                      <Sun className="h-5 w-5" />
                    ) : (
                      <Moon className="h-5 w-5" />
                    )}
                    <span>{theme === "dark" ? "Light Mode" : "Dark Mode"}</span>
                  </Button>
                </motion.div>

                {/* User Section */}
                {session?.user ? (
                  <motion.div
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.6 }}
                    className="space-y-2"
                  >
                    {/* User Info */}
                    <div className="flex items-center space-x-3 rounded-lg bg-muted px-3 py-3">
                      <Avatar className="h-8 w-8">
                        <AvatarImage
                          src={session.user.image || ""}
                          alt={session.user.name || ""}
                        />
                        <AvatarFallback className="text-xs">
                          {session.user.name?.charAt(0).toUpperCase()}
                        </AvatarFallback>
                      </Avatar>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center space-x-1">
                          <p className="text-sm font-medium truncate">
                            {session.user.name}
                          </p>
                          {session.user.role === "admin" && (
                            <Badge className="h-4 px-1 text-xs">A</Badge>
                          )}
                        </div>
                        <p className="text-xs text-muted-foreground truncate">
                          {session.user.email}
                        </p>
                      </div>
                    </div>

                    {/* User Actions */}
                    <Link
                      href="/dashboard"
                      onClick={closeMobileMenu}
                      className="flex items-center space-x-3 rounded-lg px-3 py-3 text-sm font-medium text-muted-foreground hover:bg-muted hover:text-foreground transition-colors"
                    >
                      <User className="h-5 w-5" />
                      <span>Dashboard</span>
                    </Link>

                    {session.user.role === "admin" && (
                      <Link
                        href="/admin"
                        onClick={closeMobileMenu}
                        className="flex items-center space-x-3 rounded-lg px-3 py-3 text-sm font-medium text-muted-foreground hover:bg-muted hover:text-foreground transition-colors"
                      >
                        <Code className="h-5 w-5" />
                        <span>Admin Panel</span>
                      </Link>
                    )}

                    <Button
                      variant="ghost"
                      onClick={() => {
                        signOut();
                        closeMobileMenu();
                      }}
                      className="w-full justify-start space-x-3 px-3 py-3 h-auto text-muted-foreground hover:text-foreground"
                    >
                      <LogOut className="h-5 w-5" />
                      <span>Sign Out</span>
                    </Button>
                  </motion.div>
                ) : (
                  <motion.div
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.6 }}
                  >
                    <Link href="/auth/signin" onClick={closeMobileMenu}>
                      <Button className="w-full">Sign In</Button>
                    </Link>
                  </motion.div>
                )}
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </motion.header>
  );
}
