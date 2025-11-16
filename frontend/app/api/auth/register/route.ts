import { NextResponse } from 'next/server';

/**
 * Proxy a registration request to the FastAPI backend.  The body
 * should include an `email` and `password`.  The backend returns
 * the created user.  Clients may wish to log the user in
 * immediately after registration.
 */
export async function POST(request: Request): Promise<Response> {
  const backendUrl = process.env.BACKEND_URL || 'http://app:8000';
  const body = await request.json();
  const res = await fetch(`${backendUrl}/api/v1/users/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  const data = await res.json();
  return NextResponse.json(data, { status: res.status });
}
