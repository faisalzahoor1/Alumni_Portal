/** @type {import('next').NextConfig} */
const nextConfig = {
  // FastAPI routes like /alumni/profile/ need their trailing slash preserved
  skipTrailingSlashRedirect: true,
  images: { unoptimized: true },
  // Hide the Next.js dev-tools badge (the "N" in the corner) while developing
  devIndicators: false,
};

export default nextConfig;
