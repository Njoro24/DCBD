<script lang="ts">
  import { getAllPosts } from '$lib/posts';
  const posts = getAllPosts();
</script>

<svelte:head>
  <title>HeyNia Blog</title>
  <meta name="description" content="HeyNia blog for dental practice systems and operations" />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap" rel="stylesheet" />
</svelte:head>

<style>
  @import '../app.css';
</style>

<main class="container">
  <header class="hero">
    <h1>HeyNia Blog</h1>
    <p class="sub">Systems-first insights for solo dentists</p>
  </header>

  <section class="grid">
    {#each posts as post}
      <article class="card">
        <a href={`/blog/${post.slug}`}>
          {#if post.data.image}
            <img src={post.data.image} alt={post.data.title} class="thumb" />
          {:else}
            <div class="thumb placeholder"></div>
          {/if}
          <h3>{post.data.title}</h3>
          <p class="muted">{post.data.summary}</p>
        </a>
      </article>
    {/each}
  </section>
</main>
