import { NextResponse } from 'next/server';

/**
 * Route Handler for sending chat messages.  This handler proxies
 * requests to the FastAPI backend at `/api/chat/send`.  It accepts
 * the same JSON body and returns a JSON response containing the
 * conversation ID.  Errors are propagated as appropriate.
 */
export async function POST(request: Request): Promise<Response> {
  const backendUrl = process.env.BACKEND_URL || 'http://app:8000';
  const body = await request.json();
  const res = await fetch(`${backendUrl}/api/chat/send`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  const data = await res.json();
  return NextResponse.json(data, { status: res.status });
}
