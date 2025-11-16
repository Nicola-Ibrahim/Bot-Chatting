"use client";

/**
 * Helper functions for managing authentication state in the browser.  The
 * token and user objects are persisted to localStorage.  These
 * functions gracefully handle server‑side rendering by guarding
 * against the absence of the `window` object.
 */

export interface User {
  id: string;
  email: string;
  is_verified: boolean;
  is_active: boolean;
}

/**
 * Return the current bearer token from localStorage, or null if none
 * exists or if called on the server.  Tokens are stored under the
 * "token" key.
 */
export function getToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('token');
}

/**
 * Persist the given bearer token to localStorage.  Ignored when
 * executed on the server.  Clears any existing token.
 */
export function setToken(token: string) {
  if (typeof window === 'undefined') return;
  localStorage.setItem('token', token);
}

/**
 * Remove the current bearer token and user from localStorage.  Use
 * this when signing out.  Ignored on the server.
 */
export function clearToken() {
  if (typeof window === 'undefined') return;
  localStorage.removeItem('token');
  localStorage.removeItem('user');
}

/**
 * Retrieve the current user from localStorage, parsing the stored
 * JSON into a `User` type.  Returns null if no user is stored or
 * parsing fails.
 */
export function getUser(): User | null {
  if (typeof window === 'undefined') return null;
  const raw = localStorage.getItem('user');
  if (!raw) return null;
  try {
    return JSON.parse(raw) as User;
  } catch {
    return null;
  }
}

/**
 * Persist a user object to localStorage.  This overwrites any
 * existing value.  Ignored when executed on the server.
 */
export function setUser(user: User) {
  if (typeof window === 'undefined') return;
  localStorage.setItem('user', JSON.stringify(user));
}
