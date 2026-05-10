"""Base API client with error handling."""

const API_BASE = process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://localhost:8001/api/v1";


export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public code?: string,
    public details?: Record<string, unknown>
  ) {
    super(message);
    this.name = "ApiError";
  }

  static fromResponse(response: Response, data?: { detail?: string; message?: string }): ApiError {
    const message = data?.detail ?? data?.message ?? `Request failed with status ${response.status}`;
    return new ApiError(message, response.status);
  }
}


interface RequestOptions extends RequestInit {
  timeout?: number;
}


class ApiClient {
  private baseUrl: string;
  private timeout: number;

  constructor(baseUrl: string = API_BASE, timeout: number = 30000) {
    this.baseUrl = baseUrl;
    this.timeout = timeout;
  }

  private async fetch<T>(
    endpoint: string,
    options: RequestOptions = {}
  ): Promise<T> {
    const { timeout, ...fetchOptions } = options;

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout ?? this.timeout);

    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        ...fetchOptions,
        signal: controller.signal,
        credentials: "include",
        headers: {
          ...this.getDefaultHeaders(options.body),
          ...fetchOptions.headers,
        },
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        let errorData: Record<string, unknown> = {};
        try {
          errorData = await response.json();
        } catch {
          // Response is not JSON
        }
        throw ApiError.fromResponse(response, errorData);
      }

      if (response.status === 204) {
        return undefined as T;
      }

      return await response.json();
    } catch (error) {
      clearTimeout(timeoutId);

      if (error instanceof ApiError) {
        throw error;
      }

      if (error instanceof Error) {
        if (error.name === "AbortError") {
          throw new ApiError("Request timeout", 408, "TIMEOUT");
        }
        throw new ApiError(error.message, 0, "NETWORK_ERROR");
      }

      throw new ApiError("Unknown error", 0, "UNKNOWN");
    }
  }

  private getDefaultHeaders(body: unknown): HeadersInit {
    const headers: HeadersInit = {};
    if (body instanceof FormData) {
      // Let browser set Content-Type for FormData
    } else if (body) {
      headers["Content-Type"] = "application/json";
    }
    return headers;
  }

  async get<T>(endpoint: string, options?: RequestOptions): Promise<T> {
    return this.fetch<T>(endpoint, { ...options, method: "GET" });
  }

  async post<T>(endpoint: string, body?: unknown, options?: RequestOptions): Promise<T> {
    return this.fetch<T>(endpoint, {
      ...options,
      method: "POST",
      body: body instanceof FormData ? body : body ? JSON.stringify(body) : undefined,
    });
  }

  async put<T>(endpoint: string, body?: unknown, options?: RequestOptions): Promise<T> {
    return this.fetch<T>(endpoint, {
      ...options,
      method: "PUT",
      body: body ? JSON.stringify(body) : undefined,
    });
  }

  async delete<T>(endpoint: string, options?: RequestOptions): Promise<T> {
    return this.fetch<T>(endpoint, { ...options, method: "DELETE" });
  }

  async patch<T>(endpoint: string, body?: unknown, options?: RequestOptions): Promise<T> {
    return this.fetch<T>(endpoint, {
      ...options,
      method: "PATCH",
      body: body ? JSON.stringify(body) : undefined,
    });
  }
}


export const apiClient = new ApiClient();


export function isApiError(error: unknown): error is ApiError {
  return error instanceof ApiError;
}


export function getErrorMessage(error: unknown): string {
  if (isApiError(error)) {
    return error.message;
  }
  if (error instanceof Error) {
    return error.message;
  }
  return "An unexpected error occurred";
}