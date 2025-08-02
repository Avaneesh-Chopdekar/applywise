import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  analyzeResume,
  deleteAnalysis,
  getAnalysisHistory,
  updateAnalysis,
  type GetAnalysisHistoryParams,
  type UpdateAnalysisParams,
} from "../api/ats";
import type { ATSAnalysis, ATSResponse, ATSRequestPayload } from "../api/types";

export const useATSAnalysis = (payload: ATSRequestPayload) => {
  const queryClient = useQueryClient();
  return useMutation<ATSResponse, Error, ATSRequestPayload>({
    mutationFn: () => analyzeResume(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["atsAnalysis"] });
    },
  });
};

export const useATSAnalysisHistory = (params: GetAnalysisHistoryParams) => {
  return useQuery<ATSAnalysis[], Error>({
    queryKey: ["atsAnalysis", params.resumeId, params.jobTitle],
    queryFn: () => getAnalysisHistory(params),
    enabled: !!params.resumeId && !!params.jobTitle,
  });
};

export const useUpdateATSAnalysis = () => {
  const queryClient = useQueryClient();
  return useMutation<ATSAnalysis, Error, UpdateAnalysisParams>({
    mutationFn: (params) => updateAnalysis(params),
    onSuccess: (updatedAnalysis) => {
      queryClient.invalidateQueries({ queryKey: ["atsAnalysis"] });
      queryClient.invalidateQueries({
        queryKey: ["atsAnalysis", updatedAnalysis._id],
      });
    },
  });
};

export const useDeleteATSAnalysis = () => {
  const queryClient = useQueryClient();
  return useMutation<void, Error, string>({
    mutationFn: (analysisId) => deleteAnalysis(analysisId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["atsAnalysis"] });
    },
  });
};
