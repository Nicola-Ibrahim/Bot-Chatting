const ensureLeadingSlash = (path: string) =>
  path.startsWith('/') ? path : `/${path}`;

const resolveBackendBase = () => {
  const base = process.env.BACKEND_URL || process.env.NEXT_PUBLIC_BACKEND_URL;
  if (!base) {
    throw new Error('BACKEND_URL is not configured.');
  }
  return base;
};

const buildTargetUrl = (path: string) =>
  new URL(ensureLeadingSlash(path), resolveBackendBase()).toString();

export async function postJsonToBackend(path: string, payload: unknown) {
  return fetch(buildTargetUrl(path), {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
    cache: 'no-store',
  });
}

export async function relayBackendResponse(response: Response) {
  const contentType = response.headers.get('content-type') ?? 'application/json';
  const body = await response.text();
  return new Response(body, {
    status: response.status,
    headers: {
      'Content-Type': contentType,
    },
  });
}
