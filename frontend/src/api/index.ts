import type { ApiError } from "./types";

export const BASE_URL = import.meta.env.VITE_API_URL;

export const handleApiResponse = async <T>(response: Response): Promise<T> => {
  if (!response.ok) {
    const errorData: ApiError = await response
      .json()
      .catch(() => ({ message: "An unknown error occurred" }));
    if (response.status === 429) {
      const retryAfter = response.headers.get("Retry-After");
      throw new Error(
        `Too many requests. Please try again after ${
          retryAfter ? `${retryAfter} seconds` : "some time"
        }.`
      );
    }
    const errorMessage =
      typeof errorData.detail === "string"
        ? errorData.detail
        : Array.isArray(errorData.detail) && errorData.detail.length > 0
        ? errorData.detail.map((err) => `${err.type}: ${err.msg}`).join(", ")
        : errorData.message || `HTTP error! Status: ${response.status}`;
    throw new Error(errorMessage);
  }
  return response.json();
};

export const getAuthHeaders = (): HeadersInit => {
  const token = localStorage.getItem("authToken");
  return token ? { Authorization: `Bearer ${token}` } : {};
};
