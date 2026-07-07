import { useEffect, useState } from "react";
import { X, CheckCircle, AlertCircle } from "lucide-react";

export interface Toast {
  id: number;
  message: string;
  type: "success" | "error";
}

let toastId = 0;
let listeners: Array<(toasts: Toast[]) => void> = [];
let toastsState: Toast[] = [];

function notify(newToast: Omit<Toast, "id">) {
  const id = ++toastId;
  const toast = { ...newToast, id };
  toastsState = [...toastsState, toast];
  listeners.forEach((l) => l(toastsState));

  setTimeout(() => {
    toastsState = toastsState.filter((t) => t.id !== id);
    listeners.forEach((l) => l(toastsState));
  }, 4000);
}

export const toast = {
  success: (message: string) => notify({ message, type: "success" }),
  error: (message: string) => notify({ message, type: "error" }),
};

export function ToastContainer() {
  const [toasts, setToasts] = useState<Toast[]>([]);

  useEffect(() => {
    listeners.push(setToasts);
    return () => {
      listeners = listeners.filter((l) => l !== setToasts);
    };
  }, []);

  if (toasts.length === 0) return null;

  return (
    <div className="fixed bottom-6 right-6 z-50 flex flex-col gap-3">
      {toasts.map((t) => (
        <div
          key={t.id}
          className={`animate-slide-in flex items-center gap-3 px-4 py-3 rounded-xl glass shadow-lg max-w-sm ${
            t.type === "success"
              ? "border-success/30"
              : "border-danger/30"
          }`}
          style={{
            borderColor:
              t.type === "success"
                ? "rgba(34, 197, 94, 0.3)"
                : "rgba(239, 68, 68, 0.3)",
          }}
        >
          {t.type === "success" ? (
            <CheckCircle size={18} className="text-success shrink-0" style={{ color: "#22c55e" }} />
          ) : (
            <AlertCircle size={18} className="text-danger shrink-0" style={{ color: "#ef4444" }} />
          )}
          <span className="text-sm text-text">{t.message}</span>
          <button
            onClick={() => {
              toastsState = toastsState.filter((x) => x.id !== t.id);
              setToasts(toastsState);
            }}
            className="ml-2 text-text-dim hover:text-text transition-colors shrink-0"
          >
            <X size={14} />
          </button>
        </div>
      ))}
    </div>
  );
}
