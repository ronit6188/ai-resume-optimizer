"use client";

import { useState, useEffect, useCallback } from "react";
import { User, TokenResponse, signup as apiSignup, login as apiLogin, logout as apiLogout, getMe } from "@/lib/api/endpoints";

interface UseAuthState {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
}

interface UseAuthActions {
  signup: (email: string, password: string) => Promise<void>;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  checkAuth: () => Promise<void>;
}

export type UseAuth = UseAuthState & UseAuthActions;

export function useAuth(): UseAuth {
  const [state, setState] = useState<UseAuthState>({
    user: null,
    isLoading: true,
    isAuthenticated: false,
  });

  const checkAuth = useCallback(async () => {
    try {
      const user = await getMe();
      setState({
        user,
        isLoading: false,
        isAuthenticated: true,
      });
    } catch {
      setState({
        user: null,
        isLoading: false,
        isAuthenticated: false,
      });
    }
  }, []);

  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  const signup = useCallback(async (email: string, password: string) => {
    setState((prev) => ({ ...prev, isLoading: true }));
    try {
      await apiSignup(email, password);
      await checkAuth();
    } catch (error) {
      setState((prev) => ({ ...prev, isLoading: false }));
      throw error;
    }
  }, [checkAuth]);

  const login = useCallback(async (email: string, password: string) => {
    setState((prev) => ({ ...prev, isLoading: true }));
    try {
      await apiLogin(email, password);
      await checkAuth();
    } catch (error) {
      setState((prev) => ({ ...prev, isLoading: false }));
      throw error;
    }
  }, [checkAuth]);

  const logout = useCallback(async () => {
    try {
      await apiLogout();
    } finally {
      setState({
        user: null,
        isLoading: false,
        isAuthenticated: false,
      });
    }
  }, []);

  return {
    ...state,
    signup,
    login,
    logout,
    checkAuth,
  };
}