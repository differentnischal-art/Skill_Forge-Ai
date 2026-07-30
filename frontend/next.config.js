/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [{ protocol: "https", hostname: "avatars.githubusercontent.com" }],
  },
  allowedDevOrigins: ["20.101.38.162"],
};

module.exports = nextConfig;