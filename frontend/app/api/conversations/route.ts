import { NextResponse } from 'next/server';

// Avoid static export attempting to pre-render this route
export const dynamic = 'force-dynamic';
export const fetchCache = 'force-no-store';

/**
 * Route Handler for listing conversations.  Proxies GET requests to
 * the FastAPI endpoint `/api/conversations/`.  Returns a JSON array
 * of conversation summaries.
 */
export async function GET(): Promise<Response> {
  const backendUrl = process.env.BACKEND_URL || 'http://app:8000';
  try {
    const res = await fetch(`${backendUrl}/api/conversations/`, { cache: 'no-store' });
    const data = await res.json();
    return NextResponse.json(data, { status: res.status });
  } catch (err) {
    // Return a graceful error instead of crashing build/edge rendering
    return NextResponse.json({ error: 'Failed to reach backend', detail: `${err}` }, { status: 502 });
  }
}
