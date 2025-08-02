import { BASE_URL, getAuthHeaders, handleApiResponse } from ".";
import type {
  JobApplication,
  JobApplicationCreatePayload,
  JobApplicationUpdatePayload,
  JobApplicationListItem,
  PaginatedJobApplications,
  ApiError,
} from "./types";

export interface FetchJobApplicationsParams {
  page?: number;
  pageSize?: number;
  searchTitle?: string;
  searchCompany?: string;
  status?: string;
  minApplicationDate?: string; // (YYYY-MM-DD)
  maxApplicationDate?: string; // (YYYY-MM-DD)
  hasNotes?: boolean;
  hasInterviewDates?: boolean;
  userId?: string;
  associatedResumeId?: string;
  associatedAnalysisId?: string;
  sortBy?: "application_date" | "last_updated" | "job_title";
  sortOrder?: "asc" | "desc";
}

export const fetchJobApplications = async (
  params: FetchJobApplicationsParams = {}
): Promise<PaginatedJobApplications> => {
  const query = new URLSearchParams();
  if (params.page !== undefined) query.append("page", String(params.page));
  if (params.pageSize !== undefined)
    query.append("page_size", String(params.pageSize));
  if (params.searchTitle) query.append("search_title", params.searchTitle);
  if (params.searchCompany)
    query.append("search_company", params.searchCompany);
  if (params.status) query.append("status", params.status);
  if (params.minApplicationDate)
    query.append("min_application_date", params.minApplicationDate);
  if (params.maxApplicationDate)
    query.append("max_application_date", params.maxApplicationDate);
  if (params.hasNotes !== undefined)
    query.append("has_notes", String(params.hasNotes));
  if (params.hasInterviewDates !== undefined)
    query.append("has_interview_dates", String(params.hasInterviewDates));
  if (params.userId) query.append("user_id", params.userId);
  if (params.associatedResumeId)
    query.append("associated_resume_id", params.associatedResumeId);
  if (params.associatedAnalysisId)
    query.append("associated_analysis_id", params.associatedAnalysisId);
  if (params.sortBy) query.append("sort_by", params.sortBy);
  if (params.sortOrder) query.append("sort_order", params.sortOrder);

  const response = await fetch(
    `${BASE_URL}/job-applications/?${query.toString()}`,
    {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        ...getAuthHeaders(),
      },
    }
  );
  return handleApiResponse<PaginatedJobApplications>(response);
};

export const fetchJobApplicationById = async (
  applicationId: string
): Promise<JobApplication> => {
  const response = await fetch(
    `${BASE_URL}/job-applications/${applicationId}`,
    {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        ...getAuthHeaders(),
      },
    }
  );
  return handleApiResponse<JobApplication>(response);
};

export const createJobApplication = async (
  applicationData: JobApplicationCreatePayload
): Promise<JobApplicationListItem> => {
  const response = await fetch(`${BASE_URL}/job-applications/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...getAuthHeaders(),
    },
    body: JSON.stringify(applicationData),
  });
  return handleApiResponse<JobApplicationListItem>(response);
};

export const updateJobApplication = async (
  applicationId: string,
  applicationData: JobApplicationUpdatePayload
): Promise<JobApplication> => {
  const response = await fetch(
    `${BASE_URL}/job-applications/${applicationId}`,
    {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        ...getAuthHeaders(),
      },
      body: JSON.stringify(applicationData),
    }
  );
  return handleApiResponse<JobApplication>(response);
};

export const deleteJobApplication = async (
  applicationId: string
): Promise<void> => {
  const response = await fetch(
    `${BASE_URL}/job-applications/${applicationId}`,
    {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        ...getAuthHeaders(),
      },
    }
  );
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
