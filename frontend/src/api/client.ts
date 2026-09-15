const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export type User = { id: number; email: string; full_name: string; department: string };
export type Service = { id: number; name: string; category: string; description: string; active: boolean };
export type ServiceRequest = {
  id: number;
  user_id: number;
  service_id: number;
  title: string;
  description: string;
  status: string;
};

async function request<T>(path: string, options: RequestInit = {}, token?: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
  });
  const body = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(body.detail ?? "API request failed");
  }
  return body as T;
}

export const api = {
  login: (email: string, password: string) =>
    request<{ access_token: string }>("/api/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }),
  register: (payload: { email: string; password: string; full_name: string; department: string }) =>
    request<User>("/api/auth/register", { method: "POST", body: JSON.stringify(payload) }),
  me: (token: string) => request<User>("/api/users/me", {}, token),
  updateMe: (token: string, payload: Partial<Pick<User, "full_name" | "department">>) =>
    request<User>("/api/users/me", { method: "PUT", body: JSON.stringify(payload) }, token),
  services: (token: string) => request<Service[]>("/api/services", {}, token),
  requests: (token: string, status?: string) =>
    request<ServiceRequest[]>(`/api/requests${status ? `?status=${status}` : ""}`, {}, token),
  createRequest: (token: string, payload: { service_id: number; title: string; description: string }) =>
    request<ServiceRequest>("/api/requests", { method: "POST", body: JSON.stringify(payload) }, token),
  cancelRequest: (token: string, requestId: number) =>
    request<ServiceRequest>(`/api/requests/${requestId}`, { method: "DELETE" }, token),
};
