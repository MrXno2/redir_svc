import { useState } from "react";
import { Copy, ExternalLink, Trash2, BarChart3 } from "lucide-react";
import type { RedirResponse } from "../types";
import { toast } from "./Toast";

interface Props {
  redirect: RedirResponse;
  onDelete: (url: string) => Promise<void>;
}

export function RedirectCard({ redirect, onDelete }: Props) {
  const [deleting, setDeleting] = useState(false);
  const [copied, setCopied] = useState(false);

  const shortUrl = `${window.location.origin}/go/${redirect.redir_url}`;

  const handleCopy = async () => {
    await navigator.clipboard.writeText(shortUrl);
    setCopied(true);
    toast.success("Copied to clipboard");
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDelete = async () => {
    setDeleting(true);
    try {
      await onDelete(redirect.redir_url);
      toast.success("Redirect deleted");
    } catch {
      toast.error("Failed to delete redirect");
    } finally {
      setDeleting(false);
    }
  };

  return (
    <div className="group bg-bg-card border border-border rounded-xl p-4 hover:border-primary/30 hover:bg-bg-card-hover transition-all duration-200 animate-fade-in">
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0 flex-1">
          <div className="flex items-center gap-2 mb-1.5">
            <span className="text-primary font-mono text-sm font-semibold">
              /go/{redirect.redir_url}
            </span>
          </div>
          <a
            href={redirect.default_url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-text-muted text-sm hover:text-primary transition-colors flex items-center gap-1 truncate"
          >
            {redirect.default_url}
            <ExternalLink size={12} className="shrink-0 opacity-0 group-hover:opacity-100 transition-opacity" />
          </a>
        </div>

        <div className="flex items-center gap-1.5 shrink-0">
          <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-white/5 text-text-dim text-xs">
            <BarChart3 size={12} />
            <span className="font-mono">{redirect.redir_count}</span>
          </div>

          <button
            onClick={handleCopy}
            className="p-2 rounded-lg text-text-dim hover:text-primary hover:bg-primary/10 transition-all cursor-pointer"
            title="Copy short URL"
          >
            <Copy size={15} className={copied ? "text-success" : ""} style={copied ? { color: "#22c55e" } : {}} />
          </button>

          <button
            onClick={handleDelete}
            disabled={deleting}
            className="p-2 rounded-lg text-text-dim hover:text-danger hover:bg-danger/10 transition-all cursor-pointer disabled:opacity-50"
            title="Delete redirect"
          >
            {deleting ? (
              <div className="w-3.5 h-3.5 border-2 border-danger border-t-transparent rounded-full animate-spin" />
            ) : (
              <Trash2 size={15} />
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
