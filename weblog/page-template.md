---
Date: 2026-04-02 18:15
Type: Page
Title: Page Template
Location: /_templates/page
---

<!DOCTYPE html>
<html lang="en">
<head>
<title>{weblog-title}{separator}{post-title}</title>
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
.weblog-title a { text-decoration: none; color: var(--foreground); }
</style>
</head>
<body>
<div class="content-page">
  <header>
    <h1 class="weblog-title"><a href="{base-path}">{weblog-title}</a></h1>
    {navigation}
  </header>
  <main>{body}</main>
  <footer>
    <p>Made with <a href="https://weblog.lol">weblog.lol</a>.</p>
  </footer>
</div>
</body>
</html>
