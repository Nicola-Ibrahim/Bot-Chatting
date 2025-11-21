import { NextResponse } from 'next/server';
import { postJsonToBackend, relayBackendResponse } from '@/app/api/_lib/backend';

const TITLE_PATH = process.env.BACKEND_TITLE_PATH || '/api/title';

export const dynamic = 'force-dynamic';

export async function POST(request: Request) {
  try {
    const payload = await request.json();
    const backendResponse = await postJsonToBackend(TITLE_PATH, payload);
    return relayBackendResponse(backendResponse);
  } catch (error) {
    console.error('Failed to proxy title request', error);
    const status =
      error instanceof Error && error.message.includes('BACKEND_URL') ? 500 : 502;
    return NextResponse.json(
      { error: 'Unable to reach the title backend.' },
      { status }
    );
  }
}
