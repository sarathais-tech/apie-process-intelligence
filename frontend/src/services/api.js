const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

async function request(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }

  return response.json();
}

export function getEvents() {
  return request('/api/v1/events?limit=50');
}

export function getProcesses() {
  return request('/api/v1/processes?limit=50');
}

export function reconstructProcesses() {
  return request('/api/v1/processes/reconstruct', { method: 'POST' });
}
