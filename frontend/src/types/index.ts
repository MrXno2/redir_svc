export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface RedirResponse {
  default_url: string;
  redir_url: string;
  redir_count: number;
}

export interface RedirRequest {
  default_url: string;
  custom_url?: string;
}

export interface ApiError {
  message: string;
  error_type: string;
}

export interface PydanticError {
  detail: Array<{
    type: string;
    loc: string[];
    msg: string;
    input?: unknown;
  }>;
}
