/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        bg: {
          DEFAULT: "#0a0a0f",
          card: "#12121a",
          "card-hover": "#1a1a25",
          input: "#16161f",
        },
        border: {
          DEFAULT: "#2a2a3a",
          focus: "#6366f1",
        },
        primary: {
          DEFAULT: "#6366f1",
          hover: "#818cf8",
          glow: "rgba(99, 102, 241, 0.15)",
        },
        danger: {
          DEFAULT: "#ef4444",
          hover: "#f87171",
        },
        success: "#22c55e",
        warning: "#f59e0b",
        text: {
          DEFAULT: "#e2e8f0",
          muted: "#94a3b8",
          dim: "#64748b",
        },
      },
      fontFamily: {
        sans: [
          "Inter",
          "-apple-system",
          "BlinkMacSystemFont",
          "Segoe UI",
          "sans-serif",
        ],
      },
      animation: {
        "fade-in": "fadeIn 0.3s ease-out",
        "slide-in": "slideIn 0.3s ease-out",
      },
      keyframes: {
        fadeIn: {
          "0%": { opacity: "0", transform: "translateY(8px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        slideIn: {
          "0%": { opacity: "0", transform: "translateX(16px)" },
          "100%": { opacity: "1", transform: "translateX(0)" },
        },
      },
    },
  },
  plugins: [],
};
