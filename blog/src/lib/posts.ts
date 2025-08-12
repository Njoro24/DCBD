import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';

const contentDir = path.join(process.cwd(), 'content');

export function getAllPosts() {
  const files = fs.readdirSync(contentDir).filter(Boolean);
  const posts = files.map((file) => {
    const raw = fs.readFileSync(path.join(contentDir, file), 'utf-8');
    const { data, content } = matter(raw);
    const slug = file.replace(/\.md$/, '');
    return {
      slug, data, content
    };
  }).sort((a, b) => new Date(b.data.date).getTime() - new Date(a.data.date).getTime());
  return posts;
}

export function getPostBySlug(slug) {
  const raw = fs.readFileSync(path.join(contentDir, `${slug}.md`), 'utf-8');
  const { data, content } = matter(raw);
  return { slug, data, content };
}
