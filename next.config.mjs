/** @type {import('next').NextConfig} */
const nextConfig = {
  typescript: {
    ignoreBuildErrors: true,
  },
  images: {
    unoptimized: true,
  },
  output: "standalone",
  turbopack: {
    resolveAlias: {
      'next-mdx-import-source-file': [
        './mdx-components.tsx',
        './mdx-components.ts',
        './mdx-components.js',
      ],
    },
  },
}

import nextra from 'nextra'

const withNextra = nextra({
})

export default withNextra(nextConfig)
