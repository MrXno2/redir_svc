import { useState } from "react";
import { Link2, Sparkles, Plus } from "lucide-react";
import { toast } from "./Toast";
import { parseApiError } from "../api/axios";

interface Props {
  onAdd: (url: string, custom: string) => Promise<void>;
}

export function AddRedirect({ onAdd }: Props) {
  const [url, setUrl] = useState("");
  const [custom, setCustom] = useState("");
  const [loading, setLoading] = useState(false);
  const [expanded, setExpanded] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!url.trim()) return;

    setLoading(true);
    try {
      await onAdd(url.trim(), custom.trim() || "default");
      toast.success("Redirect created");
      setUrl("");
      setCustom("");
      setExpanded(false);
    } catch (err) {
      toast.error(parseApiError(err));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-bg-card border border-border rounded-2xl p-5 glow-border">
      <form onSubmit={handleSubmit}>
        <div className="flex gap-3">
          <div className="relative flex-1">
            <Link2
              size={16}
              className="absolute left-3 top-1/2 -translate-y-1/2 text-text-dim"
            />
            <input
              type="text"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="Paste your URL here..."
              className="w-full pl-10 pr-4 py-3 bg-bg-input border border-border rounded-xl text-text placeholder:text-text-dim focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary/30 transition-all text-sm"
            />
          </div>
          <button
            type="submit"
            disabled={loading || !url.trim()}
            className="px-5 py-3 bg-primary hover:bg-primary-hover disabled:opacity-50 disabled:cursor-not-allowed text-white font-medium rounded-xl transition-all flex items-center gap-2 text-sm cursor-pointer"
          >
            {loading ? (
              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
            ) : (
              <>
                <Plus size={16} />
                <span className="hidden sm:inline">Shorten</span>
              </>
            )}
          </button>
        </div>

        <button
          type="button"
          onClick={() => setExpanded(!expanded)}
          className="mt-3 flex items-center gap-1.5 text-xs text-text-dim hover:text-primary transition-colors cursor-pointer"
        >
          <Sparkles size={12} />
          {expanded ? "Hide" : "Custom alias"}
        </button>

        {expanded && (
          <div className="mt-3 animate-fade-in">
            <input
              type="text"
              value={custom}
              onChange={(e) => setCustom(e.target.value)}
              placeholder="Custom alias (leave empty for random)"
              className="w-full px-4 py-2.5 bg-bg-input border border-border rounded-xl text-text placeholder:text-text-dim focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary/30 transition-all text-sm"
            />
          </div>
        )}
      </form>
    </div>
  );
}
