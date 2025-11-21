/**
 * Chat service for communicating with the backend API through the Next.js
 * route handlers.
 *
 * All requests default to the local `/api/*` routes which proxy to the
 * FastAPI service that runs in Docker. Set `NEXT_PUBLIC_FRONTEND_API_BASE`
 * if the proxy is mounted elsewhere (for example, when hitting a remote
 * deployment URL).
 */

const FRONTEND_API_BASE =
  (process.env.NEXT_PUBLIC_FRONTEND_API_BASE || '/api').replace(/\/$/, '');

const withBase = (path: string) =>
  `${FRONTEND_API_BASE}${path.startsWith('/') ? path : `/${path}`}`;

/**
 * Submit a new chat message and retrieve the assistant's response.
 *
 * @param history Previous messages in the conversation, formatted as objects
 *                containing a `role` ("user" | "model") and `parts` with
 *                the message text. This matches the serialized payload the
 *                backend expects.
 * @param newMessage The latest user message that should be answered.
 * @returns A promise resolving to the assistant's reply as a string.
 */
export async function generateChatResponse(
  history: { role: string; parts: { text: string }[] }[],
  newMessage: string
): Promise<string> {
  try {
    const res = await fetch(withBase('/chat'), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ history, message: newMessage }),
    });
    if (!res.ok) {
      const text = await res.text();
      throw new Error(`Backend error ${res.status}: ${text}`);
    }
    const data = await res.json();
    return data.response || data.message || 'No response generated.';
  } catch (error: any) {
    console.error('Error in generateChatResponse:', error);
    throw error;
  }
}

/**
 * Generate a brief title for a conversation.
 *
 * If a backend title endpoint exists, it will be used. Otherwise, the
 * title is derived locally from the first message. Adjust the endpoint
 * `/api/title` to match your backend's contract or replace this logic
 * entirely if not needed.
 *
 * @param firstMessage The first user message.
 * @returns A promise resolving to a short title string.
 */
export async function generateConversationTitle(firstMessage: string): Promise<string> {
  try {
    const res = await fetch(withBase('/title'), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message: firstMessage }),
    });
    if (res.ok) {
      const data = await res.json();
      return data.title || data.response || firstMessage.slice(0, 50);
    }
    // fallback if backend returns an error
    return firstMessage.slice(0, 50);
  } catch (error) {
    // derive a title by taking up to the first five words
    const words = firstMessage.split(' ');
    return words.slice(0, 5).join(' ');
  }
}
