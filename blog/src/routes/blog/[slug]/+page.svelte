<script lang="ts">
  import { getPostBySlug } from '$lib/posts';
  export let params;
  const post = getPostBySlug(params.slug);
</script>

<svelte:head>
  <title>{post.data.title}</title>
  <meta name="description" content={post.data.summary} />
</svelte:head>

<style>
  @import '../../app.css';
</style>

<article class="post">
  <header>
    <h1>{post.data.title}</h1>
    <p class="meta">{post.data.date} — {post.data.author}</p>
    {#if post.data.image}
      <img src={post.data.image} alt={post.data.title} class="hero" />
    {/if}
  </header>

  <section class="content">
    {@html post.content}
  </section>
</article>
