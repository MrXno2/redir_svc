import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { parseApiError } from "../api/axios";
import { LogIn } from "lucide-react";

export function LoginPage() {
  const [login, setLogin] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { login: authLogin } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await authLogin(login, password);
      navigate("/dashboard");
    } catch (err) {
      setError(parseApiError(err));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex-1 flex items-center justify-center px-4 py-12">
      <div className="w-full max-w-md animate-fade-in">
        <div className="text-center mb-8">
          <div className="w-14 h-14 rounded-2xl bg-primary/15 flex items-center justify-center mx-auto mb-4">
            <LogIn size={28} className="text-primary" />
          </div>
          <h1 className="text-2xl font-bold">Welcome back</h1>
          <p className="text-text-muted text-sm mt-1">
            Sign in to manage your redirects
          </p>
        </div>

        <div className="bg-bg-card border border-border rounded-2xl p-6">
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <div className="p-3 rounded-xl text-sm animate-fade-in" style={{ background: "rgba(239, 68, 68, 0.1)", border: "1px solid rgba(239, 68, 68, 0.2)", color: "#fca5a5" }}>
                {error}
              </div>
            )}

            <div>
              <label className="block text-sm font-medium text-text-muted mb-1.5">
                Login
              </label>
              <input
                type="text"
                value={login}
                onChange={(e) => setLogin(e.target.value)}
                placeholder="Enter your login"
                required
                minLength={4}
                className="w-full px-4 py-3 bg-bg-input border border-border rounded-xl text-text placeholder:text-text-dim focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary/30 transition-all text-sm"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-text-muted mb-1.5">
                Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter your password"
                required
                minLength={6}
                className="w-full px-4 py-3 bg-bg-input border border-border rounded-xl text-text placeholder:text-text-dim focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary/30 transition-all text-sm"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 bg-primary hover:bg-primary-hover disabled:opacity-50 disabled:cursor-not-allowed text-white font-medium rounded-xl transition-all flex items-center justify-center gap-2 text-sm cursor-pointer"
            >
              {loading ? (
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
              ) : (
                "Sign in"
              )}
            </button>
          </form>

          <div className="mt-6 text-center">
            <span className="text-text-dim text-sm">
              Don't have an account?{" "}
            </span>
            <Link
              to="/register"
              className="text-primary hover:text-primary-hover text-sm font-medium transition-colors"
            >
              Sign up
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
