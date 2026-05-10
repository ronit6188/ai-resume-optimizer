"use client";

import { useState, useCallback } from "react";
import { Resume, uploadResume as apiUploadResume, listResumes as apiListResumes, deleteResume as apiDeleteResume, getResume as apiGetResume } from "@/lib/api/endpoints";

interface UseResumesState {
  resumes: Resume[];
  isLoading: boolean;
  error: string | null;
}

interface UseResumesActions {
  fetchResumes: () => Promise<void>;
  uploadResume: (file: File) => Promise<Resume>;
  deleteResume: (resumeId: string) => Promise<void>;
  getResume: (resumeId: string) => Promise<Resume>;
}

export type UseResumes = UseResumesState & UseResumesActions;

export function useResumes(): UseResumes {
  const [state, setState] = useState<UseResumesState>({
    resumes: [],
    isLoading: false,
    error: null,
  });

  const setLoading = (isLoading: boolean) => {
    setState((prev) => ({ ...prev, isLoading, error: null }));
  };

  const setError = (error: string) => {
    setState((prev) => ({ ...prev, isLoading: false, error }));
  };

  const fetchResumes = useCallback(async () => {
    setLoading(true);
    try {
      const response = await apiListResumes();
      setState((prev) => ({
        ...prev,
        resumes: response.resumes,
        isLoading: false,
      }));
    } catch (error) {
      setError(error instanceof Error ? error.message : "Failed to fetch resumes");
    }
  }, []);

  const uploadResume = useCallback(async (file: File): Promise<Resume> => {
    setLoading(true);
    try {
      const resume = await apiUploadResume(file);
      setState((prev) => ({
        ...prev,
        resumes: [resume, ...prev.resumes],
        isLoading: false,
      }));
      return resume;
    } catch (error) {
      setError(error instanceof Error ? error.message : "Failed to upload resume");
      throw error;
    }
  }, []);

  const deleteResume = useCallback(async (resumeId: string) => {
    setLoading(true);
    try {
      await apiDeleteResume(resumeId);
      setState((prev) => ({
        ...prev,
        resumes: prev.resumes.filter((r) => r.id !== resumeId),
        isLoading: false,
      }));
    } catch (error) {
      setError(error instanceof Error ? error.message : "Failed to delete resume");
      throw error;
    }
  }, []);

  const getResume = useCallback(async (resumeId: string): Promise<Resume> => {
    setLoading(true);
    try {
      const resume = await apiGetResume(resumeId);
      setState((prev) => ({ ...prev, isLoading: false }));
      return resume;
    } catch (error) {
      setError(error instanceof Error ? error.message : "Failed to get resume");
      throw error;
    }
  }, []);

  return {
    ...state,
    fetchResumes,
    uploadResume,
    deleteResume,
    getResume,
  };
}