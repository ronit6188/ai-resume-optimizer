"use client";

import { useState, useCallback } from "react";
import { JobDescription, createJob as apiCreateJob, listJobs as apiListJobs, deleteJob as apiDeleteJob, getJob as apiGetJob, calculateMatch as apiCalculateMatch, MatchResult } from "@/lib/api/endpoints";

interface UseJobsState {
  jobs: JobDescription[];
  isLoading: boolean;
  error: string | null;
}

interface UseJobsActions {
  fetchJobs: () => Promise<void>;
  createJob: (title: string, description: string) => Promise<JobDescription>;
  deleteJob: (jobId: string) => Promise<void>;
  getJob: (jobId: string) => Promise<JobDescription>;
  calculateMatch: (resumeId: string, jobId: string) => Promise<MatchResult>;
}

export type UseJobs = UseJobsState & UseJobsActions;

export function useJobs(): UseJobs {
  const [state, setState] = useState<UseJobsState>({
    jobs: [],
    isLoading: false,
    error: null,
  });

  const setLoading = (isLoading: boolean) => {
    setState((prev) => ({ ...prev, isLoading, error: null }));
  };

  const setError = (error: string) => {
    setState((prev) => ({ ...prev, isLoading: false, error }));
  };

  const fetchJobs = useCallback(async () => {
    setLoading(true);
    try {
      const response = await apiListJobs();
      setState((prev) => ({
        ...prev,
        jobs: response.jobs,
        isLoading: false,
      }));
    } catch (error) {
      setError(error instanceof Error ? error.message : "Failed to fetch jobs");
    }
  }, []);

  const createJob = useCallback(async (title: string, description: string): Promise<JobDescription> => {
    setLoading(true);
    try {
      const job = await apiCreateJob(title, description);
      setState((prev) => ({
        ...prev,
        jobs: [job, ...prev.jobs],
        isLoading: false,
      }));
      return job;
    } catch (error) {
      setError(error instanceof Error ? error.message : "Failed to create job");
      throw error;
    }
  }, []);

  const deleteJob = useCallback(async (jobId: string) => {
    setLoading(true);
    try {
      await apiDeleteJob(jobId);
      setState((prev) => ({
        ...prev,
        jobs: prev.jobs.filter((j) => j.id !== jobId),
        isLoading: false,
      }));
    } catch (error) {
      setError(error instanceof Error ? error.message : "Failed to delete job");
      throw error;
    }
  }, []);

  const getJob = useCallback(async (jobId: string): Promise<JobDescription> => {
    setLoading(true);
    try {
      const job = await apiGetJob(jobId);
      setState((prev) => ({ ...prev, isLoading: false }));
      return job;
    } catch (error) {
      setError(error instanceof Error ? error.message : "Failed to get job");
      throw error;
    }
  }, []);

  const calculateMatch = useCallback(async (resumeId: string, jobId: string): Promise<MatchResult> => {
    setLoading(true);
    try {
      const result = await apiCalculateMatch(resumeId, jobId);
      setState((prev) => ({ ...prev, isLoading: false }));
      return result;
    } catch (error) {
      setError(error instanceof Error ? error.message : "Failed to calculate match");
      throw error;
    }
  }, []);

  return {
    ...state,
    fetchJobs,
    createJob,
    deleteJob,
    getJob,
    calculateMatch,
  };
}