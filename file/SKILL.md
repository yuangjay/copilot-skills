---
name: file
description: 'File operations skill. Use when creating, reading, editing, moving, deleting, or organizing files and directories. Triggers on: create file, write file, update file, delete file, rename file, move file, copy file, find file, list files, organize directory, file structure, read file contents, overwrite file, append to file, batch file operations.'
argument-hint: 'Describe the file operation (e.g. "create a config file", "find all Python files", "reorganize src/")'
---

# File Operations

## When to Use

Invoke this skill for any task involving the file system:
- Creating or writing new files with specific content
- Reading or viewing existing file contents
- Editing, updating, or overwriting existing files
- Renaming, moving, or copying files and directories
- Deleting files or directories (with confirmation for destructive ops)
- Finding files by name pattern or content
- Listing and exploring directory structures
- Batch file operations across multiple files

## Procedures

### Creating a File

1. Confirm the target path (absolute or workspace-relative).
2. Check if the file already exists — warn before overwriting.
3. Write the content using the `create_file` tool.
4. Verify the file was created with a follow-up read or directory listing.

### Editing an Existing File

1. **Read first**: Always read the file before editing to understand context.
2. Use `replace_string_in_file` for targeted edits (include 3–5 lines of context around the change).
3. Use `multi_replace_string_in_file` when making multiple independent changes at once.
4. After editing, validate the result (re-read the changed section or check for errors).

### Finding Files

1. Use `file_search` with a glob pattern when you know the filename pattern (e.g. `**/*.json`).
2. Use `grep_search` when searching by file content or a string inside files.
3. Use `list_dir` to explore a specific directory's contents.
4. Combine glob + grep for pattern-based content searches across matched files.

### Moving / Renaming Files

1. Use the terminal with `mv <source> <destination>` (reversible within the workspace).
2. For renames that affect imports or references, search for all usages first.
3. Confirm with the user before moving files outside the workspace.

### Deleting Files

> **Requires confirmation** — deletion is not easily reversible.

1. List the files to be deleted and present them to the user for review.
2. Use `rm` (file) or `rm -rf` (directory) ONLY after explicit user confirmation.
3. Prefer moving to a backup location over permanent deletion when in doubt.

### Organizing a Directory

1. Use `list_dir` to audit the current structure.
2. Propose a new structure to the user before making changes.
3. Use `mv` commands in the terminal, batched where possible.
4. Update any references (imports, configs, paths) affected by the reorganization.

## Key Principles

- **Read before write**: Never edit a file without reading it first.
- **Reversibility**: Prefer edits and moves over deletions. Ask before destructive ops.
- **Absolute paths**: Always use absolute paths in tool calls.
- **Batch parallel reads**: When checking multiple files, read them in parallel.
- **Validate after write**: After creating or editing, confirm the result is correct.

## Examples

**Create a config file:**
> `/file create a .env.example with DATABASE_URL, API_KEY, and DEBUG vars`

**Find all test files:**
> `/file find all test files under workspace/`

**Reorganize a directory:**
> `/file move all *.log files in /tmp into /tmp/logs/`

**Bulk edit:**
> `/file replace all occurrences of "localhost:8080" with "localhost:3000" in config files`
