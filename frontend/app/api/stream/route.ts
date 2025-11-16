import { NextResponse } from 'next/server';

/**
 * Route Handler for streaming chat responses via SSE.  This handler
 * forwards the incoming request to the FastAPI backend, piping the
 * response body directly back to the client.  It ensures the
 * appropriate `Content-Type` header is set to `text/event-stream` and
 * disables automatic response body buffering.
 */
export async function GET(req: Request): Promise<Response> {
  const { searchParams } = new URL(req.url);
  const conversationId = searchParams.get('conversation_id');
  if (!conversationId) {
    return new NextResponse('Missing conversation_id', { status: 400 });
  }
  const backendUrl = process.env.BACKEND_URL || 'http://app:8000';
  const backendResponse = await fetch(
    `${backendUrl}/api/chat/stream?conversation_id=${encodeURIComponent(conversationId)}`,
    {
      headers: {
        Accept: 'text/event-stream',
      },
      // Do not buffer SSE responses
      cache: 'no-store',
    },
  );
  const { readable, writable } = new TransformStream();
  if (backendResponse.body) {
    // Pipe the response body to the writable stream without modification.
    backendResponse.body.pipeTo(writable);
  }
  return new NextResponse(readable, {
    status: backendResponse.status,
    headers: {
      'Content-Type': 'text/event-stream',
    },
  });
}
