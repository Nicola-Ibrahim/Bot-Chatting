/**
 * Client utility for consuming server‑sent events (SSE) from the chat
 * API.  It opens an EventSource connection to the given URL and
 * invokes the provided callbacks as token and done events are
 * received.  Call the returned function to cancel the stream.
 */
export function streamTokens(
  url: string,
  onToken: (delta: string) => void,
  onDone: () => void,
  onError?: (err: any) => void,
) {
  const source = new EventSource(url);
  const handleToken = (e: MessageEvent) => {
    try {
      const data = JSON.parse(e.data);
      onToken(data.delta || '');
    } catch (err) {
      console.error('Failed to parse token event', err);
    }
  };
  const handleDone = () => {
    onDone();
    source.close();
  };
  const handleError = (e: Event) => {
    if (onError) onError(e);
    source.close();
  };
  source.addEventListener('token', handleToken);
  source.addEventListener('done', handleDone);
  source.onerror = handleError;
  return () => source.close();
}