import type {
  CalendarEvent,
  EventInput
} from '#lib/types/event.ts';

const API = 'http://localhost:8000';

export interface AuthUser {
  id: string;
  name: string;
  email: string;
}

async function request<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const response = await fetch(`${API}${path}`, {
    ...options,
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      ...options.headers
    }
  });

  if (!response.ok) {
    const body = await response.json().catch(() => null);

    throw new Error(
      body?.detail instanceof Array
        ? 'Please check the submitted information.'
        : typeof body?.detail === 'string'
          ? body.detail
          : `Request failed (${response.status})`
    );
  }

  return response.json() as Promise<T>;
}

export const api = {
  register: (data: {
    name: string;
    email: string;
    password: string;
  }) =>
    request<AuthUser>('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify(data)
    }),

  login: (email: string, password: string) =>
    request<AuthUser>('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password })
    }),

  me: () => request<AuthUser>('/api/auth/me'),

  logout: () =>
    request<{ message: string }>('/api/auth/logout', {
      method: 'POST'
    }),

  getEvents: () =>
    request<CalendarEvent[]>('/api/events'),

  createEvent: (data: EventInput) =>
    request<CalendarEvent>('/api/events', {
      method: 'POST',
      body: JSON.stringify(data)
    }),

  updateEvent: (id: string, data: EventInput) =>
    request<CalendarEvent>(`/api/events/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(data)
    }),

  deleteEvent: (id: string) =>
    request<{ message: string }>(
      `/api/events/${id}`,
      { method: 'DELETE' }
    )
};
