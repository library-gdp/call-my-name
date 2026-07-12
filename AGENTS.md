# Repository Guidelines

## Project Structure & Module Organization

This repository contains a Codex skill rather than a deployable application. The skill lives under `call-my-name/skills/write-korean-cover-letter/`:

- `SKILL.md` defines the skill metadata, operating rules, workflow, and output checks.
- `agents/openai.yaml` provides the user-facing display name, description, and default prompt.
- `references/writing-guide.md` contains detailed writing criteria loaded when needed.

Keep core instructions concise in `SKILL.md`; place supporting detail in `references/` and link to it with a relative path. Add new skills as sibling directories under `call-my-name/skills/`, using lowercase kebab-case names.

These commands inventory skill files, review heading structure, confirm YAML text renders as UTF-8, and detect whitespace errors. Before submitting, invoke the skill in Codex with a representative Korean cover-letter request and verify that referenced files load correctly.

## Security & Source Integrity

Never commit resumes, credentials, detailed addresses, resident registration numbers, or other applicant data. Preserve the skill's requirements to use public sources, respect access restrictions, verify posting status and deadlines, and distinguish sourced facts from interpretation.
