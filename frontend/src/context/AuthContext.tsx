import {
  createContext,
  useContext,
  useState,
  useCallback,
  useEffect,
  type ReactNode,
} from "react";
import type { TokenResponse } from "../types";
import * as authApi from "../api/auth";

interface AuthContextType {
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (login: string, password: string) => Promise<void>;
  register: (
    login: string,
    password1: string,
    password2: string
  ) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    setIsAuthenticated(!!token);
    setIsLoading(false);
  }, []);

  const saveTokens = (tokens: TokenResponse) => {
    localStorage.setItem("access_token", tokens.access_token);
    localStorage.setItem("refresh_token", tokens.refresh_token);
    setIsAuthenticated(true);
  };

  const login = useCallback(async (login: string, password: string) => {
    const tokens = await authApi.login(login, password);
    saveTokens(tokens);
  }, []);

  const register = useCallback(
    async (login: string, password1: string, password2: string) => {
      const tokens = await authApi.register(login, password1, password2);
      if (tokens) {
        saveTokens(tokens);
      }
    },
    []
  );

  const logout = useCallback(() => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    setIsAuthenticated(false);
  }, []);

  return (
    <AuthContext.Provider
      value={{ isAuthenticated, isLoading, login, register, logout }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
