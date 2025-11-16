import { NextResponse } from 'next/server';

/**
 * Proxy a user update request to the FastAPI backend.  The request
 * should include a JSON body with `user_id` and any fields to
 * update (e.g. `email`, `password`).  The `Authorization` header is
 * forwarded from the client request to authenticate the update.
 */
export async function PATCH(request: Request): Promise<Response> {
  const backendUrl = process.env.BACKEND_URL || 'http://app:8000';
  const authHeader = request.headers.get('authorization') || '';
  const body = await request.json();
  const { user_id, ...updateFields } = body;
  if (!user_id) {
    return NextResponse.json({ detail: 'Missing user_id' }, { status: 400 });
  }
  const res = await fetch(`${backendUrl}/api/v1/users/${encodeURIComponent(user_id)}`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      Authorization: authHeader,
    },
    body: JSON.stringify(updateFields),
  });
  // Return JSON even when no content (204) to simplify client handling
  const text = await res.text();
  let data;
  try {
    data = text ? JSON.parse(text) : {};
  } catch {
    data = {};
  }
  return NextResponse.json(data, { status: res.status });
}
