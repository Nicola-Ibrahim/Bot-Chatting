import { NextResponse } from 'next/server';

/**
 * Retrieve the currently authenticated user from the FastAPI backend.
 * The incoming request should include the `Authorization` header set
 * to `Bearer <token>`.  This route simply forwards the header to
 * the backend and returns the user object when authenticated.
 */
export async function GET(request: Request): Promise<Response> {
  const backendUrl = process.env.BACKEND_URL || 'http://app:8000';
  const authHeader = request.headers.get('authorization') || '';
  const res = await fetch(`${backendUrl}/api/v1/users/me`, {
    headers: {
      Authorization: authHeader,
    },
  });
  const data = await res.json();
  return NextResponse.json(data, { status: res.status });
}