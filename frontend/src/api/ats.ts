import { BASE_URL, getAuthHeaders, handleApiResponse } from ".";
import type {
  ATSRequestPayload,
  ATSResponse,
  ATSAnalysis,
  ApiError,
} from "./types";

export const analyzeResume = async (
  payload: ATSRequestPayload
): Promise<ATSResponse> => {
  const response = await fetch(`${BASE_URL}/ats/analyze`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...getAuthHeaders(),
    },
    body: JSON.stringify(payload),
  });

  return handleApiResponse<ATSResponse>(response);
};

export interface GetAnalysisHistoryParams {
  resumeId?: string;
  jobTitle?: string;
  skip?: number;
  limit?: number;
}

export const getAnalysisHistory = async (
  params: GetAnalysisHistoryParams = {}
): Promise<ATSAnalysis[]> => {
  const query = new URLSearchParams();
  if (params.resumeId) query.append("resume_id", params.resumeId);
  if (params.jobTitle) query.append("job_title", params.jobTitle);
  if (params.skip) query.append("skip", String(params.skip));
  if (params.limit) query.append("limit", String(params.limit));
  const response = await fetch(`${BASE_URL}/ats/history?${query.toString()}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      ...getAuthHeaders(),
    },
  });
  return handleApiResponse<ATSAnalysis[]>(response);
};

export interface UpdateAnalysisParams {
  analysisId: string;
  jobTitle: string;
  jobDescription: string;
}

export const updateAnalysis = async (
  params: UpdateAnalysisParams
): Promise<ATSAnalysis> => {
  const response = await fetch(`${BASE_URL}/ats/history/${params.analysisId}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      ...getAuthHeaders(),
    },
    body: JSON.stringify({
      job_title: params.jobTitle,
      job_description: params.jobDescription,
    }),
  });
  return handleApiResponse<ATSAnalysis>(response);
};

export const deleteAnalysis = async (analysisId: string): Promise<void> => {
  const response = await fetch(`${BASE_URL}/ats/history/${analysisId}`, {
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
