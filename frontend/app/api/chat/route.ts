import { NextResponse } from 'next/server';
import { postJsonToBackend, relayBackendResponse } from '@/app/api/_lib/backend';

const CHAT_PATH = process.env.BACKEND_CHAT_PATH || '/api/chat';

export const dynamic = 'force-dynamic';

export async function POST(request: Request) {
  try {
    const payload = await request.json();
    const backendResponse = await postJsonToBackend(CHAT_PATH, payload);
    return relayBackendResponse(backendResponse);
  } catch (error) {
    console.error('Failed to proxy chat request', error);
    const status =
      error instanceof Error && error.message.includes('BACKEND_URL') ? 500 : 502;
    return NextResponse.json(
      { error: 'Unable to reach the chat backend.' },
      { status }
    );
  }
}
