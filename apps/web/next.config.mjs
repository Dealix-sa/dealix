/** @type {import('next').NextConfig} */
const nextConfig = {
  // Typed routes intentionally disabled: the Founder Console builds
  // navigation links dynamically from a runtime list of section paths,
  // which is incompatible with statically-typed Link href values.
  experimental: {
    typedRoutes: false,
  },
};

export default nextConfig;
