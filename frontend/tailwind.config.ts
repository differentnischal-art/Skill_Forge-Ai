import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        graphite: "#15171B",
        surface: "#1D2026",
        surfaceRaised: "#252932",
        border: "#2E323C",
        ink: "#E8E6E1",
        muted: "#8B8F99",
        ember: "#E8703A",
        emberDim: "#B85A2E",
        good: "#6FAE8C",
        warn: "#D9A441",
      },
      fontFamily: {
        display: ["var(--font-display)", "sans-serif"],
        body: ["var(--font-body)", "sans-serif"],
        mono: ["var(--font-mono)", "monospace"],
      },
    },
  },
  plugins: [],
};
export default config;