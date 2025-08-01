import { BASE_URL, getAuthHeaders, handleApiResponse } from ".";
import type {
  PaginatedResumes,
  Resume,
  ResumeCreatePayload,
  ResumeUpdatePayload,
  ApiError,
} from "./types";

export interface FetchResumesParams {
  page?: number;
  pageSize?: number;
  searchName?: string;
  starred?: boolean;
  minCreatedAt?: string;
  maxCreatedAt?: string;
  sortBy?: "created_at" | "updated_at" | "name";
  sortOrder?: "asc" | "desc";
}

export const fetchResumes = async (
  params: FetchResumesParams = {}
): Promise<PaginatedResumes> => {
  const query = new URLSearchParams();
  if (params.page !== undefined) query.append("page", String(params.page));
  if (params.pageSize !== undefined)
    query.append("page_size", String(params.pageSize));
  if (params.searchName) query.append("search_name", params.searchName);
  if (params.starred !== undefined)
    query.append("starred", String(params.starred));
  if (params.minCreatedAt) query.append("min_created_at", params.minCreatedAt);
  if (params.maxCreatedAt) query.append("max_created_at", params.maxCreatedAt);
  if (params.sortBy) query.append("sort_by", params.sortBy);
  if (params.sortOrder) query.append("sort_order", params.sortOrder);

  const response = await fetch(`${BASE_URL}/resumes/?${query.toString()}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      ...getAuthHeaders(),
    },
  });
  return handleApiResponse<PaginatedResumes>(response);
};

export const createResume = async (
  resumeData: ResumeCreatePayload
): Promise<Resume> => {
  const response = await fetch(`${BASE_URL}/resumes/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...getAuthHeaders(),
    },
    body: JSON.stringify(resumeData),
  });
  return handleApiResponse<Resume>(response);
};

export const fetchResumeById = async (resumeId: string): Promise<Resume> => {
  const response = await fetch(`${BASE_URL}/resumes/${resumeId}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      ...getAuthHeaders(),
    },
  });
  return handleApiResponse<Resume>(response);
};

export const updateResume = async (
  resumeId: string,
  updateData: ResumeUpdatePayload
): Promise<Resume> => {
  const response = await fetch(`${BASE_URL}/resumes/${resumeId}`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      ...getAuthHeaders(),
    },
    body: JSON.stringify(updateData),
  });
  return handleApiResponse<Resume>(response);
};

export const deleteResume = async (resumeId: string): Promise<void> => {
  const response = await fetch(`${BASE_URL}/resumes/${resumeId}`, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
      ...getAuthHeaders(),
    },
  });
  if (!response.ok && response.status !== 204) {
    const errorData: ApiError = await response
      .json()
      .catch(() => ({ message: "An unknown error occurred" }));
    let errorMessage: string;
    if (typeof errorData.detail === "string") {
      errorMessage = errorData.detail;
    } else if (Array.isArray(errorData.detail) && errorData.detail.length > 0) {
      errorMessage = errorData.detail
        .map((err) => `${err.type}: ${err.msg}`)
        .join(", ");
    } else {
      errorMessage =
        errorData.message || `HTTP error! Status: ${response.status}`;
    }
    throw new Error(errorMessage);
  }
};
