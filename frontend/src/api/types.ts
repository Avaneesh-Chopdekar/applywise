export interface ResumeListItem {
  _id: string;
  name: string;
  user_id: string;
  starred: boolean;
  created_at: string;
  updated_at: string;
}

export interface PaginatedResumes {
  total: number;
  page: number;
  page_size: number;
  items: ResumeListItem[];
}

export interface Resume {
  _id: string;
  user_id: string;
  name: string;
  starred: boolean;
  contact?: {
    phone?: string;
    email?: string;
    linkedin?: string;
    github?: string;
  };
  education: Array<{
    institution: string;
    location?: string;
    degree: string;
    major?: string;
    minor?: string;
    start_date?: string;
    end_date?: string;
    description?: string[];
  }>;
  experience: Array<{
    title: string;
    company: string;
    location?: string;
    start_date?: string;
    end_date?: string;
    description: string[];
  }>;
  projects: Array<{
    name: string;
    technologies?: string;
    date_range?: string;
    link?: string;
    description: string[];
  }>;
  skills: Array<{
    category: string;
    items: string;
  }>;
  created_at: string;
  updated_at: string;
}

export type ResumeCreatePayload = Omit<
  Resume,
  "_id" | "created_at" | "updated_at"
>;

export type ResumeUpdatePayload = Partial<ResumeCreatePayload> & {
  starred?: boolean;
};

export interface ATSRequestPayload {
  resume_id: string;
  job_title: string;
  job_description: string;
}

export interface ATSResponse {
  relevance_score: number;
  skills: string[];
  total_years_of_experience: number;
  project_categories: string[];
}

export interface ATSAnalysis {
  _id: string;
  llm_analysis: ATSResponse;
  resume_id: string;
  job_title: string;
  job_description: string;
  created_at: string;
}

export interface JobApplication {
  _id: string;
  user_id: string;
  job_title: string;
  company_name: string;
  company_website?: string;
  job_url?: string;
  location?: string;
  status: string;
  application_date: string; // (YYYY-MM-DD)
  last_updated: string;
  interview_dates: string[]; // (YYYY-MM-DD)
  notes?: string;
  associated_resume_id?: string;
  associated_analysis_id?: string;
}

export type JobApplicationCreatePayload = Omit<
  JobApplication,
  "_id" | "last_updated"
>;

export type JobApplicationUpdatePayload = Partial<JobApplicationCreatePayload>;

export interface JobApplicationListItem {
  _id: string;
  user_id: string;
  job_title: string;
  company_name: string;
  status: string;
  application_date: string;
  last_updated: string;
  associated_resume_id?: string;
  associated_analysis_id?: string;
}

export interface PaginatedJobApplications {
  total: number;
  page: number;
  page_size: number;
  items: JobApplicationListItem[];
}

export interface ApiError {
  detail?: string | { msg: string; type: string }[];
  message?: string;
}
