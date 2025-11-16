"use client";

import Link from 'next/link';
import { useState, useEffect } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import {
  Menu as MenuIcon,
  X as CloseIcon,
  UserCircle,
  LogIn,
  LogOut,
  UserPlus,
  MessageSquare,
} from 'lucide-react';
import { getToken, getUser, clearToken } from '@/lib/auth';

/**
 * Primary navigation bar for the chat application.  It displays
 * contextual links depending on whether the user is signed in.  On
 * small screens the navigation collapses into a hamburger menu.
 */
export default function NavBar() {
  const router = useRouter();
  const pathname = usePathname();
  const [menuOpen, setMenuOpen] = useState(false);
  const [user, setUserState] = useState<ReturnType<typeof getUser> | null>(null);

  // Refresh user state whenever the pathname changes so that the
  // navigation reflects sign‑in or sign‑out actions.
  useEffect(() => {
    setUserState(getUser());
  }, [pathname]);

  const handleSignOut = () => {
    clearToken();
    setUserState(null);
    setMenuOpen(false);
    router.push('/');
  };

  // Build navigation links based on authentication state.  When
  // unauthenticated we offer sign in and registration; otherwise we
  // offer profile and sign out.
  const navLinks = user
    ? [
      { href: '/chat', label: 'Chat', icon: MessageSquare },
      { href: '/profile', label: user.email, icon: UserCircle },
    ]
    : [
      { href: '/auth/login', label: 'Sign In', icon: LogIn },
      { href: '/auth/register', label: 'Register', icon: UserPlus },
    ];

  return (
    <nav className="bg-panelLight border-b border-border text-gray-100 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-14 items-center">
          {/* Branding */}
          <div className="flex items-center gap-2">
            <Link href="/" className="text-xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-500">
              HorizonChat
            </Link>
          </div>
          {/* Desktop navigation */}
          <div className="hidden md:flex md:items-center md:gap-6">
            {navLinks.map(({ href, label, icon: Icon }) => (
              <Link
                key={href}
                href={href}
                className="flex items-center gap-1 hover:text-primary transition-colors"
                onClick={() => setMenuOpen(false)}
              >
                <Icon size={18} />
                <span>{label}</span>
              </Link>
            ))}
            {user && (
              <button
                onClick={handleSignOut}
                className="flex items-center gap-1 hover:text-primary transition-colors"
              >
                <LogOut size={18} />
                <span>Sign Out</span>
              </button>
            )}
          </div>
          {/* Mobile menu toggle */}
          <div className="md:hidden flex items-center">
            <button
              onClick={() => setMenuOpen(!menuOpen)}
              className="text-gray-400 hover:text-primary focus:outline-none"
              aria-label={menuOpen ? 'Close menu' : 'Open menu'}
            >
              {menuOpen ? <CloseIcon size={24} /> : <MenuIcon size={24} />}
            </button>
          </div>
        </div>
      </div>
      {/* Mobile dropdown menu */}
      {menuOpen && (
        <div className="md:hidden border-t border-border bg-panelLight pb-3 pt-2">
          <div className="space-y-2 px-4">
            {navLinks.map(({ href, label, icon: Icon }) => (
              <Link
                key={href}
                href={href}
                className="flex items-center gap-2 px-2 py-2 rounded-md hover:bg-panel transition-colors"
                onClick={() => setMenuOpen(false)}
              >
                <Icon size={20} />
                <span>{label}</span>
              </Link>
            ))}
            {user && (
              <button
                onClick={handleSignOut}
                className="flex items-center gap-2 w-full px-2 py-2 rounded-md hover:bg-panel transition-colors"
              >
                <LogOut size={20} />
                <span>Sign Out</span>
              </button>
            )}
          </div>
        </div>
      )}
    </nav>
  );
}