---
Date: 2026-04-02 18:15
Type: Page
Title: Landing Page Template
Location: /_templates/landing-page
---

<!DOCTYPE html>
<html lang="en">
<head>
<title>{weblog-title}</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{feeds}
<link rel="stylesheet" href="/responsive-layout.css">
<link rel="stylesheet" href="/prism.css">
<link rel="stylesheet" href="/blade-runner-theme.css">
<style>
@import url('https://static.omg.lol/type/font-honey.css');
@import url('https://static.omg.lol/type/font-lato-regular.css');
@import url('https://static.omg.lol/type/font-lato-bold.css');
@import url('https://static.omg.lol/type/font-lato-italic.css');
@import url('https://static.omg.lol/type/font-md-io.css');
@import url('https://static.omg.lol/type/fontawesome-free/css/all.css');

* { box-sizing: border-box; }
body {
  font-family: 'Lato', sans-serif;
  font-size: 120%;
  color: var(--foreground);
  background: var(--background);
}
header nav ul { list-style-type: none; margin: 0; padding: 0; }
header nav li { display: inline-block; }
header nav li a { display: block; text-decoration: none; margin-right: 1em; }
h1, h2, h3, h4, h5, h6 { font-family: 'VC Honey Deck', serif; margin: 1rem 0; }
p, li { line-height: 160%; }
header, main, footer { max-width: 60em; margin: 2em auto; padding: 0 1em; }
header { margin-top: 4em; }
footer p { margin-top: 5em; font-size: 90%; text-align: center; }
a:link, a:visited, a:hover, a:active { color: var(--link); }
.post-info, .post-tags { font-size: 85%; color: var(--accent); text-align: right; }
.post-info i:nth-child(2) { margin-left: .75em; }
.weblog-title a { text-decoration: none; color: var(--foreground); }
.post-list { list-style: none; margin: 2rem 0 0; padding: 0; }
.post-preview { margin-bottom: 2.5rem; padding-bottom: 2rem; border-bottom: 1px solid var(--accent); }
.post-preview h3 { margin-bottom: .75rem; }
.post-preview h3 a, .post-link { text-decoration: none; }
.post-meta { display: flex; gap: 1rem; justify-content: space-between; align-items: center; flex-wrap: wrap; }
.post-meta .post-info { text-align: left; }
</style>
</head>
<body>
<script src="/prism.js"></script>
<script type="module">
import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
mermaid.initialize({ startOnLoad: false, theme: 'dark' });
await mermaid.run({ querySelector: '.language-mermaid' });
</script>
<div class="content-page">
  <header>
    <h1 class="weblog-title"><a href="{base-path}">{weblog-title}</a></h1>
    {navigation}
  </header>
  <main>
    <h2>Latest posts</h2>
    {post-list}
  </main>
  <footer>
    <p>Made with <a href="https://weblog.lol">weblog.lol</a>.</p>
  </footer>
</div>
</body>
</html>
