import adapter from '@sveltejs/adapter-auto';
import { mdsvex } from 'mdsvex';

export default {
  extensions: ['.svelte', '.svx', '.md'],
  preprocess: [mdsvex({ extension: '.md' })],
  kit: {
    adapter: adapter(),
    alias: {
      $lib: './src/lib'
    }
  }
};
