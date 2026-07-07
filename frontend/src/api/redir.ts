import api from "./axios";
import type { RedirRequest, RedirResponse } from "../types";

export async function addRedirect(
  req: RedirRequest
): Promise<RedirResponse> {
  const { data } = await api.post<RedirResponse>("/api/redir/add", {
    default_url: req.default_url,
    custom_url: req.custom_url || "default",
  });
  return data;
}

export async function listRedirects(): Promise<RedirResponse[]> {
  const { data } = await api.get<RedirResponse[]>("/api/redir/list");
  return data;
}

export async function deleteRedirect(redirUrl: string): Promise<void> {
  await api.delete(`/api/redir/del/${redirUrl}`);
}
