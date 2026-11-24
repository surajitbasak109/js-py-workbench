/**
 * Retries an async operation with exponential backoff.
 */
export async function retryAsync(fn, { retries = 3, delayMs = 250 } = {}) {
  let lastError;
  for (let attempt = 0; attempt <= retries; attempt++) {
    try {
      return await fn();
    } catch (err) {
      lastError = err;
      if (attempt < retries) {
        await new Promise((r) => setTimeout(r, delayMs * 2 ** attempt));
      }
    }
  }
  throw lastError;
}

/**
 * Safely parses JSON and returns a fallback instead of throwing.
 */
export function safeJsonParse(raw, fallback = null) {
  try {
    return JSON.parse(raw);
  } catch {
    return fallback;
  }
}

/**
 * Debounces frequent UI events (search inputs, resize, scroll).
 */
export function debounce(fn, waitMs = 300) {
  let timerId;
  return (...args) => {
    clearTimeout(timerId);
    timerId = setTimeout(() => fn(...args), waitMs);
  };
}

/**
 * Calls a local Python HTTP endpoint with clean error handling.
 */
export async function callPythonApi(baseUrl, path, payload = null) {
  const options = {
    method: payload ? "POST" : "GET",
    headers: { "Content-Type": "application/json" },
  };
  if (payload) options.body = JSON.stringify(payload);

  const res = await fetch(`${baseUrl.replace(/\/$/, "")}${path}`, options);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Python API error (${res.status}): ${text}`);
  }
  return res.json();
}
