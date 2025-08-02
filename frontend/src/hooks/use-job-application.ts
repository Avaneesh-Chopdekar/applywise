import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  fetchJobApplications,
  createJobApplication,
  fetchJobApplicationById,
  updateJobApplication,
  deleteJobApplication,
  type FetchJobApplicationsParams,
} from "../api/job-application";
import type {
  PaginatedJobApplications,
  JobApplication,
  JobApplicationCreatePayload,
  JobApplicationUpdatePayload,
  JobApplicationListItem,
} from "../api/types";

export const useJobApplications = (params: FetchJobApplicationsParams) => {
  return useQuery<PaginatedJobApplications, Error>({
    queryKey: ["jobApplications", params],
    queryFn: () => fetchJobApplications(params),
    placeholderData: (previousData) => previousData,
  });
};

export const useJobApplication = (appId: string) => {
  return useQuery<JobApplication, Error>({
    queryKey: ["jobApplication", appId],
    queryFn: () => fetchJobApplicationById(appId),
    enabled: !!appId,
  });
};

export const useCreateJobApplication = () => {
  const queryClient = useQueryClient();
  return useMutation<
    JobApplicationListItem,
    Error,
    JobApplicationCreatePayload
  >({
    mutationFn: createJobApplication,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["jobApplications"] });
    },
  });
};

export const useUpdateJobApplication = () => {
  const queryClient = useQueryClient();
  return useMutation<
    JobApplicationListItem,
    Error,
    { appId: string; payload: JobApplicationUpdatePayload }
  >({
    mutationFn: ({ appId, payload }) => updateJobApplication(appId, payload),
    onSuccess: (updatedApp) => {
      queryClient.invalidateQueries({ queryKey: ["jobApplications"] });
      queryClient.invalidateQueries({
        queryKey: ["jobApplication", updatedApp._id],
      });
      queryClient.setQueryData<PaginatedJobApplications>(
        ["jobApplications"],
        (oldData) => {
          if (!oldData) return oldData;
          return {
            ...oldData,
            items: oldData.items.map((app) =>
              app._id === updatedApp._id ? updatedApp : app
            ),
          };
        }
      );
      queryClient.setQueryData<JobApplication>(
        ["jobApplication", updatedApp._id],
        updatedApp as JobApplication
      );
    },
  });
};

export const useDeleteJobApplication = () => {
  const queryClient = useQueryClient();
  return useMutation<void, Error, string>({
    mutationFn: deleteJobApplication,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["jobApplications"] });
    },
  });
};
