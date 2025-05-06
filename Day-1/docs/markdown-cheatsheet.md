# 📘 Markdown Cheatsheet

This cheatsheet is your quick reference to Markdown syntax. It helps you write clean, readable, and portable documentation across README files, wikis, and MkDocs sites.

---

## 🧱 Headings

Use `#` for headings (1–6 levels):

```markdown
# H1 - Title
## H2 - Section
### H3 - Subsection
#### H4
##### H5
###### H6

## 📌 Lists

Unordered List:

```markdown
- Item 1
- Item 2
  - Sub-item
    - Sub-sub-item

Ordered List:

```markdown
1. First
2. Second
3. Third

## 🔗 Links

```markdown
[Link Text](https://example.com)

## 🖼️ Images

```markdown
![Alt text](https://via.placeholder.com/150)


## 🧾 Code Blocks

Inline Code:
Use backticks: `code` → code

Multiline Code Block:
<pre> ```python def hello(): print("Hello Markdown!") ``` </pre>

## 📋 Blockquotes

```markdown
> This is a blockquote.
>> Nested blockquote.

## 📊 Tables

```markdown
| Feature     | Supported |
|------------|-----------|
| Headings   | ✅        |
| Lists      | ✅        |
| Tables     | ✅        |

## 🎯 Task Lists

```markdown
- [x] Write Markdown Cheatsheet
- [ ] Finish README
- [ ] Publish MkDocs site

## 🧪 Horizontal Rule

```markdown
---

## ⌨️ Inline Formatting

Bold: **bold** → bold
Italic: *italic* → italic
Strikethrough: ~~strikethrough~~ → strikethrough


## 🛠️ Embedding Mermaid Diagrams

<pre> ```mermaid sequenceDiagram participant User participant Frontend participant Backend participant DB User->>Frontend: Login Request Frontend->>Backend: API Call Backend->>DB: Verify User DB-->>Backend: Result Backend-->>Frontend: Response Frontend-->>User: Logged In ``` </pre>
