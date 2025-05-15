# Daily Learning Log

This document serves as a daily journal to track what I've learned and what confused me during my work on this project. The goal is to reflect on my progress, identify areas needing more attention, and foster a better understanding over time.

---

## [05-05-2025]

### What I Learned Today:

* Markdown Cheatsheet Writing – I practiced creating a detailed Markdown cheatsheet with all key elements: headings, bold/italic, inline and block code, tables, lists, links, images, and blockquotes. This helped me reinforce my Markdown fluency.

* Mermaid.js Sequence Diagrams – I learned how to embed a Mermaid.js sequence diagram directly in Markdown, showing interactions between user, frontend, backend, and database for a login flow. I figured out how to represent both synchronous (-->) and asynchronous (-->>) calls.

* MkDocs + Material Setup – I successfully installed MkDocs and the Material theme, created a basic mkdocs.yml, added navigation, and ran mkdocs serve. I confirmed that Mermaid diagrams render nicely and that the built-in search works.

### What Confused Me Today:

* Embedding Draw.io Diagrams in Markdown – I wasn’t sure about the best way to embed Draw.io (exported as SVG or PNG) into Markdown so it renders correctly on both GitHub and MkDocs. Should I use relative paths or absolute URLs? I’ll test both.

* Organizing Large Documentation Projects – I’m a bit unclear on how to split a large system’s documentation into separate Markdown files and how to structure them cleanly in the docs/ folder for MkDocs. Should each component get its own page? How granular should it be?

* Combining Mermaid and Draw.io Diagrams – I wonder whether it’s better to use one diagramming tool consistently or mix Mermaid (for flows) and Draw.io (for architecture) in the same documentation set. Will mixing confuse readers or enrich clarity?

---

## [06-05-2025]

### What I Learned Today:

* Learned to set up Python projects as libraries, CLI tools, and notebooks.  
* Used Typer to build simple and clean CLI interfaces.  
* Understood managing configs with YAML, env vars, and defaults.  
* Practiced Pythonic patterns like EAFP vs LBYL and generator expressions.  
* Refreshed function design: *args, **kwargs, positional-only, keyword-only.

### What Confused Me Today:

* Exact flow of config resolution (local vs env vs defaults).  
* How `.send()` works with generators and when to apply it.  
* Memory differences between list comprehensions vs generators.