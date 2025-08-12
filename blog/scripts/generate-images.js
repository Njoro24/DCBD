// scripts/generate-images.js
import fs from 'fs-extra';
import path from 'path';
import matter from 'gray-matter';
import glob from 'glob';
import axios from 'axios';
import { v4 as uuidv4 } from 'uuid';

const OPENAI_KEY = process.env.OPENAI_API_KEY;
const CLOUD_NAME = process.env.CLOUDINARY_CLOUD;
const CLOUD_PRESET = process.env.CLOUDINARY_UPLOAD_PRESET;

if (!OPENAI_KEY || !CLOUD_NAME || !CLOUD_PRESET) {
  console.error('Missing required env vars, aborting.');
  process.exit(1);
}

const contentDir = path.join(process.cwd(), 'content');

function promptFor(title) {
  return `Ghibli-inspired, hand-painted, warm pastel palette, cinematic soft light, whimsical scene, quiet domestic clinic vignette, high detail, wide aspect 16:9, no text, subject: "${title}", calm, roomy composition.`;
}

async function generateImage(prompt) {
  const url = 'https://api.openai.com/v1/images/generations';
  const payload = {
    prompt,
    n: 1,
    size: '1024x576'
  };
  const res = await axios.post(url, payload, {
    headers: {
      'Authorization': `Bearer ${OPENAI_KEY}`,
      'Content-Type': 'application/json'
    }
  });
  if (!res.data || !res.data.data || !res.data.data[0] || !res.data.data[0].b64_json) {
    throw new Error('No image returned from OpenAI');
  }
  const b64 = res.data.data[0].b64_json;
  const buffer = Buffer.from(b64, 'base64');
  return buffer;
}

async function uploadToCloudinary(buffer, publicId) {
  const form = new URLSearchParams();
  form.append('file', `data:image/png;base64,${buffer.toString('base64')}`);
  form.append('upload_preset', CLOUD_PRESET);
  form.append('public_id', publicId);

  const cloudUrl = `https://api.cloudinary.com/v1_1/${CLOUD_NAME}/image/upload`;
  const res = await axios.post(cloudUrl, form.toString(), {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
  });
  return res.data.secure_url;
}

async function processFile(filePath) {
  const raw = await fs.readFile(filePath, 'utf8');
  const parsed = matter(raw);
  const fm = parsed.data;
  if (fm.generate_image && (!fm.image || fm.image === null)) {
    console.log('Generating image for', filePath);
    const prompt = promptFor(fm.title || path.basename(filePath));
    const imgBuffer = await generateImage(prompt);
    const publicId = `blog/${path.basename(filePath, '.md')}-${uuidv4().slice(0,8)}`;
    const url = await uploadToCloudinary(imgBuffer, publicId);
    fm.image = url;
    const newMd = matter.stringify(parsed.content, fm);
    await fs.writeFile(filePath, newMd, 'utf8');
    console.log('Updated', filePath, 'with', url);
  } else {
    console.log('Skipping', filePath);
  }
}

async function run() {
  const files = glob.sync(path.join(contentDir, '*.md'));
  for (const f of files) {
    try {
      await processFile(f);
    } catch (err) {
      console.error('Error processing', f, err.message || err);
    }
  }
}

run();
