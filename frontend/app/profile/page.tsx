"use client";

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { getToken, getUser, clearToken, setUser } from '@/lib/auth';

/**
 * Profile page.  Displays the currently authenticated user's
 * information and allows updating the email or password.  If no
 * user is signed in the client is redirected to the login page.
 */
export default function ProfilePage() {
  const router = useRouter();
  const [user, setUserState] = useState(getUser());
  const [email, setEmail] = useState(user?.email ?? '');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  // Redirect unauthenticated users to the login page
  useEffect(() => {
    const token = getToken();
    if (!token || !user) {
      router.replace('/auth/login');
    }
  }, [router, user]);

  // Refresh user state by calling the backend to retrieve the latest
  // profile information.  This ensures that updates are reflected
  // after page reload.
  useEffect(() => {
    const fetchUser = async () => {
      const token = getToken();
      if (!token) return;
      try {
        const res = await fetch('/api/auth/me', {
          headers: { Authorization: `Bearer ${token}` },
        });
        const data = await res.json();
        if (res.ok) {
          setUserState(data);
          setUser(data);
          setEmail(data.email);
        }
      } catch {
        // ignore errors silently
      }
    };
    fetchUser().catch(() => {});
  }, []);

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    setMessage(null);
    setError(null);
    if (!user) return;
    setLoading(true);
    const token = getToken();
    if (!token) {
      router.replace('/auth/login');
      return;
    }
    try {
      const res = await fetch('/api/auth/update', {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ user_id: user.id, email, password: password || undefined }),
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.detail || 'Update failed');
        setLoading(false);
        return;
      }
      setUserState(data);
      setUser(data);
      setMessage('Profile updated successfully');
      setPassword('');
      setLoading(false);
    } catch (err) {
      setError('Update failed');
      setLoading(false);
    }
  };

  const handleSignOut = () => {
    clearToken();
    setUserState(null);
    router.push('/');
  };

  if (!user) {
    return null;
  }
  return (
    <main className="flex flex-col items-center justify-center min-h-[calc(100vh-3.5rem)] p-4 bg-panel text-gray-100 animate-fadeIn">
      <div className="max-w-sm w-full space-y-6 bg-panelLight border border-border rounded-xl p-6 shadow-lg">
        <h1 className="text-3xl font-bold text-center mb-2">Profile</h1>
        {message && <p className="text-green-500 text-center text-sm">{message}</p>}
        {error && <p className="text-red-500 text-center text-sm">{error}</p>}
        <form onSubmit={handleUpdate} className="space-y-4">
          <div className="space-y-1">
            <label htmlFor="email" className="block text-sm font-medium">Email</label>
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
            <label htmlFor="password" className="block text-sm font-medium">New Password</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Leave blank to keep current password"
              className="w-full px-4 py-2 bg-panel border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="w-full py-2 bg-primary rounded-lg hover:bg-primary-dark transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Saving…' : 'Save Changes'}
          </button>
        </form>
        <button
          onClick={handleSignOut}
          className="w-full py-2 mt-4 bg-panel border border-border rounded-lg hover:bg-panel hover:border-primary transition-colors"
        >
          Sign Out
        </button>
      </div>
    </main>
  );
}