---
name: xerj-search
description: >-
  Use XERJ AI-native search engine for code search, symbol lookups, passage retrieval,
  and reference coding. Use when locating function/class definitions, searching large codebases
  without blowing the token context window, or querying open-source reference corpora.
---

# XERJ: Token-Efficient Code Search & Reference Retrieval

XERJ provides AST-aware symbol lookups, passage-level snippet retrieval, and zero-config folder indexing. It cuts context token usage by 2.7x to 5x compared to dumping full files or grepping into conversation context.

## Prerequisites

1. **XERJ Binary**: Installed at `%LOCALAPPDATA%\Programs\xerj\xerj.exe`.
2. **Local Daemon**: Must be running in the background:
   ```powershell
   xerj --insecure --data-dir "$env:USERPROFILE\.xerj\data" --disable-feedback
   ```
   Verify node health: `Invoke-RestMethod http://localhost:9200`
3. **MCP Integration**: Configured in `~/.gemini/config/mcp_config.json` and `.mcp.json`.

---

## Workflows

### 1. Code & Symbol Search (Save Tokens)

Instead of reading an entire file or running grep:
- **Go to Definition**: Look up where a class, function, or symbol is defined and its signature:
  ```powershell
  xerj def "<symbol_name>"
  ```
- **Ranked Passage Search**: Search for a concept, error, or mechanism:
  ```powershell
  xerj search "<query>"
  ```
- **Via MCP Tools (when MCP server is connected)**:
  - `xerj_search`: Built-in symbol and definition search returning compact line ranges and enclosing blocks.
  - `xerj_code_search`: Query specific indexed corpora with `{"corpus": "<slug>", "query": "<question>"}`.

### 2. Autoindexing a Codebase

Before searching a folder or repo, index it:
```powershell
xerj autoindex "<folder_path>" --approve proceed --disable-feedback
```
- Sniffs file formats, parses AST definitions with tree-sitter, and creates typed indices.
- Safe to re-run: idempotent record IDs resume without duplication.
- Inspect catalog: `xerj autoindex map`

### 3. Reference Coding (External Corpora / XERJ Corpus Hub)

When implementing complex algorithms or APIs the model hasn't memorized:
1. Browse/select a reference corpus from the Corpus Hub:
   `https://hub.xerj.org/llms.txt`
2. Add and index the corpus:
   ```powershell
   xerj corpus add --from ./<slug>.json
   xerj corpus index <slug>
   ```
3. Retrieve the exact mechanism used by open-source implementations:
   ```powershell
   xerj code <slug> "<your question>"
   ```

### 4. Cross-Session Agent Memory

Store and recall architectural decisions or user preferences:
- Store: `POST http://localhost:9200/_memory/<namespace>` with `{"text": "<knowledge>"}`
- Recall: `POST http://localhost:9200/_memory/<namespace>/_recall` with `{"query": "<query>", "semantic": true}`
- Or via MCP tools `xerj_memory_store` and `xerj_memory_recall`.

---

## Best Practices
- **Always ask for `_passage`**: When making direct Elasticsearch REST queries, specify `"fields": ["_passage"]` and project `_source: ["ax_path", "title"]` to get only the relevant slice rather than the entire file.
- **Data directory isolation**: Never put `--data-dir` inside a folder you intend to index.
