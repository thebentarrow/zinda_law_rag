import type {
  FAQListResponse,
  LogListResponse,
  QueryResponse,
  UploadResult,
  HealthResponse,
} from "@/types/api";

const BASE = import.meta.env.VITE_API_URL ?? "";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, init);
  if (!res.ok) {
    const body = await res.text();
    throw new Error(body || res.statusText);
  }
  return res.json() as Promise<T>;
}

export const api = {
  query(question: string): Promise<QueryResponse> {
    return request("/api/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });
  },

  getLogs(page = 1, pageSize = 20): Promise<LogListResponse> {
    return request(`/api/logs?page=${page}&page_size=${pageSize}`);
  },

  getFaqs(category?: string, page = 1, pageSize = 50): Promise<FAQListResponse> {
    const params = new URLSearchParams({ page: String(page), page_size: String(pageSize) });
    if (category) params.set("category", category);
    return request(`/api/faqs?${params}`);
  },

  uploadContent(file: File, mode: "append" | "replace"): Promise<UploadResult> {
    const form = new FormData();
    form.append("file", file);
    form.append("mode", mode);
    return request("/api/upload", { method: "POST", body: form });
  },

  health(): Promise<HealthResponse> {
    return request("/api/health");
  },
};
