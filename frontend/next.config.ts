import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Enable React strict mode for catching potential issues
  reactStrictMode: true,

  // Image optimization
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "avatars.githubusercontent.com",
      },
      {
        protocol: "https",
        hostname: "lh3.googleusercontent.com",
      },
    ],
  },

  // API proxy to FastAPI backend (avoids CORS in dev)
  async rewrites() {
    return [
      {
        source: "/api/backend/:path*",
        destination: `${process.env.NEXT_PUBLIC_API_URL || "http://backend:8000"}/:path*`,
      },
    ];
  },

  // Security headers
  async headers() {
    return [
      {
        source: "/(.*)",
        headers: [
          { key: "X-Frame-Options", value: "DENY" },
          { key: "X-Content-Type-Options", value: "nosniff" },
          { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
          {
            key: "Permissions-Policy",
            value: "camera=(), microphone=(), geolocation=()",
          },
        ],
      },
    ];
  },

  // Optimize bundle
  experimental: {
    optimizePackageImports: ["lucide-react", "recharts"],
  },
};

export default nextConfig;
