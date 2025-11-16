"use client";

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { getToken, setToken, setUser, getUser } from '@/lib/auth';

/**
 * Login page.  Renders a form for entering an email and password.
 * On successful authentication the user is redirected to the chat
 * interface and the token/user details are stored in localStorage.
 */
export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  // If already authenticated, redirect to chat
  useEffect(() => {
    const token = getToken();
    if (token && getUser()) {
      router.replace('/chat');
    }
  }, [router]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const res = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.detail || 'Invalid credentials');
        setLoading(false);
        return;
      }
      setToken(data.access_token);
      setUser(data.user);
      router.push('/chat');
    } catch (err) {
      setError('Login failed');
      setLoading(false);
    }
  };

  return (
    <main className="flex flex-col items-center justify-center min-h-[calc(100vh-3.5rem)] p-4 bg-panel text-gray-100 animate-fadeIn">
      <div className="max-w-sm w-full space-y-6 bg-panelLight border border-border rounded-xl p-6 shadow-lg">
        <h1 className="text-3xl font-bold text-center mb-2">Sign In</h1>
        {error && <p className="text-red-500 text-center text-sm">{error}</p>}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-1">
            <label htmlFor="email" className="block text-sm font-medium">
              Email
            </label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full px-4 py-2 bg-panel border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
            />
          </div>
          <div className="space-y-1">
            <label htmlFor="password" className="block text-sm font-medium">
              Password
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full px-4 py-2 bg-panel border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="w-full py-2 bg-primary rounded-lg hover:bg-primary-dark transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Signing in…' : 'Sign In'}
          </button>
        </form>
        <p className="text-center text-sm text-gray-400">
          Don&apos;t have an account?{' '}
          <Link href="/auth/register" className="text-primary hover:underline">
            Register
          </Link>
        </p>
      </div>
    </main>
  );
}
