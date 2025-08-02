import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  fetchResumes,
  createResume,
  fetchResumeById,
  updateResume,
  deleteResume,
  type FetchResumesParams,
} from "../api/resume";
import type {
  PaginatedResumes,
  Resume,
  ResumeCreatePayload,
  ResumeUpdatePayload,
} from "../api/types";

export const useResumes = (params: FetchResumesParams) => {
  return useQuery<PaginatedResumes, Error>({
    queryKey: ["resumes", params],
    queryFn: () => fetchResumes(params),
    placeholderData: (previousData) => previousData,
  });
};

export const useResume = (resumeId: string) => {
  return useQuery<Resume, Error>({
    queryKey: ["resume", resumeId],
    queryFn: () => fetchResumeById(resumeId),
    enabled: !!resumeId,
  });
};

export const useCreateResume = () => {
  const queryClient = useQueryClient();
  return useMutation<Resume, Error, ResumeCreatePayload>({
    mutationFn: createResume,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["resumes"] });
    },
  });
};

export const useUpdateResume = () => {
  const queryClient = useQueryClient();
  return useMutation<
    Resume,
    Error,
    { resumeId: string; updateData: ResumeUpdatePayload }
  >({
    mutationFn: ({ resumeId, updateData }) =>
      updateResume(resumeId, updateData),
    onSuccess: (updatedResume) => {
      queryClient.invalidateQueries({ queryKey: ["resumes"] });
      queryClient.invalidateQueries({
        queryKey: ["resume", updatedResume._id],
      });
      queryClient.setQueryData<PaginatedResumes>(["resumes"], (oldData) => {
        if (!oldData) return oldData;
        return {
          ...oldData,
          items: oldData.items.map((r) =>
            r._id === updatedResume._id ? updatedResume : r
          ),
        };
      });
      queryClient.setQueryData<Resume>(
        ["resume", updatedResume._id],
        updatedResume
      );
    },
  });
};

export const useDeleteResume = () => {
  const queryClient = useQueryClient();
  return useMutation<void, Error, string>({
    mutationFn: deleteResume,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["resumes"] });
    },
  });
};
