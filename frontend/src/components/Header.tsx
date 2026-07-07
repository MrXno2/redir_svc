import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { LogOut, Link2 } from "lucide-react";

export function Header() {
  const { isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <header className="glass border-b border-border sticky top-0 z-40">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
        <Link
          to={isAuthenticated ? "/dashboard" : "/login"}
          className="flex items-center gap-2.5 group"
        >
          <div className="w-9 h-9 rounded-lg bg-primary/15 flex items-center justify-center group-hover:bg-primary/25 transition-colors">
            <Link2 size={20} className="text-primary" />
          </div>
          <span className="text-lg font-bold tracking-tight">
            redir<span className="text-primary">.</span>svc
          </span>
        </Link>

        {isAuthenticated && (
          <button
            onClick={handleLogout}
            className="flex items-center gap-2 px-3 py-1.5 text-sm text-text-muted hover:text-text rounded-lg hover:bg-white/5 transition-all cursor-pointer"
          >
            <LogOut size={16} />
            <span className="hidden sm:inline">Logout</span>
          </button>
        )}
      </div>
    </header>
  );
}
