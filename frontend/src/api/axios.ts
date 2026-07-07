import axios from "axios";
import type { ApiError, PydanticError } from "../types";

const api = axios.create({
  baseURL: "",
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
});

export function parseApiError(error: unknown): string {
  if (!axios.isAxiosError(error) || !error.response) {
    return "Network error. Check your connection.";
  }

  const status = error.response.status;
  const data = error.response.data;

  if (status === 401 || status === 403) {
    const errData = data as ApiError;
    if (errData?.error_type) {
      const messages: Record<string, string> = {
        UserNotFound: "User not found",
        InvalidPassword: "Invalid password",
        CredentialsRequired: "Please log in",
        NotAuthenticated: "Please log in",
        TokenRequired: "Session expired, please log in again",
        InvalidToken: "Session expired, please log in again",
      };
      return messages[errData.error_type] || errData.message || "Unauthorized";
    }
    return "Session expired, please log in again";
  }

  if (status === 404) {
    const errData = data as ApiError;
    const messages: Record<string, string> = {
      URLNotFound: "URL not found or expired",
      ListEmpty: "No redirects yet",
    };
    return messages[errData?.error_type] || errData?.message || "Not found";
  }

  if (status === 409) {
    const errData = data as ApiError;
    const messages: Record<string, string> = {
      UserAlreadyExists: "User already exists",
      RedirCreateError: "This short URL is already taken",
    };
    return messages[errData?.error_type] || errData?.message || "Conflict";
  }

  if (status === 422) {
    const errData = data as PydanticError;
    if (errData?.detail?.length) {
      return errData.detail.map((e) => e.msg).join(". ");
    }
    return "Validation error";
  }

  return "Something went wrong";
}

export default api;
