import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  poweredByHeader: false,
  async rewrites() {
    const backend = process.env.API_INTERNAL_URL ?? "http://127.0.0.1:8000";
    return [
      {
        source: "/backend/:path*",
        destination: `${backend}/:path*`,
      },
    ];
  },
};

export default nextConfig;
