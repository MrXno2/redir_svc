import { useEffect, useState, useCallback } from "react";
import { listRedirects, deleteRedirect, addRedirect } from "../api/redir";
import { parseApiError } from "../api/axios";
import type { RedirResponse } from "../types";
import { RedirectCard } from "../components/RedirectCard";
import { AddRedirect } from "../components/AddRedirect";
import { toast } from "../components/Toast";
import { Link2, Inbox } from "lucide-react";

export function DashboardPage() {
  const [redirects, setRedirects] = useState<RedirResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchRedirects = useCallback(async () => {
    try {
      const data = await listRedirects();
      setRedirects(data);
      setError("");
    } catch (err) {
      const msg = parseApiError(err);
      if (msg === "No redirects yet") {
        setRedirects([]);
        setError("");
      } else {
        setError(msg);
      }
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchRedirects();
  }, [fetchRedirects]);

  const handleAdd = async (url: string, custom: string) => {
    await addRedirect({ default_url: url, custom_url: custom });
    await fetchRedirects();
  };

  const handleDelete = async (redirUrl: string) => {
    await deleteRedirect(redirUrl);
    setRedirects((prev) => prev.filter((r) => r.redir_url !== redirUrl));
  };

  return (
    <div className="flex-1 max-w-4xl mx-auto w-full px-4 sm:px-6 py-8">
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <Link2 size={24} className="text-primary" />
          <h1 className="text-2xl font-bold">Dashboard</h1>
        </div>
        <p className="text-text-muted text-sm">
          Create and manage your short URLs
        </p>
      </div>

      <div className="mb-8">
        <AddRedirect onAdd={handleAdd} />
      </div>

      {loading ? (
        <div className="flex justify-center py-16">
          <div className="w-8 h-8 border-2 border-primary border-t-transparent rounded-full animate-spin" />
        </div>
      ) : error ? (
        <div className="text-center py-16">
          <p className="text-danger text-sm">{error}</p>
          <button
            onClick={() => {
              setLoading(true);
              setError("");
              fetchRedirects();
            }}
            className="mt-3 text-primary text-sm hover:text-primary-hover transition-colors cursor-pointer"
          >
            Try again
          </button>
        </div>
      ) : redirects.length === 0 ? (
        <div className="text-center py-16 animate-fade-in">
          <div className="w-16 h-16 rounded-2xl bg-white/5 flex items-center justify-center mx-auto mb-4">
            <Inbox size={32} className="text-text-dim" />
          </div>
          <p className="text-text-muted text-sm">
            No redirects yet. Paste a URL above to get started.
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          <div className="flex items-center justify-between mb-2">
            <span className="text-text-dim text-xs font-medium uppercase tracking-wider">
              {redirects.length} redirect{redirects.length !== 1 ? "s" : ""}
            </span>
          </div>
          {redirects.map((r) => (
            <RedirectCard
              key={r.redir_url}
              redirect={r}
              onDelete={handleDelete}
            />
          ))}
        </div>
      )}
    </div>
  );
}
