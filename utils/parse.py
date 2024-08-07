extraction_rules = """
Extract the main content from the provided HTML document. The main content typically includes the primary text of the article, blog post, or main textual content. Follow these guidelines:

1. **Focus on main content selectors:**
   Concentrate on tags and attributes that are likely to contain the main content, such as:
   - <main>
   - <article>
   - <div> elements with class names like "content", "main-content", "article-body", etc.

2. **Exclude non-essential elements:** 
   Ignore elements that are likely to contain ads, navigation menus, sidebars, footers, headers, pop-ups, or other non-essential content. Typically, these might include:
   - <nav>
   - <footer>
   - <header>
   - <aside>
   - <div> elements with class names like "ad", "sidebar", "popup", "footer", etc.

3. **Handle nested content elements:**
   Ensure that nested content elements within the main content are also considered. For instance, if a <div class="article-body"> contains a nested <section>, the content of the <section> should also be included.

4. **Preserve text formatting:**
   If possible, preserve the text formatting tags within the main content, such as <p>, <h1>, <h2>, <h3>, <ul>, <ol>, and <li>.

5. **Ignore script and style tags:**
   Do not include content from <script> or <style> tags.

Example:

Given the HTML:

<!DOCTYPE html>
<html>
<head>
  <title>Sample Article</title>
  <style>
    .ad { display:none; }
  </style>
</head>
<body>
  <header>Site Header</header>
  <nav>Main Navigation</nav>
  <aside>Sidebar Content</aside>
  <main>
    <article>
      <h1>Title of the Article</h1>
      <p>This is the first paragraph of the main content.</p>
      <p>This is the second paragraph of the main content.</p>
    </article>
  </main>
  <div class="ad">Advertisement</div>
  <footer>Site Footer</footer>
</body>
</html>

The expected output:

<main>
  <article>
    <h1>Title of the Article</h1>
    <p>This is the first paragraph of the main content.</p>
    <p>This is the second paragraph of the main content.</p>
  </article>
</main>
"""
