import api from "./axios";
import type { TokenResponse } from "../types";

export async function register(
  login: string,
  password1: string,
  password2: string
): Promise<TokenResponse> {
  const { data } = await api.post<TokenResponse>("/api/auth/register", {
    login,
    password1,
    password2,
  });
  return data;
}

export async function login(
  login: string,
  password: string
): Promise<TokenResponse> {
  const { data } = await api.post<TokenResponse>("/api/auth/login", {
    login,
    password,
  });
  return data;
}
