import { NextResponse } from 'next/server';

/**
 * Proxy a login request to the FastAPI backend.  The request body
 * should contain an `email` and `password`.  The backend will return
 * a user and an access token.  This token should be stored by the
 * client; this route does not set cookies on its own.
 */
export async function POST(request: Request): Promise<Response> {
  const backendUrl = process.env.BACKEND_URL || 'http://app:8000';
  const body = await request.json();
  const res = await fetch(`${backendUrl}/api/v1/users/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  const data = await res.json();
  return NextResponse.json(data, { status: res.status });
}