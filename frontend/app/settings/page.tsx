"use client";

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { getToken, getUser } from '@/lib/auth';

/**
 * Settings page placeholder.  In a more complete application this
 * page could allow users to manage preferences, theme options or
 * billing details.  Currently it simply restricts access to
 * authenticated users and displays a message.
 */
export default function SettingsPage() {
  const router = useRouter();
  useEffect(() => {
    const token = getToken();
    const user = getUser();
    if (!token || !user) {
      router.replace('/auth/login');
    }
  }, [router]);
  return (
    <main className="flex flex-col items-center justify-center min-h-[calc(100vh-3.5rem)] p-4 bg-panel text-gray-100 animate-fadeIn">
      <div className="max-w-sm w-full space-y-6 bg-panelLight border border-border rounded-xl p-6 shadow-lg text-center">
        <h1 className="text-3xl font-bold">Settings</h1>
        <p className="text-gray-400">This is a placeholder for settings. Coming soon!</p>
      </div>
    </main>
  );
}
