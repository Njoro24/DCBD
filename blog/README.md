# HeyNia Blog - SvelteKit starter

## workflow
1. Push markdown to `content/` with frontmatter `generate_image: true` and `image: null`.
2. GitHub Action runs on push, generates hero images via OpenAI, uploads to Cloudinary, updates post frontmatter with `image`.
3. Vercel builds and serves the blog at your domain.

## required secrets (GitHub repo settings)
- OPENAI_API_KEY
- CLOUDINARY_CLOUD
- CLOUDINARY_UPLOAD_PRESET
- CLOUDINARY_API_KEY
- CLOUDINARY_API_SECRET

## local testing
- Copy env vars into `.env`
- `npm install`
- `npm run generate-images` to run locally

Deploy to Vercel after push, set environment variables in Vercel for runtime.
