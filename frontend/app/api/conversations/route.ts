import { NextResponse } from 'next/server';

/**
 * Route Handler for listing conversations.  Proxies GET requests to
 * the FastAPI endpoint `/api/conversations/`.  Returns a JSON array
 * of conversation summaries.
 */
export async function GET(): Promise<Response> {
  const backendUrl = process.env.BACKEND_URL || 'http://app:8000';
  const res = await fetch(`${backendUrl}/api/conversations/`, { cache: 'no-store' });
  const data = await res.json();
  return NextResponse.json(data, { status: res.status });
}