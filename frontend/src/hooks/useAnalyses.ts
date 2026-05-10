"use client";

import { useState, useCallback } from "react";
import { Analysis, createAnalysis as apiCreateAnalysis, listAnalyses as apiListAnalyses, getAnalysis as apiGetAnalysis, deleteAnalysis as apiDeleteAnalysis } from "@/lib/api/endpoints";

interface UseAnalysesState {
  analyses: Analysis[];
  currentAnalysis: Analysis | null;
  isLoading: boolean;
  error: string | null;
}

interface UseAnalysesActions {
  fetchAnalyses: () => Promise<void>;
  createAnalysis: (resumeId: string, jobDescId?: string) => Promise<Analysis>;
  getAnalysis: (analysisId: string) => Promise<Analysis>;
  deleteAnalysis: (analysisId: string) => Promise<void>;
  clearCurrentAnalysis: () => void;
}

export type UseAnalyses = UseAnalysesState & UseAnalysesActions;

export function useAnalyses(): UseAnalyses {
  const [state, setState] = useState<UseAnalysesState>({
    analyses: [],
    currentAnalysis: null,
    isLoading: false,
    error: null,
  });

  const setLoading = (isLoading: boolean) => {
    setState((prev) => ({ ...prev, isLoading, error: null }));
  };

  const setError = (error: string) => {
    setState((prev) => ({ ...prev, isLoading: false, error }));
  };

  const fetchAnalyses = useCallback(async () => {
    setLoading(true);
    try {
      const response = await apiListAnalyses();
      setState((prev) => ({
        ...prev,
        analyses: response.analyses,
        isLoading: false,
      }));
    } catch (error) {
      setError(error instanceof Error ? error.message : "Failed to fetch analyses");
    }
  }, []);

  const createAnalysis = useCallback(async (resumeId: string, jobDescId?: string): Promise<Analysis> => {
    setLoading(true);
    try {
      const analysis = await apiCreateAnalysis(resumeId, jobDescId);
      setState((prev) => ({
        ...prev,
        analyses: [analysis, ...prev.analyses],
        currentAnalysis: analysis,
        isLoading: false,
      }));
      return analysis;
    } catch (error) {
      setError(error instanceof Error ? error.message : "Failed to create analysis");
      throw error;
    }
  }, []);

  const getAnalysis = useCallback(async (analysisId: string): Promise<Analysis> => {
    setLoading(true);
    try {
      const analysis = await apiGetAnalysis(analysisId);
      setState((prev) => ({
        ...prev,
        currentAnalysis: analysis,
        isLoading: false,
      }));
      return analysis;
    } catch (error) {
      setError(error instanceof Error ? error.message : "Failed to get analysis");
      throw error;
    }
  }, []);

  const deleteAnalysis = useCallback(async (analysisId: string) => {
    setLoading(true);
    try {
      await apiDeleteAnalysis(analysisId);
      setState((prev) => ({
        ...prev,
        analyses: prev.analyses.filter((a) => a.id !== analysisId),
        currentAnalysis: prev.currentAnalysis?.id === analysisId ? null : prev.currentAnalysis,
        isLoading: false,
      }));
    } catch (error) {
      setError(error instanceof Error ? error.message : "Failed to delete analysis");
      throw error;
    }
  }, []);

  const clearCurrentAnalysis = useCallback(() => {
    setState((prev) => ({ ...prev, currentAnalysis: null }));
  }, []);

  return {
    ...state,
    fetchAnalyses,
    createAnalysis,
    getAnalysis,
    deleteAnalysis,
    clearCurrentAnalysis,
  };
}