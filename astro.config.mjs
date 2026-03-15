import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://greenway-website.netlify.app',
  output: 'static',
  build: {
    inlineStylesheets: 'auto'
  },
  vite: {
    build: {
      cssMinify: true
    }
  }
});
