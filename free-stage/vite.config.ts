import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'node:path'

// https://vitejs.dev/config/
export default defineConfig({
  build: {
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
        display: resolve(__dirname, 'src/pages/display/index.html')
      }
    }
  },
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    proxy: {
      // Use a wildcard pattern for a catch-all
      '/api': {
        target: 'http://localhost:80/api/',
        changeOrigin: true, // needed for virtual hosted sites
        // rewrite: (path) => path.replace(/^\/api/, '')
      },
      '/content': {
        target: 'http://localhost:80/content/',
        changeOrigin: true, // needed for virtual hosted sites
        rewrite: (path) => path.replace(/^\/content/, '')
      }
    }
  }
})
