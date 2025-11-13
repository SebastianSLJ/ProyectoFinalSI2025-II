import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'
import tailwindcss from "@tailwindcss/vite"
import { resolve } from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    tailwindcss(),
    react(),
  ],
  resolve: {
    alias: {
      // allow imports like 'components/Foo' -> src/components/Foo
      components: resolve(__dirname, 'src/components'),
      pages: resolve(__dirname, 'src/Pages'),
      assets: resolve(__dirname, 'src/assets'),
      '@': resolve(__dirname, 'src')
    }
  }
})
